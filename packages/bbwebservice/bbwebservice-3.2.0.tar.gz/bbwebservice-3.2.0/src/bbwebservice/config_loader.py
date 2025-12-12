import sys as system
import json
import os
from typing import List, Literal, Optional, Union

from .__init__ import MAIN_PATH
from .type_validation import Constraint, Scheme, ValidationError, satisfies

ERROR_PREFIX = '[CONFIG_ERROR]'

HOST_ENTRY_SCHEMA = {
    "host": {"type": str},
    "cert_path": {"type": str},
    "key_path": {"type": str},
}

HOST_TYPE = Union[str, List[Scheme[HOST_ENTRY_SCHEMA]]]

SERVER_BASE_SCHEMA = {
    "ip": {"type": str},
    "port": {"type": Constraint[int, '>=', 0]},
    "queue_size": {"type": Constraint[int, '>=', 0]},
    "max_threads": {"type": Optional[Constraint[int, '>=', 0]], "default": None},
    "max_threads_per_process": {"type": Optional[Constraint[int, '>=', 1]], "default": None},
    "connection_queue_timeout": {"type": Optional[Constraint[int, '>=', 0]], "default": None},
    "keep_alive_timeout": {"type": Optional[Constraint[int, '>=', 0]], "default": None},
    "keep_alive_max_requests": {"type": Optional[Constraint[int, '>=', 0]], "default": None},
    "header_timeout": {"type": Optional[Constraint[int, '>=', 0]], "default": None},
    "body_min_rate_bytes_per_sec": {"type": Optional[Constraint[int, '>=', 0]], "default": None},
    "handler_timeout": {"type": Optional[Constraint[int, '>=', 0]], "default": None},
    "ssl_handshake_timeout": {"type": Optional[Constraint[int, '>=', 0]], "default": None},
    "https-redirect": {"type": Optional[Literal[True, False]], "default": False},
    "https-redirect-escape-paths": {"type": Optional[List[str]], "default": []},
    "update-cert-state": {"type": Optional[Literal[True, False]], "default": False},
    "stream_max_chunk_size": {"type": Optional[Constraint[int, '>=', 1]], "default": None},
    "stream_max_total_bytes": {"type": Optional[Constraint[int, '>=', 0]], "default": None},
    "stream_max_duration": {"type": Optional[Constraint[float, '>=', 0]], "default": None},
    "stream_idle_timeout": {"type": Optional[Constraint[float, '>=', 0]], "default": None},
}

SSL_DISABLED_SCHEMA = {
    **SERVER_BASE_SCHEMA,
    "SSL": {"type": Literal[False]},
    "host": {"type": HOST_TYPE, "default": ""},
    "cert_path": {"type": Optional[str], "default": ""},
    "key_path": {"type": Optional[str], "default": ""},
}

SSL_ENABLED_SCHEMA = {
    **SERVER_BASE_SCHEMA,
    "SSL": {"type": Literal[True]},
    "host": {"type": HOST_TYPE, "default": ""},
    "cert_path": {"type": Optional[str], "default": ""},
    "key_path": {"type": Optional[str], "default": ""},
}

SERVER_SCHEMA = Union[Scheme[SSL_DISABLED_SCHEMA], Scheme[SSL_ENABLED_SCHEMA]]

DEFAULT_WORKER_PROCESSES = max(1, os.cpu_count() or 1)
DEFAULT_MAX_THREADS_PER_PROCESS = 16

CONFIG_SCHEMA = Scheme({
    "max_threads": {"type": Constraint[int, '>=', 0], "default": 100},
    "max_threads_per_process": {"type": Constraint[int, '>=', 1], "default": DEFAULT_MAX_THREADS_PER_PROCESS},
    "max_header_size": {"type": Constraint[int, '>', 0], "default": 16384},
    "max_body_size": {"type": Constraint[int, '>', 0], "default": 10485760},
    "max_url_length": {"type": Constraint[int, '>', 0], "default": 2048},
    "keep_alive_timeout": {"type": Constraint[int, '>=', 0], "default": 15},
    "keep_alive_max_requests": {"type": Constraint[int, '>=', 0], "default": 100},
    "header_timeout": {"type": Constraint[int, '>=', 0], "default": 10},
    "body_min_rate_bytes_per_sec": {"type": Constraint[int, '>=', 0], "default": 1024},
    "handler_timeout": {"type": Constraint[int, '>=', 0], "default": 30},
    "stream_max_chunk_size": {"type": Constraint[int, '>=', 1], "default": 65536},
    "stream_max_total_bytes": {"type": Constraint[int, '>=', 0], "default": 10485760},
    "stream_max_duration": {"type": Constraint[float, '>=', 0], "default": 60.0},
    "stream_idle_timeout": {"type": Constraint[float, '>=', 0], "default": 10.0},
    "connection_queue_timeout": {"type": Constraint[int, '>=', 0], "default": 2},
    "ssl_handshake_timeout": {"type": Constraint[int, '>=', 0], "default": 5},
    "worker_processes": {"type": Constraint[int, '>=', 1], "default": DEFAULT_WORKER_PROCESSES},
    "worker_timeout_threshold": {"type": Constraint[float, '>=', 0], "default": 0.5},
    "server": {"type": List[SERVER_SCHEMA]},
})


def _normalize_host_entries(host):
    if isinstance(host, list):
        return host
    if isinstance(host, str) and host:
        return [{"host": host, "cert_path": "", "key_path": ""}]
    return []


class Config:
    def __init__(self) -> None:
        """Load and validate configuration values from config.json."""

        config_path = MAIN_PATH + "/config/config.json"

        with open(config_path, 'r', encoding='utf-8') as file:
            config_raw = json.load(file)

        config_data = dict(config_raw)
        updated_config = False
        server_timeout_keys = [
            'keep_alive_timeout',
            'keep_alive_max_requests',
            'header_timeout',
            'body_min_rate_bytes_per_sec',
            'handler_timeout',
            'connection_queue_timeout',
            'ssl_handshake_timeout',
            'stream_max_chunk_size',
            'stream_max_total_bytes',
            'stream_max_duration',
            'stream_idle_timeout',
        ]
        for entry in config_data.get('server', []):
            for key in server_timeout_keys:
                if key not in entry:
                    entry[key] = None
                    updated_config = True
        if 'max_threads_per_process' not in config_data:
            fallback = config_data.get('max_threads', DEFAULT_MAX_THREADS_PER_PROCESS)
            config_data['max_threads_per_process'] = max(1, fallback)
            updated_config = True
        stream_root_defaults = {
            'stream_max_chunk_size': 65536,
            'stream_max_total_bytes': 10485760,
            'stream_max_duration': 60.0,
            'stream_idle_timeout': 10.0,
        }
        for key, default in stream_root_defaults.items():
            if key not in config_data:
                config_data[key] = default
                updated_config = True
        for entry in config_data.get('server', []):
            if entry.get('max_threads_per_process') is None:
                if entry.get('max_threads') is not None:
                    entry['max_threads_per_process'] = max(1, entry['max_threads'])
                else:
                    entry['max_threads_per_process'] = config_data['max_threads_per_process']
                updated_config = True
        wt_threshold = config_data.get('worker_timeout_threshold', 0.5)
        try:
            config_data['worker_timeout_threshold'] = float(wt_threshold)
        except (TypeError, ValueError):
            config_data['worker_timeout_threshold'] = 0.5
        duration_keys = ['stream_max_duration', 'stream_idle_timeout']
        for key in duration_keys:
            if key in config_data and config_data[key] is not None:
                try:
                    config_data[key] = float(config_data[key])
                except (TypeError, ValueError):
                    pass
        for entry in config_data.get('server', []):
            for key in duration_keys:
                if key in entry and entry[key] is not None:
                    try:
                        entry[key] = float(entry[key])
                    except (TypeError, ValueError):
                        pass
        errors: List[ValidationError] = []
        is_valid = satisfies(config_data, CONFIG_SCHEMA, strict=True, _errors=errors)
        if not is_valid:
            for error in errors:
                print(ERROR_PREFIX, str(error))
            system.exit(0)
        if updated_config:
            try:
                with open(config_path, 'w', encoding='utf-8') as file:
                    json.dump(config_data, file, indent=2)
            except OSError as err:
                print(ERROR_PREFIX, f'Failed to update config defaults: {err}')

        self.MAX_THREADS = config_data['max_threads']
        self.MAX_THREADS_PER_PROCESS = config_data.get('max_threads_per_process', config_data['max_threads'])
        self.MAX_HEADER_SIZE = config_data['max_header_size']
        self.MAX_BODY_SIZE = config_data['max_body_size']
        self.MAX_URL_LENGTH = config_data['max_url_length']
        self.KEEP_ALIVE_TIMEOUT = config_data['keep_alive_timeout']
        self.KEEP_ALIVE_MAX_REQUESTS = config_data['keep_alive_max_requests']
        self.HEADER_TIMEOUT = config_data['header_timeout']
        self.BODY_MIN_RATE_BYTES_PER_SEC = config_data['body_min_rate_bytes_per_sec']
        self.HANDLER_TIMEOUT = config_data['handler_timeout']
        self.STREAM_MAX_CHUNK_SIZE = config_data['stream_max_chunk_size']
        self.STREAM_MAX_TOTAL_BYTES = config_data['stream_max_total_bytes']
        self.STREAM_MAX_DURATION = config_data['stream_max_duration']
        self.STREAM_IDLE_TIMEOUT = config_data['stream_idle_timeout']
        self.CONNECTION_QUEUE_TIMEOUT = config_data['connection_queue_timeout']
        self.SSL_HANDSHAKE_TIMEOUT = config_data['ssl_handshake_timeout']
        self.WORKER_PROCESSES = config_data['worker_processes']
        self.WORKER_TIMEOUT_THRESHOLD = config_data['worker_timeout_threshold']
        self.SERVERS = []
        for entry in config_data['server']:
            normalized_entry = dict(entry)
            normalized_entry['host'] = _normalize_host_entries(normalized_entry.get('host', ''))
            if normalized_entry['SSL']:
                cert_path = normalized_entry.get('cert_path', '')
                key_path = normalized_entry.get('key_path', '')
                host_entries = normalized_entry['host']
                if not host_entries and (not cert_path or not key_path):
                    print(ERROR_PREFIX, "SSL server requires 'cert_path' and 'key_path' when no host list is provided.")
                    system.exit(0)
                if host_entries and (not cert_path or not key_path):
                    first_host = host_entries[0]
                    normalized_entry['cert_path'] = first_host['cert_path']
                    normalized_entry['key_path'] = first_host['key_path']
            else:
                normalized_entry['cert_path'] = normalized_entry.get('cert_path', '')
                normalized_entry['key_path'] = normalized_entry.get('key_path', '')
            if normalized_entry.get('max_threads') is None:
                normalized_entry['max_threads'] = self.MAX_THREADS
            normalized_entry['https-redirect'] = bool(normalized_entry.get('https-redirect', False))
            normalized_entry['https-redirect-escape-paths'] = list(normalized_entry.get('https-redirect-escape-paths', []))
            normalized_entry['update-cert-state'] = bool(normalized_entry.get('update-cert-state', False))
            timeout_defaults = {
                'keep_alive_timeout': self.KEEP_ALIVE_TIMEOUT,
                'keep_alive_max_requests': self.KEEP_ALIVE_MAX_REQUESTS,
                'header_timeout': self.HEADER_TIMEOUT,
                'body_min_rate_bytes_per_sec': self.BODY_MIN_RATE_BYTES_PER_SEC,
                'handler_timeout': self.HANDLER_TIMEOUT,
                'ssl_handshake_timeout': self.SSL_HANDSHAKE_TIMEOUT,
                'stream_max_chunk_size': self.STREAM_MAX_CHUNK_SIZE,
                'stream_max_total_bytes': self.STREAM_MAX_TOTAL_BYTES,
                'stream_max_duration': self.STREAM_MAX_DURATION,
                'stream_idle_timeout': self.STREAM_IDLE_TIMEOUT,
            }
            for key, default in timeout_defaults.items():
                if normalized_entry.get(key) is None:
                    normalized_entry[key] = default
            self.SERVERS.append(normalized_entry)

    def _get_server_value(self, key):
        if not self.SERVERS:
            return None
        return self.SERVERS[0].get(key)

    def _set_server_value(self, key, value):
        if not self.SERVERS:
            return
        self.SERVERS[0][key] = value

    @property
    def SERVER_IP(self):
        return self._get_server_value('ip')

    @SERVER_IP.setter
    def SERVER_IP(self, value):
        self._set_server_value('ip', value)

    @property
    def SERVER_PORT(self):
        return self._get_server_value('port')

    @SERVER_PORT.setter
    def SERVER_PORT(self, value):
        self._set_server_value('port', value)

    @property
    def QUE_SIZE(self):
        return self._get_server_value('queue_size')

    @QUE_SIZE.setter
    def QUE_SIZE(self, value):
        self._set_server_value('queue_size', value)

    @property
    def SSL(self):
        return self._get_server_value('SSL')

    @SSL.setter
    def SSL(self, value):
        self._set_server_value('SSL', value)

    @property
    def HOST(self):
        return self._get_server_value('host')

    @HOST.setter
    def HOST(self, value):
        self._set_server_value('host', _normalize_host_entries(value))

    @property
    def CERT_PATH(self):
        return self._get_server_value('cert_path')

    @CERT_PATH.setter
    def CERT_PATH(self, value):
        self._set_server_value('cert_path', value)

    @property
    def KEY_PATH(self):
        return self._get_server_value('key_path')

    @KEY_PATH.setter
    def KEY_PATH(self, value):
        self._set_server_value('key_path', value)

    @property
    def SERVER_MAX_THREADS(self):
        return self._get_server_value('max_threads')

    @SERVER_MAX_THREADS.setter
    def SERVER_MAX_THREADS(self, value):
        self._set_server_value('max_threads', value)

    @property
    def HTTPS_REDIRECT(self):
        return self._get_server_value('https-redirect')

    @HTTPS_REDIRECT.setter
    def HTTPS_REDIRECT(self, value):
        self._set_server_value('https-redirect', bool(value))

    @property
    def HTTPS_REDIRECT_ESCAPE_PATHS(self):
        return self._get_server_value('https-redirect-escape-paths')

    @HTTPS_REDIRECT_ESCAPE_PATHS.setter
    def HTTPS_REDIRECT_ESCAPE_PATHS(self, value):
        paths = list(value) if isinstance(value, list) else []
        self._set_server_value('https-redirect-escape-paths', paths)

    @property
    def UPDATE_CERT_STATE(self):
        return self._get_server_value('update-cert-state')

    @UPDATE_CERT_STATE.setter
    def UPDATE_CERT_STATE(self, value):
        self._set_server_value('update-cert-state', bool(value))
