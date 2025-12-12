import importlib
import socket
from threading import Thread, Event, current_thread, Lock, Condition, RLock
import ssl
import os
import time
import errno
import random
from collections import deque
from .config_loader import Config
from . import global_state
from .http_parser import HTTP_Message_Factory, log, LOGGING_OPTIONS, LOGGING_CALLBACK, LOGGING_SCOPED_OPTIONS, LOGGING_SCOPED_CALLBACKS, LOG_LOCK
import traceback
from .url_utils import format_ip_port, UrlTemplate
from .worker_pool import ProcessWorkerPool
from .callable_blueprint import CallableBlueprint
from . import metrics as metrics_module


SSL_CONTEXTS = {}
SESSIONS = {}
PAGES = {}
GET_TEMPLATES = []
POST_HANDLER = {}
POST_TEMPLATES = []
PUT_HANDLER = {}
PUT_TEMPLATES = []
DELETE_HANDLER = {}
DELETE_TEMPLATES = []
PATCH_HANDLER = {}
PATCH_TEMPLATES = []
OPTIONS_HANDLER = {}
OPTIONS_TEMPLATES = []
ERROR_HANDLER = {}
ROUTES = {
    'GET': {'static': {}, 'templates': []},
    'POST': {'static': {}, 'templates': []},
    'PUT': {'static': {}, 'templates': []},
    'DELETE': {'static': {}, 'templates': []},
    'PATCH': {'static': {}, 'templates': []},
    'OPTIONS': {'static': {}, 'templates': []},
}
RESPONSE_LOG_PREVIEW_BYTES = 1024
DEFAULT_KEEP_ALIVE_TIMEOUT = 15
DEFAULT_KEEP_ALIVE_MAX_REQUESTS = 100
KEEP_ALIVE_TIMEOUT = DEFAULT_KEEP_ALIVE_TIMEOUT
KEEP_ALIVE_MAX_REQUESTS = DEFAULT_KEEP_ALIVE_MAX_REQUESTS
CERT_MONITOR_INTERVAL = 60
CERT_MONITOR_JITTER = 10
DEFAULT_HANDSHAKE_TIMEOUT = 5
DEFAULT_ACCEPT_TIMEOUT = 5.0
DEFAULT_CONNECTION_QUEUE_TIMEOUT = 2.0
CORS_SETTINGS = {
    'enabled': False,
    'allow_origin': '*',
    'allow_methods': ['GET', 'POST', 'OPTIONS'],
    'allow_headers': ['*'],
    'expose_headers': [],
    'allow_credentials': False,
    'max_age': 600,
}

CONFIG = Config()
KEEP_ALIVE_TIMEOUT = getattr(CONFIG, "KEEP_ALIVE_TIMEOUT", KEEP_ALIVE_TIMEOUT)
KEEP_ALIVE_MAX_REQUESTS = getattr(CONFIG, "KEEP_ALIVE_MAX_REQUESTS", KEEP_ALIVE_MAX_REQUESTS)
DEFAULT_HANDSHAKE_TIMEOUT = getattr(CONFIG, "SSL_HANDSHAKE_TIMEOUT", DEFAULT_HANDSHAKE_TIMEOUT)
HEADER_TIMEOUT = getattr(CONFIG, "HEADER_TIMEOUT", 10)
BODY_MIN_RATE_BYTES_PER_SEC = getattr(CONFIG, "BODY_MIN_RATE_BYTES_PER_SEC", 1024)
HANDLER_TIMEOUT = getattr(CONFIG, "HANDLER_TIMEOUT", 30)
CONNECTION_QUEUE_TIMEOUT = getattr(CONFIG, "CONNECTION_QUEUE_TIMEOUT", DEFAULT_CONNECTION_QUEUE_TIMEOUT)
ROUTE_LOCK = RLock()
SERVER_MANAGER = None


class ScheduledTask:
    def __init__(self, manager, func, interval):
        self.manager = manager
        self.func = func
        self.interval = max(interval, 0)
        self.state = Event()
        self.thread = None
        self._expects_data = False
        if hasattr(func, '__code__'):
            arg_count = func.__code__.co_argcount
            arg_names = func.__code__.co_varnames[:arg_count]
            self._expects_data = 'data' in arg_names

    def start(self):
        if self.thread and self.thread.is_alive():
            return
        self.state.set()
        self.thread = Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        self.state.clear()
        if self.thread:
            self.thread.join(timeout=1)
            self.thread = None

    def _run(self):
        while self.state.is_set():
            try:
                if self._expects_data:
                    self.func(data=self.manager.build_task_data())
                else:
                    self.func()
            except Exception as err:
                log(f'[SERVER TASK] error: {err}', log_lvl='debug')
                traceback.print_exc()
            if not self.state.is_set():
                break
            if self.interval == 0:
                self.state.wait(0.1)
                continue
            self.state.wait(self.interval)


class ServerInstance:
    def __init__(self, manager, settings):
        self.manager = manager
        self.settings = settings
        self.ip = settings['ip']
        self.port = settings['port']
        self.queue_size = settings['queue_size']
        self.max_threads = settings.get('max_threads', manager.global_max_threads)
        self.ssl_enabled = settings['SSL']
        self.host_entries = settings.get('host', [])
        self.cert_path = settings.get('cert_path', '')
        self.key_path = settings.get('key_path', '')
        self.https_redirect = settings.get('https-redirect', False)
        self.https_redirect_escape_paths = settings.get('https-redirect-escape-paths', [])
        self.update_cert_state = settings.get('update-cert-state', False)
        self.state = Event()
        self.server_socket = None
        self.thread = None
        self.worker_handles = []
        self.lock = Lock()
        self.active_connections = 0
        self.ssl_context = None
        self.sni_contexts = {}
        inherited_handshake = getattr(manager.config, 'SSL_HANDSHAKE_TIMEOUT', DEFAULT_HANDSHAKE_TIMEOUT)
        self.handshake_timeout = settings.get('ssl_handshake_timeout', inherited_handshake)
        config = manager.config
        self.keep_alive_timeout = settings.get('keep_alive_timeout', getattr(config, 'KEEP_ALIVE_TIMEOUT', KEEP_ALIVE_TIMEOUT))
        self.keep_alive_max_requests = settings.get('keep_alive_max_requests', getattr(config, 'KEEP_ALIVE_MAX_REQUESTS', KEEP_ALIVE_MAX_REQUESTS))
        self.header_timeout = settings.get('header_timeout', getattr(config, 'HEADER_TIMEOUT', HEADER_TIMEOUT))
        self.body_min_rate = settings.get('body_min_rate_bytes_per_sec', getattr(config, 'BODY_MIN_RATE_BYTES_PER_SEC', BODY_MIN_RATE_BYTES_PER_SEC))
        self.handler_timeout = settings.get('handler_timeout', getattr(config, 'HANDLER_TIMEOUT', HANDLER_TIMEOUT))
        stream_chunk_setting = settings.get('stream_max_chunk_size')
        self.stream_max_chunk_size = getattr(config, 'STREAM_MAX_CHUNK_SIZE', None) if stream_chunk_setting is None else stream_chunk_setting
        stream_total_setting = settings.get('stream_max_total_bytes')
        self.stream_max_total_bytes = getattr(config, 'STREAM_MAX_TOTAL_BYTES', None) if stream_total_setting is None else stream_total_setting
        stream_duration_setting = settings.get('stream_max_duration')
        self.stream_max_duration = getattr(config, 'STREAM_MAX_DURATION', None) if stream_duration_setting is None else stream_duration_setting
        stream_idle_setting = settings.get('stream_idle_timeout')
        self.stream_idle_timeout = getattr(config, 'STREAM_IDLE_TIMEOUT', None) if stream_idle_setting is None else stream_idle_setting
        self._ctx_lock = Lock()
        self._cert_monitor_interval = CERT_MONITOR_INTERVAL
        self._cert_monitor_jitter = CERT_MONITOR_JITTER
        self._cert_monitor_state = Event()
        self._cert_monitor_thread = None
        self._cert_sources = []
        self.bound_ip = None
        self.address_family = socket.AF_INET
        queue_timeout = settings.get('connection_queue_timeout')
        if queue_timeout is None:
            queue_timeout = getattr(config, 'CONNECTION_QUEUE_TIMEOUT', CONNECTION_QUEUE_TIMEOUT)
        if queue_timeout and queue_timeout > 0:
            self.connection_queue_timeout = float(queue_timeout)
        else:
            self.connection_queue_timeout = None
            if self.header_timeout:
                self.connection_queue_timeout = float(self.header_timeout)
        self._connection_queue = deque()
        self._connection_queue_lock = Lock()
        self._connection_queue_cv = Condition(self._connection_queue_lock)
        self._dispatcher_thread = None
        self._dispatch_notify = Event()
        self._queue_idle_delay = 0.05
        self._ssl_context_label = None

    def _resolve_ip(self):
        if self.ip == 'default':
            resolved = socket.gethostbyname(socket.gethostname())
        else:
            resolved = self.ip
        if isinstance(resolved, str) and resolved.startswith('[') and resolved.endswith(']'):
            resolved = resolved[1:-1]
        return resolved

    def build_dispatch_payload(self):
        return {
            'bound_ip': self.bound_ip,
            'port': self.port,
            'ssl_enabled': self.ssl_enabled,
            'cert_path': self.cert_path,
            'key_path': self.key_path,
            'host_entries': self.host_entries,
            'keep_alive_timeout': self.keep_alive_timeout,
            'keep_alive_max_requests': self.keep_alive_max_requests,
            'header_timeout': self.header_timeout,
            'body_min_rate': self.body_min_rate,
            'handler_timeout': self.handler_timeout,
            'handshake_timeout': self.handshake_timeout,
            'stream_max_chunk_size': self.stream_max_chunk_size,
            'stream_max_total_bytes': self.stream_max_total_bytes,
            'stream_max_duration': self.stream_max_duration,
            'stream_idle_timeout': self.stream_idle_timeout,
            'https_redirect': self.https_redirect,
            'https_redirect_escape_paths': self.https_redirect_escape_paths,
            'ssl_prepared': False,
            'cert_sources': list(self._cert_sources) if self._cert_sources else [],
        }

    def _record_cert_source(self, name, cert_path, key_path):
        if not cert_path or not key_path:
            return None
        cert_mtime, key_mtime = self._get_cert_mtimes(cert_path, key_path)
        return {
            'name': name,
            'cert_path': cert_path,
            'key_path': key_path,
            'cert_mtime': cert_mtime,
            'key_mtime': key_mtime,
        }

    @staticmethod
    def _get_cert_mtimes(cert_path, key_path):
        cert_mtime = None
        key_mtime = None
        try:
            cert_mtime = os.path.getmtime(cert_path)
        except OSError:
            pass
        try:
            key_mtime = os.path.getmtime(key_path)
        except OSError:
            pass
        return cert_mtime, key_mtime

    def _select_sni_context(self, server_name):
        selected = None
        if server_name and self.sni_contexts:
            selected = self.sni_contexts.get(server_name)
        return selected or self.ssl_context

    def _make_sni_callback(self):
        def _sni_callback(sock, server_name, context):
            selected = self._select_sni_context(server_name)
            if selected:
                sock.context = selected
                log(f'[SNI CALLBACK] Loaded certificate for {server_name}', log_lvl='debug')
            else:
                log(f'[SNI CALLBACK] Unknown server name: {server_name}', log_lvl='debug')
        return _sni_callback

    def _build_ssl_contexts(self):
        default_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        sni_contexts = {}
        sources = []
        fallback_cert = self.cert_path
        fallback_key = self.key_path
        if (not fallback_cert or not fallback_key) and self.host_entries:
            first_entry = self.host_entries[0]
            fallback_cert = first_entry.get('cert_path', '')
            fallback_key = first_entry.get('key_path', '')
        if fallback_cert and fallback_key:
            default_context.load_cert_chain(certfile=fallback_cert, keyfile=fallback_key)
            default_source = self._record_cert_source(format_ip_port(self.bound_ip, self.port) or 'default', fallback_cert, fallback_key)
            if default_source:
                sources.append(default_source)
        for host in self.host_entries:
            cert_path = host.get('cert_path')
            key_path = host.get('key_path')
            host_name = host.get('host')
            if not cert_path or not key_path:
                continue
            host_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            host_context.load_cert_chain(certfile=cert_path, keyfile=key_path)
            if host_name:
                sni_contexts[host_name] = host_context
                SSL_CONTEXTS[host_name] = host_context
            source = self._record_cert_source(host_name or '', cert_path, key_path)
            if source:
                sources.append(source)
        default_context.sni_callback = self._make_sni_callback()
        return default_context, sni_contexts, sources

    def _init_ssl_contexts(self):
        try:
            default_context, sni_contexts, cert_sources = self._build_ssl_contexts()
            with self._ctx_lock:
                self.ssl_context = default_context
                self.sni_contexts = sni_contexts
                self._cert_sources = cert_sources
            self._ssl_context_label = format_ip_port(self.bound_ip, self.port) or ''
            SSL_CONTEXTS[self._ssl_context_label] = self.ssl_context
            log(f'[SERVER] ssl active on {format_ip_port(self.bound_ip, self.port)}', log_lvl='debug')
        except Exception as err:
            log(f'[SERVER] error starting ssl: {err}', log_lvl='debug')
            traceback.print_exc()
            raise

    def _start_cert_monitor(self):
        if not self.update_cert_state or not self.ssl_enabled:
            return
        self._cert_monitor_state.set()
        self._cert_monitor_thread = Thread(target=self._cert_monitor_loop, daemon=True)
        self._cert_monitor_thread.start()

    def _stop_cert_monitor(self):
        if not self._cert_monitor_thread:
            return
        self._cert_monitor_state.clear()
        self._cert_monitor_thread.join(timeout=1)
        self._cert_monitor_thread = None

    def _cert_monitor_loop(self):
        while self._cert_monitor_state.is_set():
            try:
                self._check_cert_updates()
            except Exception as err:
                log(f'[CERT REFRESH] Unexpected reload error: {err}', log_lvl='debug')
                traceback.print_exc()
            interval = self._cert_monitor_interval
            jitter = self._cert_monitor_jitter
            wait_for = interval
            if jitter:
                wait_for += random.uniform(-jitter, jitter)
            wait_for = max(5, wait_for)
            self._cert_monitor_state.wait(wait_for)

    def _check_cert_updates(self):
        if not self.update_cert_state or not self.ssl_enabled:
            return False
        if not self._cert_sources:
            return False
        for source in self._cert_sources:
            cert_mtime, key_mtime = self._get_cert_mtimes(source['cert_path'], source['key_path'])
            if cert_mtime != source['cert_mtime'] or key_mtime != source['key_mtime']:
                break
        else:
            return False
        try:
            default_context, sni_contexts, cert_sources = self._build_ssl_contexts()
        except Exception as err:
            log(f'[CERT REFRESH] Failed to rebuild SSL contexts: {err}', log_lvl='debug')
            traceback.print_exc()
            return False
        with self._ctx_lock:
            self.ssl_context = default_context
            self.sni_contexts = sni_contexts
            self._cert_sources = cert_sources
            if self._ssl_context_label is None:
                self._ssl_context_label = format_ip_port(self.bound_ip, self.port) or ''
            SSL_CONTEXTS[self._ssl_context_label] = self.ssl_context
        log(f'[CERT REFRESH] Reloaded certificate sources for {format_ip_port(self.bound_ip, self.port)}', log_lvl='debug')
        return True

    def _init_socket(self):
        self.bound_ip = self._resolve_ip()
        use_ipv6 = self.bound_ip and ':' in self.bound_ip and self.bound_ip.count('.') == 0
        self.address_family = socket.AF_INET6 if use_ipv6 else socket.AF_INET
        if self.address_family == socket.AF_INET6:
            server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            try:
                server_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
            except AttributeError:
                pass
            bind_addr = (self.bound_ip, self.port, 0, 0)
        else:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            bind_addr = (self.bound_ip, self.port)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(bind_addr)
        server_socket.listen(self.queue_size)
        server_socket.settimeout(DEFAULT_ACCEPT_TIMEOUT)
        if self.ssl_enabled:
            self._init_ssl_contexts()
        return server_socket

    def _cleanup_workers(self):
        with self.lock:
            self.worker_handles = [handle for handle in self.worker_handles if handle.get('active')]

    def _enqueue_connection(self, conn, addr):
        handle = {'connection': conn, 'instance': self, 'active': True, 'address': addr, 'dispatched': False}
        entry = {
            'connection': conn,
            'address': addr,
            'handle': handle,
            'accepted_at': time.monotonic(),
        }
        with self._connection_queue_cv:
            if len(self._connection_queue) >= self.queue_size:
                return False
            self._connection_queue.append(entry)
            self._connection_queue_cv.notify()
        with self.lock:
            self.worker_handles.append(handle)
        return True

    def _pop_connection_entry(self):
        with self._connection_queue_cv:
            while not self._connection_queue:
                if not self.state.is_set():
                    return None
                self._connection_queue_cv.wait(0.05)
            return self._connection_queue.popleft()

    def _requeue_connection_front(self, entry):
        with self._connection_queue_cv:
            self._connection_queue.appendleft(entry)
            self._connection_queue_cv.notify()

    def _queue_entry_expired(self, entry):
        timeout = self.connection_queue_timeout
        if not timeout:
            return False
        return (time.monotonic() - entry['accepted_at']) >= timeout

    def _fail_queued_entry(self, entry):
        self._reject_connection(entry['connection'])
        self._finalize_handle(entry['handle'])

    def _wait_for_worker_signal(self):
        self._dispatch_notify.wait(self._queue_idle_delay)
        self._dispatch_notify.clear()

    def _dispatch_loop(self):
        while True:
            entry = self._pop_connection_entry()
            if entry is None:
                break
            if not self.state.is_set():
                self._fail_queued_entry(entry)
                continue
            if self._queue_entry_expired(entry):
                log(f'[QUEUE_TIMEOUT] dropping connection from {entry["address"]}', log_lvl='debug')
                self._fail_queued_entry(entry)
                continue
            limit_reached = False
            if self.max_threads and self.max_threads > 0:
                with self.lock:
                    limit_reached = self.active_connections >= self.max_threads
            if limit_reached:
                self._requeue_connection_front(entry)
                self._wait_for_worker_signal()
                continue
            try:
                submitted = self.manager.worker_pool.dispatch_connection(self, entry['connection'], entry['address'], entry['handle'])
            except Exception as err:
                log(f'[DISPATCH_ERROR] {err}', log_lvl='debug')
                self._fail_queued_entry(entry)
                continue
            if not submitted:
                self._requeue_connection_front(entry)
                self._wait_for_worker_signal()
                continue
            with self.lock:
                self.active_connections += 1
                entry['handle']['dispatched'] = True

    def _drain_connection_queue(self):
        entries = []
        with self._connection_queue_cv:
            while self._connection_queue:
                entries.append(self._connection_queue.popleft())
            self._connection_queue_cv.notify_all()
        for entry in entries:
            self._fail_queued_entry(entry)

    def _accept_loop(self):
        endpoint = format_ip_port(self.bound_ip, self.port) or f':{self.port}'
        print(f'[SERVER] {endpoint} running...')
        while self.state.is_set():
            self._cleanup_workers()
            try:
                conn, addr = self.server_socket.accept()
            except TimeoutError:
                continue
            except ssl.SSLError as err:
                if self.state.is_set():
                    log(f'[SSL_ACCEPT_ERROR] {err}', log_lvl='debug')
                continue
            except OSError as err:
                if not self.state.is_set():
                    break
                fatal_errors = {
                    errno.EBADF,
                    errno.ENOTSOCK,
                    errno.EINVAL,
                }
                if err.errno in fatal_errors:
                    log(f'[ACCEPT_ERROR] fatal {err}', log_lvl='debug')
                    break
                log(f'[ACCEPT_ERROR] non-fatal {err}', log_lvl='debug')
                continue
            except Exception as err:
                if self.state.is_set():
                    log(f'[CONNECTION_ERROR] {err}', log_lvl='debug')
                continue
            queued = self._enqueue_connection(conn, addr)
            if not queued:
                self._reject_connection(conn)
                log(f'[ACCEPT_QUEUE] rejecting connection for {endpoint} (queue full)', log_lvl='debug')
                continue

    def _finalize_handle(self, handle):
        dispatched = bool(handle.get('dispatched'))
        handle['active'] = False
        with self.lock:
            if handle in self.worker_handles:
                self.worker_handles.remove(handle)
            if dispatched and self.active_connections > 0:
                self.active_connections -= 1
        if dispatched:
            self._dispatch_notify.set()

    def _reject_connection(self, conn):
        try:
            if not self.ssl_enabled:
                response = b"HTTP/1.1 503 Service Unavailable\r\nConnection: close\r\nContent-Length: 0\r\n\r\n"
                conn.sendall(response)
        except Exception:
            pass
        finally:
            try:
                conn.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            try:
                conn.close()
            except Exception:
                pass

    def start(self):
        if self.thread and self.thread.is_alive():
            return
        self.server_socket = self._init_socket()
        self.state.set()
        self._dispatcher_thread = Thread(target=self._dispatch_loop, daemon=True)
        self._dispatcher_thread.start()
        self.thread = Thread(target=self._accept_loop, daemon=True)
        self.thread.start()
        self._start_cert_monitor()

    def shutdown(self):
        self.state.clear()
        self._dispatch_notify.set()
        with self._connection_queue_cv:
            self._connection_queue_cv.notify_all()
        self._drain_connection_queue()
        for handle in list(self.worker_handles):
            connection = handle['connection']
            try:
                connection.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            try:
                connection.close()
            except Exception:
                pass
            handle['active'] = False
            self._finalize_handle(handle)
        while True:
            with self.lock:
                remaining = self.active_connections
            if remaining == 0:
                break
            time.sleep(0.05)
        with self.lock:
            self.worker_handles = []
        if self.server_socket:
            try:
                self.server_socket.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            try:
                self.server_socket.close()
            except Exception:
                pass
            self.server_socket = None
        if self.thread:
            self.thread.join(timeout=1)
            self.thread = None
        if self._dispatcher_thread:
            self._dispatcher_thread.join(timeout=1)
            self._dispatcher_thread = None
        self._stop_cert_monitor()


class ServerManager:
    def __init__(self, config):
        self.config = config
        self.instances = []
        self.global_max_threads = config.MAX_THREADS
        self.running = False
        self.tasks = []
        self.worker_pool = ProcessWorkerPool(self.config, _build_runtime_snapshot, _export_global_resources)

    def start(self):
        if self.running:
            return
        self.running = True
        _ensure_metrics_shared_store()
        self.worker_pool.start()
        for settings in self.config.SERVERS:
            instance = ServerInstance(self, settings)
            instance.start()
            self.instances.append(instance)
        self._start_tasks()

    def _start_tasks(self):
        for task in self.tasks:
            task.start()

    def register_task(self, func, interval):
        task = ScheduledTask(self, func, interval)
        self.tasks.append(task)
        if self.running:
            task.start()
        return task

    def shutdown(self):
        if not self.running:
            return
        self.running = False
        for task in self.tasks:
            task.stop()
        for instance in list(self.instances):
            instance.shutdown()
        self.instances = []
        self.worker_pool.shutdown()

    def build_task_data(self):
        return {
            'sessions': SESSIONS,
            'config': self.config,
            'servers': self.instances,
            'routes': {
                'pages': PAGES,
                'get_templates': GET_TEMPLATES,
                'post_handler': POST_HANDLER,
                'post_templates': POST_TEMPLATES,
                'put_handler': PUT_HANDLER,
                'put_templates': PUT_TEMPLATES,
                'delete_handler': DELETE_HANDLER,
                'delete_templates': DELETE_TEMPLATES,
                'patch_handler': PATCH_HANDLER,
                'patch_templates': PATCH_TEMPLATES,
                'options_handler': OPTIONS_HANDLER,
                'options_templates': OPTIONS_TEMPLATES,
                'error_handler': ERROR_HANDLER,
                'scoped': ROUTES,
            },
            'logging': {
                'options': LOGGING_OPTIONS,
                'callbacks': LOGGING_CALLBACK,
                'scoped_options': LOGGING_SCOPED_OPTIONS,
                'scoped_callbacks': LOGGING_SCOPED_CALLBACKS,
            }
        }

    def get_default_instance(self):
        if self.instances:
            return self.instances[0]
        return None


def register_global_resource(name, factory, *, replace=False):
    """Register a cross-process shared resource."""
    return global_state.register(name, factory, replace=replace)


def get_global_resource(name):
    """Fetch a previously registered shared resource."""
    return global_state.get(name)


def _export_global_resources():
    return global_state.export()


def _import_global_resources(resources):
    return global_state.import_resources(resources)


def _describe_handler(func):
    module = getattr(func, '__module__', None)
    qualname = getattr(func, '__qualname__', None)
    if module and qualname and '<locals>' not in qualname:
        return {'kind': 'module', 'module': module, 'qualname': qualname}
    return {'kind': 'blueprint', 'data': CallableBlueprint.from_callable(func)}


def _load_handler(descriptor):
    kind = descriptor.get('kind', 'module')
    if kind == 'module':
        module_name = descriptor['module']
        qualname = descriptor['qualname']
        module = importlib.import_module(module_name)
        target = module
        for part in qualname.split('.'):
            target = getattr(target, part)
        return target
    if kind == 'blueprint':
        blueprint = descriptor['data']
        if isinstance(blueprint, CallableBlueprint):
            return blueprint.instantiate()
        raise ValueError('Invalid blueprint payload.')
    raise ValueError(f'Unknown handler descriptor kind {kind!r}.')


def _create_metrics_resource(manager):
    store = manager.dict({'header': 0, 'body': 0, 'handler': 0})
    lock = manager.RLock()
    return {'store': store, 'lock': lock}


def _ensure_metrics_shared_store():
    try:
        resource = get_global_resource('bbws.metrics')
    except KeyError:
        resource = register_global_resource('bbws.metrics', _create_metrics_resource)
    metrics_module.attach_store(resource['store'], resource.get('lock'))


def _export_handler_map(mapping):
    entries = []
    for route, data in mapping.items():
        if not data:
            continue
        func, mime_type = data
        entries.append({
            'route': route,
            'mime_type': mime_type,
            'handler': _describe_handler(func),
        })
    return entries


def _export_template_list(templates):
    exported = []
    for template in templates:
        if template.handler is None:
            continue
        exported.append({
            'template': getattr(template, 'template', template.path_template),
            'mime_type': template.type,
            'handler': _describe_handler(template.handler),
        })
    return exported


def _export_routes(routes):
    exported = {}
    for method, data in routes.items():
        method_static = []
        for scope, path_map in data.get('static', {}).items():
            for path, entry in path_map.items():
                handler = entry.get('handler')
                if handler is None:
                    continue
                method_static.append({
                    'scope': scope,
                    'path': path,
                    'mime_type': entry.get('type'),
                    'handler': _describe_handler(handler),
                })
        method_templates = []
        for entry in data.get('templates', []):
            handler = entry.get('handler')
            template = entry.get('template')
            if handler is None or template is None:
                continue
            method_templates.append({
                'ip': entry.get('ip'),
                'port': entry.get('port'),
                'domain': entry.get('domain'),
                'template': getattr(template, 'template', template.path_template),
                'mime_type': entry.get('type'),
                'handler': _describe_handler(handler),
            })
        exported[method] = {'static': method_static, 'templates': method_templates}
    return exported


def _build_runtime_snapshot():
    return {
        'pages': _export_handler_map(PAGES),
        'post_handler': _export_handler_map(POST_HANDLER),
        'put_handler': _export_handler_map(PUT_HANDLER),
        'delete_handler': _export_handler_map(DELETE_HANDLER),
        'patch_handler': _export_handler_map(PATCH_HANDLER),
        'options_handler': _export_handler_map(OPTIONS_HANDLER),
        'error_handler': [
            {
                'status': status,
                'mime_type': data[1],
                'handler': _describe_handler(data[0]),
            }
            for status, data in ERROR_HANDLER.items()
        ],
        'get_templates': _export_template_list(GET_TEMPLATES),
        'post_templates': _export_template_list(POST_TEMPLATES),
        'put_templates': _export_template_list(PUT_TEMPLATES),
        'delete_templates': _export_template_list(DELETE_TEMPLATES),
        'patch_templates': _export_template_list(PATCH_TEMPLATES),
        'options_templates': _export_template_list(OPTIONS_TEMPLATES),
        'routes': _export_routes(ROUTES),
        'cors': dict(CORS_SETTINGS),
    }


def _instantiate_handler(entry):
    handler = _load_handler(entry['handler'])
    mime_type = entry['mime_type']
    return handler, mime_type


def _apply_runtime_snapshot(snapshot):
    def _load_templates(target, entries):
        target[:] = []
        for entry in entries:
            handler = _load_handler(entry['handler'])
            template = UrlTemplate(entry['template'])
            template.handler = handler
            template.type = entry['mime_type']
            target.append(template)

    def _load_handler_map(target, entries):
        target.clear()
        for entry in entries:
            handler, mime_type = _instantiate_handler(entry)
            target[entry['route']] = [handler, mime_type]

    _load_handler_map(PAGES, snapshot.get('pages', []))
    _load_handler_map(POST_HANDLER, snapshot.get('post_handler', []))
    _load_handler_map(PUT_HANDLER, snapshot.get('put_handler', []))
    _load_handler_map(DELETE_HANDLER, snapshot.get('delete_handler', []))
    _load_handler_map(PATCH_HANDLER, snapshot.get('patch_handler', []))
    _load_handler_map(OPTIONS_HANDLER, snapshot.get('options_handler', []))

    ERROR_HANDLER.clear()
    for entry in snapshot.get('error_handler', []):
        handler = _load_handler(entry['handler'])
        ERROR_HANDLER[entry['status']] = [handler, entry['mime_type']]

    _load_templates(GET_TEMPLATES, snapshot.get('get_templates', []))
    _load_templates(POST_TEMPLATES, snapshot.get('post_templates', []))
    _load_templates(PUT_TEMPLATES, snapshot.get('put_templates', []))
    _load_templates(DELETE_TEMPLATES, snapshot.get('delete_templates', []))
    _load_templates(PATCH_TEMPLATES, snapshot.get('patch_templates', []))
    _load_templates(OPTIONS_TEMPLATES, snapshot.get('options_templates', []))

    for method, data in snapshot.get('routes', {}).items():
        method_entry = ROUTES.setdefault(method, {'static': {}, 'templates': []})
        static_map = {}
        for entry in data.get('static', []):
            handler, mime_type = _instantiate_handler(entry)
            scope = tuple(entry['scope'])
            path_map = static_map.setdefault(scope, {})
            path_map[entry['path']] = {'handler': handler, 'type': mime_type}
        method_entry['static'] = static_map
        templates = []
        for entry in data.get('templates', []):
            handler, mime_type = _instantiate_handler(entry)
            template = UrlTemplate(entry['template'])
            template.handler = handler
            template.type = mime_type
            templates.append({
                'ip': entry.get('ip'),
                'port': entry.get('port'),
                'domain': entry.get('domain'),
                'template': template,
                'handler': handler,
                'type': mime_type,
            })
        method_entry['templates'] = templates

    CORS_SETTINGS.clear()
    CORS_SETTINGS.update(snapshot.get('cors', {}))


def create_ssl_context(cert_path, key_path):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=cert_path, keyfile=key_path)
    return context


def _ensure_manager():
    global SERVER_MANAGER
    if SERVER_MANAGER is None:
        SERVER_MANAGER = ServerManager(CONFIG)
    return SERVER_MANAGER


def servlet(conn, addr, worker_state, server_instance=None):
    instance = server_instance
    if instance is None:
        manager = _ensure_manager()
        instance = manager.get_default_instance()
        if instance is None:
            log('[THREADING] No server instance available for servlet.', log_lvl='debug')
            return
    keep_alive_timeout = getattr(instance, 'keep_alive_timeout', KEEP_ALIVE_TIMEOUT)
    keep_alive_max_requests = getattr(instance, 'keep_alive_max_requests', KEEP_ALIVE_MAX_REQUESTS)
    header_timeout = getattr(instance, 'header_timeout', HEADER_TIMEOUT)
    body_min_rate = getattr(instance, 'body_min_rate', BODY_MIN_RATE_BYTES_PER_SEC)
    handler_timeout = getattr(instance, 'handler_timeout', HANDLER_TIMEOUT)
    try:
        while worker_state.is_set():
            log(f'[THREADING] thread {current_thread().ident} listens now.', log_lvl='debug')
            try:
                message_factory = HTTP_Message_Factory(
                    conn,
                    addr,
                    PAGES,
                    GET_TEMPLATES,
                    POST_HANDLER,
                    POST_TEMPLATES,
                    PUT_HANDLER,
                    PUT_TEMPLATES,
                    DELETE_HANDLER,
                    DELETE_TEMPLATES,
                    PATCH_HANDLER,
                    PATCH_TEMPLATES,
                    OPTIONS_HANDLER,
                    OPTIONS_TEMPLATES,
                    ERROR_HANDLER,
                    routes=ROUTES,
                    server_instance=instance,
                    max_header_size=CONFIG.MAX_HEADER_SIZE,
                    max_body_size=CONFIG.MAX_BODY_SIZE,
                    cors_settings=CORS_SETTINGS,
                    header_timeout=header_timeout,
                    body_min_rate=body_min_rate,
                    handler_timeout=handler_timeout,
                    max_url_length=CONFIG.MAX_URL_LENGTH,
                    handler_signal=getattr(worker_state, 'handler_signal', None),
                    stream_max_chunk_size=getattr(instance, 'stream_max_chunk_size', None),
                    stream_max_total_bytes=getattr(instance, 'stream_max_total_bytes', None),
                    stream_max_duration=getattr(instance, 'stream_max_duration', None),
                    stream_idle_timeout=getattr(instance, 'stream_idle_timeout', None),
                )
                if getattr(message_factory, 'aborted', False):
                    log(f'[THREADING] thread {current_thread().ident} aborts due to closed client connection.', log_lvl='debug')
                    break
                if message_factory.stay_alive:
                    current_count = getattr(worker_state, 'request_count', 0)
                    next_count = current_count + 1
                    max_requests = keep_alive_max_requests
                    if max_requests > 0 and next_count >= max_requests:
                        message_factory.stay_alive = False
                        worker_state.request_count = max_requests
                    else:
                        worker_state.request_count = next_count
                        remaining = (max_requests - next_count) if max_requests > 0 else None
                        message_factory.keep_alive_policy = {
                            'timeout': keep_alive_timeout,
                            'remaining': remaining
                        }
                if not hasattr(message_factory, 'response_message'):
                    log(f'[THREADING] Factory init failed, closing thread {current_thread().ident}.', log_lvl='debug')
                    break
                should_log_response = bool(
                    LOGGING_OPTIONS.get('response')
                    or LOGGING_CALLBACK
                    or LOGGING_SCOPED_OPTIONS
                    or LOGGING_SCOPED_CALLBACKS
                )
                if getattr(message_factory, 'is_streaming', lambda: False)():
                    message_factory.send_streaming_response(conn, log_response=should_log_response)
                else:
                    resp = message_factory.get_message()
                    conn.sendall(resp)

                    if should_log_response:
                        header, _, body = resp.partition(b'\r\n\r\n')
                        body_length = len(body)
                        preview = body
                        truncated = False
                        if body_length > RESPONSE_LOG_PREVIEW_BYTES:
                            preview = body[:RESPONSE_LOG_PREVIEW_BYTES]
                            truncated = True
                        preview_text = preview.decode('utf-8', errors='replace')
                        summary = f'[body length: {body_length} bytes{"; truncated" if truncated else ""}]'
                        log(
                            '\n\nRESPONSE:',
                            str(header, 'utf-8'),
                            preview_text if preview_text else '',
                            summary,
                            '\n',
                            log_lvl='response',
                            sep='\n',
                            scope=message_factory.scope
                        )

                if not message_factory.stay_alive:
                    log(f'[THREADING] thread {current_thread().ident} closes because stay_alive is set to False', log_lvl='debug')
                    break
            except TimeoutError:
                log(f'[THREADING] thread {current_thread().ident} closes due to a timeout error.', log_lvl='debug')
                break
            except Exception as err:
                log(f'[THREADING] thread {current_thread().ident} closes due to an error: "{err}"', log_lvl='debug')
                traceback.print_exc()
                break
    finally:
        try:
            conn.settimeout(1.0)
            conn.close()
        except Exception as e:
            log(f'[THREADING] thread {current_thread().ident} encountered an error while closing connection: {e}', log_lvl='debug')


def main(server=None, state=None, server_config=None):
    manager = _ensure_manager()
    if server is None:
        manager.start()
        return manager
    settings = CONFIG.SERVERS[0] if not server_config else server_config
    instance = ServerInstance(manager, settings)
    instance.server_socket = server
    instance.state = state if state else Event()
    instance.state.set()
    instance.bound_ip = server.getsockname()[0]
    instance.port = server.getsockname()[1]
    try:
        server.settimeout(DEFAULT_ACCEPT_TIMEOUT)
    except Exception:
        pass
    if instance.ssl_enabled:
        log('[SERVER] Existing socket provided, SSL settings ignored.', log_lvl='debug')
    instance.thread = Thread(target=instance._accept_loop, daemon=True)
    instance.thread.start()
    manager.instances.append(instance)
    return instance


def shutdown_server(server=None, server_thread=None, server_state=None):
    manager = _ensure_manager()
    manager.shutdown()
    print('[SERVER] Closed...')


def start():
    manager = _ensure_manager()
    manager.start()
    try:
        while True:
            try:
                state = input()
            except EOFError:
                state = ''
            state = state.strip().lower()
            if state in {'quit', 'q', 'exit', 'e', 'stop'}:
                manager.shutdown()
                break
            if not state:
                continue
            print('[SERVER]', f'Unknown command "{state}". Type q/quit/exit to stop.')
    except KeyboardInterrupt:
        manager.shutdown()
        os._exit(0)


def schedule_task(func, interval):
    manager = _ensure_manager()
    return manager.register_task(func, interval)
