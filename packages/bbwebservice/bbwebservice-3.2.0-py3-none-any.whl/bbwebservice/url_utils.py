HEX_CHARS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']


#TODO: unefficient af fix that 

def leading_ones_count(encoded_byte):
    byte_value = int(encoded_byte, 16)
    count = 0
    mask = 0x80 
    while mask != 0 and byte_value & mask:
        count += 1
        mask >>= 1
    return count

def unescape_url(url:str) -> str:
    unescaped = ''
    escape_sequence = ''
    index = 0
    count = 0
    url_len = len(url)
    
    while index < url_len:
        
        if len(escape_sequence) == 0 and url[index] == '%' and index + 3 <= url_len and url[index+1] in HEX_CHARS and url[index+2] in HEX_CHARS:
            escape_byte = url[index+1:index+3]
            count =  leading_ones_count(escape_byte)
            escape_sequence += escape_byte
            index += 3
            
        elif url[index] == '%' and index + 3 <= url_len and url[index+1] in HEX_CHARS and url[index+2] in HEX_CHARS and count > 1:
            escape_byte = url[index+1:index+3]
            count -= 1
            escape_sequence+= escape_byte
            index += 3
            
        elif escape_sequence:
            unescaped += decode_hex_string(escape_sequence)
            escape_sequence = ''
            count = 0
        else:
            unescaped += url[index]
            index += 1

    return unescaped if not escape_sequence else unescaped + decode_hex_string(escape_sequence)
            

def decode_hex_string(hex_string:str) ->str:
    try:
        decoded_bytes = bytes.fromhex(hex_string)
        unicode_char = decoded_bytes.decode('utf-8')
        return unicode_char
    except UnicodeDecodeError:
        return ''


def _normalize_port(port_str: str | None):
    if port_str is None:
        return None
    if port_str == '':
        return None
    if not port_str.isdigit():
        raise ValueError(f"Invalid port specifier '{port_str}'.")
    return int(port_str)


def _parse_ip_port(component: str):
    component = component.strip()
    if not component:
        return (None, None)
    ip = None
    port = None
    if component.startswith('['):
        end = component.find(']')
        if end == -1:
            raise ValueError(f"Invalid IPv6 specifier '{component}'.")
        ip = component[1:end]
        remainder = component[end+1:]
        if remainder.startswith(':'):
            port = _normalize_port(remainder[1:])
        elif remainder:
            raise ValueError(f"Invalid specifier '{component}'.")
    else:
        if component.startswith(':'):
            port = _normalize_port(component[1:])
        elif component.count(':') == 1:
            ip_part, port_part = component.split(':', 1)
            ip = ip_part or None
            port = _normalize_port(port_part)
        else:
            ip = component or None
    return (ip, port)


def split_route_scope(route):
    if isinstance(route, UrlTemplate):
        return (route.ip, route.port, route.domain, route.path_template)
    if not isinstance(route, str):
        return (None, None, None, route)
    slash_index = route.find('/')
    if slash_index == -1:
        prefix = route
        path = route if route.startswith('/') else '/' + route
    else:
        prefix = route[:slash_index]
        path = route[slash_index:]
    ip = port = domain = None
    if '::' in prefix:
        ip_part, domain_part = prefix.rsplit('::', 1)
        ip, port = _parse_ip_port(ip_part)
        domain = domain_part.rstrip(':') or None
    elif prefix:
        ip, port = _parse_ip_port(prefix)
    if not path.startswith('/'):
        path = '/' + path if path else '/'
    return (ip, port, domain, path)


def format_ip_port(ip, port):
    if ip is None and port is None:
        return ''
    ip_repr = ''
    if ip is not None:
        ip_repr = f'[{ip}]' if (':' in ip and not ip.startswith('[')) else ip
    if port is not None:
        port_str = str(port)
        if ip_repr:
            return f'{ip_repr}:{port_str}'
        return f':{port_str}'
    return ip_repr


def _is_decimal(value: str) -> bool:
    if value.count('.') != 1:
        return False
    left, right = value.split('.', 1)
    return bool(left) and bool(right) and left.isdigit() and right.isdigit()


class UrlTemplate:
    """
    A URL template wraps a route string with optional IP/port/domain selectors
    plus path placeholders.

    Syntax:
        ip:port::domain:/path/to/{placeholders}

    Examples:
        - '::/status'                                -> matches every endpoint regardless of IP or domain
        - '127.0.0.1::/debug'                        -> IPv4 127.0.0.1, all ports, all domains
        - ':8443::/metrics'                          -> any IP, port 8443
        - ':::example.com:/domain-only'              -> all IPs/ports, only domain `example.com`
        - '127.0.0.1:8000::example.com:/foo'         -> specific IP/port/domain combination
        - '[::1]:8080::/ipv6/{path:path}'            -> IPv6 loopback, port 8080, path wildcard

    Path placeholders use the familiar '{name:type}' syntax and support the built-in
    types ('int', 'str', 'float', 'bool', 'path').
    """

    _PLACEHOLDER_TYPES = {
        'int': (
            lambda value: value.isdigit(),
            int,
        ),
        'float': (
            lambda value: _is_decimal(value),
            float,
        ),
        'bool': (
            lambda value: value in ('True', 'False'),
            lambda value: value == 'True',
        ),
        'str': (
            lambda value: bool(value) and all(ch.isalnum() or ch == '_' for ch in value),
            lambda value: value,
        ),
        'path': (
            lambda value: bool(value),
            lambda value: value,
        ),
    }

    def __init__(self, template_string):
        self.template = template_string
        self.ip, self.port, self.domain, self.path_template = split_route_scope(template_string)
        self.handler = None
        self.type = None
        self._is_root = self.path_template == '/'
        self._requires_trailing_slash = bool(self.path_template.endswith('/') and not self._is_root)
        self._segments = self._compile_segments()
        self._path_wildcard_index = None
        self._path_placeholder_name = None
        for idx, segment in enumerate(self._segments):
            if segment.get('path_placeholder'):
                self._path_wildcard_index = idx
                self._path_placeholder_name = segment['path_placeholder']
                break

    def _compile_segments(self):
        if self._is_root:
            return []
        raw = self.path_template.strip('/')
        if not raw:
            return []
        parts = raw.split('/')
        segments = []
        path_placeholder_seen = False
        for index, part in enumerate(parts):
            tokens = self._parse_segment_tokens(part)
            if tokens and any(tok['kind'] == 'var' and tok['var_type'] == 'path' for tok in tokens):
                if path_placeholder_seen:
                    raise ValueError('Only one {path:path} placeholder is allowed per UrlTemplate.')
                if len(tokens) != 1 or tokens[0]['var_type'] != 'path':
                    raise ValueError('{path:path} must occupy an entire path segment.')
                if index != len(parts) - 1:
                    raise ValueError('{path:path} must be the final segment in a UrlTemplate.')
                path_placeholder_seen = True
                segments.append({
                    'tokens': tokens,
                    'path_placeholder': tokens[0]['name'],
                })
                continue
            segments.append({'tokens': tokens})
        return segments

    def _parse_segment_tokens(self, segment):
        if not segment:
            return []
        tokens = []
        idx = 0
        last_token_was_var = False
        while idx < len(segment):
            start = segment.find('{', idx)
            if start == -1:
                literal = segment[idx:]
                if literal:
                    tokens.append({'kind': 'literal', 'value': literal})
                break
            if start > idx:
                literal = segment[idx:start]
                if literal:
                    tokens.append({'kind': 'literal', 'value': literal})
                    last_token_was_var = False
            end = segment.find('}', start)
            if end == -1:
                raise ValueError(f"Malformed placeholder in '{segment}'.")
            inner = segment[start + 1:end]
            if ':' not in inner:
                raise ValueError(f"Invalid placeholder '{inner}', expected syntax {{name:type}}.")
            name, type_name = inner.split(':', 1)
            if not name or not all(ch.isalnum() or ch == '_' for ch in name):
                raise ValueError(f"Invalid placeholder name '{name}'.")
            if type_name not in self._PLACEHOLDER_TYPES:
                raise ValueError(f"Unknown placeholder type '{type_name}'.")
            if last_token_was_var:
                raise ValueError('Adjacent placeholders must be separated by literal text.')
            tokens.append({'kind': 'var', 'name': name, 'var_type': type_name})
            last_token_was_var = True
            idx = end + 1
        return tokens

    def _split_request_segments(self, path):
        if path == '/':
            return []
        trimmed = path.strip('/')
        if not trimmed:
            return []
        return trimmed.split('/')

    def _next_literal(self, tokens, start_index):
        for offset in range(start_index, len(tokens)):
            token = tokens[offset]
            if token['kind'] == 'literal' and token['value']:
                return token['value']
        return None

    def _match_segment(self, tokens, segment):
        if not tokens:
            return {} if segment == '' else None
        position = 0
        values = {}
        for idx, token in enumerate(tokens):
            if token['kind'] == 'literal':
                literal = token['value']
                if not segment.startswith(literal, position):
                    return None
                position += len(literal)
            else:
                var_type = token['var_type']
                validator, converter = self._PLACEHOLDER_TYPES[var_type]
                next_literal = self._next_literal(tokens, idx + 1)
                if next_literal is None:
                    value = segment[position:]
                    position = len(segment)
                else:
                    next_index = segment.find(next_literal, position)
                    if next_index == -1:
                        return None
                    value = segment[position:next_index]
                    position = next_index
                if not value or not validator(value):
                    return None
                values[token['name']] = converter(value)
        if position != len(segment):
            return None
        return values

    def _match_path(self, path, ip=None, port=None, domain=None):
        if not path or not path.startswith('/'):
            return None
        if self.ip is not None and self.ip != ip:
            return None
        if self.port is not None and self.port != port:
            return None
        if self.domain:
            if domain is None or self.domain != domain:
                return None

        if self._is_root:
            return {} if path == '/' else None

        has_trailing_slash = path.endswith('/') and path != '/'
        if self._requires_trailing_slash != has_trailing_slash:
            return None

        request_segments = self._split_request_segments(path)
        extracted = {}

        if self._path_wildcard_index is not None:
            min_segments = self._path_wildcard_index + 1
            if len(request_segments) < min_segments:
                return None
        elif len(request_segments) != len(self._segments):
            return None

        for index, segment_def in enumerate(self._segments):
            if self._path_wildcard_index is not None and index == self._path_wildcard_index:
                remaining = request_segments[index:]
                value = '/'.join(remaining)
                if not value:
                    return None
                validator, converter = self._PLACEHOLDER_TYPES['path']
                if not validator(value):
                    return None
                extracted[segment_def['path_placeholder']] = converter(value)
                break
            segment_value = request_segments[index]
            segment_result = self._match_segment(segment_def['tokens'], segment_value)
            if segment_result is None:
                return None
            extracted.update(segment_result)

        return extracted

    def extract(self, url):
        return self._match_path(url)

    def matches(self, ip, port, domain, path):
        return self._match_path(path, ip, port, domain) is not None

    def __eq__(self, other):
        if isinstance(other, str):
            return self._match_path(other) is not None
        if isinstance(other, self.__class__):
            return (
                self.path_template == other.path_template
                and self.ip == other.ip
                and self.port == other.port
                and self.domain == other.domain
            )
        return False
