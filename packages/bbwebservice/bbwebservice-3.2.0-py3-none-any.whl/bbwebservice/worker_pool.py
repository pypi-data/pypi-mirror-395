from __future__ import annotations

import itertools
import math
import queue
import socket
import ssl
import threading
import time
from dataclasses import dataclass
from multiprocessing import get_context, connection as mp_connection
from multiprocessing.connection import Connection
from multiprocessing.reduction import send_handle, recv_handle
from typing import Any, Dict, Optional

from . import metrics as metrics_module
from .http_parser import log

_SSL_CONTEXT_CACHE: Dict[tuple, ssl.SSLContext] = {}
_SSL_CONTEXT_LOCK = threading.Lock()


@dataclass
class TaskRecord:
    task_id: int
    worker_id: int
    instance: Any
    handle: dict


class ProcessWorker:
    def __init__(self, ctx, worker_id: int, snapshot, shared_resources, threads_per_process: int):
        self.ctx = ctx
        self.worker_id = worker_id
        self.snapshot = snapshot
        self.shared_resources = shared_resources
        self.threads_per_process = max(1, threads_per_process)
        self.parent_conn: Connection
        self.child_conn: Connection
        self.parent_conn, self.child_conn = ctx.Pipe()
        self.process = None

    def start(self):
        if self.process and self.process.is_alive():
            return
        self.process = self.ctx.Process(
            target=_worker_main,
            args=(
                self.worker_id,
                self.child_conn,
                self.snapshot,
                self.shared_resources,
                self.threads_per_process,
            ),
            daemon=True,
        )
        self.process.start()

    def restart(self):
        self.stop()
        self.parent_conn, self.child_conn = self.ctx.Pipe()
        self.start()

    def stop(self):
        if self.process and self.process.is_alive():
            try:
                self.parent_conn.send({'cmd': 'STOP'})
            except Exception:
                pass
            self.process.join(timeout=1)
        if self.process and self.process.is_alive():
            self.process.terminate()
            self.process.join(timeout=1)
        self.process = None

    def send_task(self, task_id: int, conn: socket.socket, addr, server_payload):
        if not self.process or not self.process.is_alive():
            raise RuntimeError('Worker process not available.')
        message = {
            'cmd': 'START',
            'task_id': task_id,
            'addr': addr,
            'server': server_payload,
            'socket_info': {
                'family': conn.family,
                'type': conn.type,
                'proto': conn.proto,
            }
        }
        self.parent_conn.send(message)
        send_handle(self.parent_conn, conn.fileno(), self.process.pid)


class ProcessWorkerPool:
    def __init__(self, config, snapshot_builder, resource_exporter):
        self.config = config
        self.snapshot_builder = snapshot_builder
        self.resource_exporter = resource_exporter
        self.ctx = get_context('spawn')
        self.worker_count = max(1, getattr(config, 'WORKER_PROCESSES', 1))
        self.worker_slots = max(1, getattr(config, 'MAX_THREADS_PER_PROCESS', getattr(config, 'MAX_THREADS', 1)))
        self.slot_wait_timeout = 0.05
        configured_threshold = getattr(config, 'WORKER_TIMEOUT_THRESHOLD', 0.5)
        if configured_threshold >= 1:
            self.worker_timeout_threshold = math.ceil(configured_threshold)
        else:
            ratio = configured_threshold if configured_threshold > 0 else 0.5
            self.worker_timeout_threshold = max(1, math.ceil(self.worker_slots * ratio))
        self.workers: list[ProcessWorker] = []
        self.available = queue.Queue()
        self.task_seq = itertools.count(1)
        self.tasks: Dict[int, TaskRecord] = {}
        self.lock = threading.Lock()
        self.running = False
        self.listener_thread = None
        self.listener_stop = threading.Event()
        self.conn_map: Dict[Connection, int] = {}
        self.worker_timeout_counts: Dict[int, int] = {}
        self.worker_draining: set[int] = set()
        self.worker_capacity: Dict[int, int] = {}

    def start(self):
        if self.running:
            return
        snapshot = self.snapshot_builder()
        shared_resources = self.resource_exporter()
        self.available = queue.Queue()
        self.conn_map = {}
        with self.lock:
            self.tasks.clear()
        self.workers = []
        for worker_id in range(self.worker_count):
            worker = ProcessWorker(
                self.ctx,
                worker_id,
                snapshot,
                shared_resources,
                self.worker_slots,
            )
            worker.start()
            self.workers.append(worker)
            self.worker_timeout_counts[worker_id] = 0
            self._prime_worker_slots(worker_id)
            self.conn_map[worker.parent_conn] = worker_id
        self.running = True
        self.listener_stop.clear()
        self.listener_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listener_thread.start()

    def _prime_worker_slots(self, worker_id):
        if worker_id in self.worker_draining:
            return
        with self.lock:
            self.worker_capacity[worker_id] = self.worker_slots
        self.available.put(worker_id)

    def _acquire_worker_slot(self):
        deadline = time.monotonic() + self.slot_wait_timeout
        while True:
            timeout = max(0.0, deadline - time.monotonic())
            if timeout == 0:
                raise queue.Empty
            try:
                worker_id = self.available.get(timeout=timeout)
            except queue.Empty:
                raise
            if worker_id in self.worker_draining:
                continue
            worker = self.workers[worker_id]
            if not worker.process or not worker.process.is_alive():
                continue
            with self.lock:
                capacity = self.worker_capacity.get(worker_id, self.worker_slots)
                if capacity <= 0:
                    continue
                self.worker_capacity[worker_id] = capacity - 1
                remaining = self.worker_capacity[worker_id]
            if remaining > 0:
                self.available.put(worker_id)
            return worker_id

    def _release_worker_slot(self, worker_id):
        if worker_id in self.worker_draining:
            with self.lock:
                self.worker_capacity[worker_id] = 0
            return
        with self.lock:
            max_slots = self.worker_slots
            current = self.worker_capacity.get(worker_id, max_slots)
            if current >= max_slots:
                return
            new_value = current + 1
            self.worker_capacity[worker_id] = new_value
            if new_value == 1:
                self.available.put(worker_id)

    def shutdown(self):
        if not self.running:
            return
        self.listener_stop.set()
        if self.listener_thread:
            self.listener_thread.join(timeout=1)
        with self.lock:
            tasks = list(self.tasks.items())
            self.tasks.clear()
        for _, record in tasks:
            self._finalize_instance_handle(record)
        for worker in self.workers:
            worker.stop()
        self.workers = []
        self.conn_map = {}
        self.running = False

    def dispatch_connection(self, instance, conn: socket.socket, addr, handle) -> bool:
        try:
            worker_id = self._acquire_worker_slot()
        except queue.Empty:
            return False
        worker = self.workers[worker_id]
        task_id = next(self.task_seq)
        server_payload = instance.build_dispatch_payload()
        record = TaskRecord(
            task_id=task_id,
            worker_id=worker_id,
            instance=instance,
            handle=handle,
        )
        with self.lock:
            self.tasks[task_id] = record
        try:
            worker.send_task(task_id, conn, addr, server_payload)
        except Exception:
            with self.lock:
                self.tasks.pop(task_id, None)
            self._release_worker_slot(worker_id)
            raise
        finally:
            try:
                conn.close()
            except Exception:
                pass
        return True

    def _listen_loop(self):
        while not self.listener_stop.is_set():
            conns = [worker.parent_conn for worker in self.workers if worker.process and worker.process.is_alive()]
            if not conns:
                time.sleep(0.05)
                continue
            ready = []
            try:
                ready = mp_connection.wait(conns, timeout=0.1)
            except Exception:
                continue
            for conn in ready:
                worker_id = self._resolve_worker_id(conn)
                try:
                    message = conn.recv()
                except EOFError:
                    if conn in self.conn_map:
                        self.conn_map.pop(conn, None)
                    self._handle_worker_exit(worker_id)
                    continue
                cmd = message.get('cmd')
                task_id = message.get('task_id')
                if cmd == 'DONE':
                    self._complete_task(task_id)
                elif cmd == 'ERROR':
                    self._complete_task(task_id, error=message.get('error'))
                elif cmd == 'TIMEOUT':
                    self._handle_timeout_notification(task_id)

    def _complete_task(self, task_id, error=None):
        with self.lock:
            record = self.tasks.pop(task_id, None)
        if not record:
            return
        self._finalize_instance_handle(record)
        self._release_worker_slot(record.worker_id)
        self._maybe_shutdown_drained_worker(record.worker_id)

    def _handle_timeout_notification(self, task_id):
        with self.lock:
            record = self.tasks.pop(task_id, None)
        if not record:
            return
        metrics_module.record_timeout('handler')
        self._finalize_instance_handle(record)
        self._release_worker_slot(record.worker_id)
        self._track_worker_timeout(record.worker_id)
        self._maybe_shutdown_drained_worker(record.worker_id)

    def _handle_worker_exit(self, worker_id):
        if worker_id is None or not self.running:
            return
        self.worker_draining.discard(worker_id)
        self.worker_timeout_counts[worker_id] = 0
        pending = []
        with self.lock:
            for task_id, record in list(self.tasks.items()):
                if record.worker_id == worker_id:
                    pending.append(record)
                    self.tasks.pop(task_id, None)
        for record in pending:
            self._finalize_instance_handle(record)
            self._release_worker_slot(record.worker_id)
            self._maybe_shutdown_drained_worker(record.worker_id)
        self._restart_worker(worker_id)
        self._prime_worker_slots(worker_id)

    def _restart_worker(self, worker_id):
        worker = self.workers[worker_id]
        old_conn = worker.parent_conn
        worker.restart()
        self.conn_map.pop(old_conn, None)
        self.conn_map[worker.parent_conn] = worker_id

    def _finalize_instance_handle(self, record: TaskRecord):
        try:
            record.instance._finalize_handle(record.handle)
        except Exception:
            pass

    def _resolve_worker_id(self, conn):
        worker_id = self.conn_map.get(conn)
        if worker_id is not None:
            return worker_id
        for worker in self.workers:
            if worker.parent_conn == conn:
                return worker.worker_id
        return None

    def _track_worker_timeout(self, worker_id):
        if worker_id is None:
            return
        count = self.worker_timeout_counts.get(worker_id, 0) + 1
        self.worker_timeout_counts[worker_id] = count
        if count >= self.worker_timeout_threshold:
            self._begin_worker_drain(worker_id)

    def _begin_worker_drain(self, worker_id):
        if worker_id in self.worker_draining:
            return
        self.worker_draining.add(worker_id)
        with self.lock:
            self.worker_capacity[worker_id] = 0
        self._maybe_shutdown_drained_worker(worker_id)

    def _has_pending_tasks(self, worker_id):
        with self.lock:
            for record in self.tasks.values():
                if record.worker_id == worker_id:
                    return True
        return False

    def _maybe_shutdown_drained_worker(self, worker_id):
        if worker_id not in self.worker_draining:
            return
        if self._has_pending_tasks(worker_id):
            return
        self.worker_draining.discard(worker_id)
        self.worker_timeout_counts[worker_id] = 0
        self._restart_worker(worker_id)
        self._prime_worker_slots(worker_id)


def _worker_main(worker_id, control_conn, snapshot, shared_resources, threads_per_process):
    from . import core as core_module
    from . import metrics as metrics_module
    core_module._apply_runtime_snapshot(snapshot)
    core_module._import_global_resources(shared_resources)
    try:
        metrics_resource = core_module.get_global_resource('bbws.metrics')
        metrics_module.attach_store(metrics_resource['store'], metrics_resource.get('lock'))
    except Exception:
        pass
    send_lock = threading.Lock()
    task_queue: queue.Queue = queue.Queue()
    threads = []

    def _worker_loop():
        while True:
            item = task_queue.get()
            if item is None:
                break
            task_id, conn, addr, server_payload = item
            try:
                _serve_connection(
                    conn,
                    addr,
                    server_payload,
                    core_module,
                    control_conn,
                    task_id,
                    send_lock=send_lock,
                )
                _send_control(control_conn, {'cmd': 'DONE', 'task_id': task_id}, send_lock)
            except Exception as exc:
                _send_control(
                    control_conn,
                    {'cmd': 'ERROR', 'task_id': task_id, 'error': str(exc)},
                    send_lock,
                )

    thread_count = max(1, threads_per_process)
    for _ in range(thread_count):
        thread = threading.Thread(target=_worker_loop, daemon=True)
        thread.start()
        threads.append(thread)

    try:
        while True:
            try:
                message = control_conn.recv()
            except EOFError:
                break
            cmd = message.get('cmd')
            if cmd == 'STOP':
                break
            if cmd != 'START':
                continue
            task_id = message['task_id']
            socket_info = message['socket_info']
            addr = message['addr']
            server_payload = message['server']
            try:
                conn = _receive_socket(control_conn, socket_info)
            except Exception as exc:
                _send_control(
                    control_conn,
                    {'cmd': 'ERROR', 'task_id': task_id, 'error': str(exc)},
                    send_lock,
                )
                continue
            task_queue.put((task_id, conn, addr, server_payload))
    finally:
        for _ in threads:
            task_queue.put(None)
        for thread in threads:
            thread.join(timeout=0.5)

def _send_control(control_conn, message, lock=None):
    try:
        if lock:
            with lock:
                control_conn.send(message)
        else:
            control_conn.send(message)
    except Exception as exc:
        log(f'[WORKER_POOL] failed to send control message: {exc}', log_lvl='debug')


def _receive_socket(control_conn, socket_info):
    handle = recv_handle(control_conn)
    family = socket_info['family']
    sock_type = socket_info['type']
    proto = socket_info['proto']
    dup = socket.socket(family, sock_type, proto, fileno=handle)
    return dup


def _prepare_connection(connection, payload):
    if payload.get('ssl_enabled') and not payload.get('ssl_prepared'):
        return _wrap_ssl_connection(connection, payload)
    keep_alive = payload.get('keep_alive_timeout')
    if keep_alive:
        try:
            connection.settimeout(keep_alive)
        except Exception:
            pass
    return connection


def _context_cache_key(payload):
    sources = payload.get('cert_sources') or []
    if not sources:
        return (
            payload.get('cert_path'),
            payload.get('key_path'),
            tuple(),
        )
    key_parts = []
    for source in sources:
        key_parts.append((
            source.get('name'),
            source.get('cert_path'),
            source.get('key_path'),
            source.get('cert_mtime'),
            source.get('key_mtime'),
        ))
    return tuple(key_parts)


def _build_worker_ssl_context(payload):
    cert_path = payload.get('cert_path')
    key_path = payload.get('key_path')
    host_entries = payload.get('host_entries') or []
    fallback_cert = cert_path
    fallback_key = key_path
    if (not fallback_cert or not fallback_key) and host_entries:
        first = host_entries[0]
        fallback_cert = fallback_cert or first.get('cert_path')
        fallback_key = fallback_key or first.get('key_path')
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    if fallback_cert and fallback_key:
        context.load_cert_chain(certfile=fallback_cert, keyfile=fallback_key)
    sni_contexts = {}
    for entry in host_entries:
        host_name = entry.get('host')
        host_cert = entry.get('cert_path')
        host_key = entry.get('key_path')
        if not host_name or not host_cert or not host_key:
            continue
        host_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        host_context.load_cert_chain(certfile=host_cert, keyfile=host_key)
        sni_contexts[host_name] = host_context

    if sni_contexts:
        def _sni_callback(sock, server_name, ctx):
            selected = sni_contexts.get(server_name)
            if selected:
                sock.context = selected
        context.sni_callback = _sni_callback
    return context


def _get_ssl_context(payload):
    key = _context_cache_key(payload)
    with _SSL_CONTEXT_LOCK:
        cached = _SSL_CONTEXT_CACHE.get(key)
        if cached:
            return cached
        context = _build_worker_ssl_context(payload)
        _SSL_CONTEXT_CACHE[key] = context
        return context


def _wrap_ssl_connection(conn, payload):
    handshake_timeout = payload.get('handshake_timeout') or 5
    try:
        conn.settimeout(handshake_timeout)
    except Exception:
        pass
    try:
        context = _get_ssl_context(payload)
        wrapped = context.wrap_socket(conn, server_side=True)
        keep_alive = payload.get('keep_alive_timeout')
        if keep_alive:
            try:
                wrapped.settimeout(keep_alive)
            except Exception:
                pass
        return wrapped
    except Exception as exc:
        log(f'[WORKER_POOL] SSL wrap failed: {exc}', log_lvl='debug')
        try:
            conn.close()
        except Exception as close_err:
            log(f'[WORKER_POOL] closing failed after SSL error: {close_err}', log_lvl='debug')
        return None


def _serve_connection(connection, addr, server_payload, core_module, control_conn, task_id, *, send_lock=None):
    instance = _ServerContext(server_payload)
    prepared = _prepare_connection(connection, server_payload)
    if prepared is None:
        return
    timeout = server_payload.get('handler_timeout')
    controller = _TimeoutController(prepared, control_conn, task_id, timeout, send_lock=send_lock)
    worker_state = _WorkerState(instance, handler_signal=controller)
    try:
        core_module.servlet(prepared, addr, worker_state, server_instance=instance)
    finally:
        controller.stop()
        try:
            prepared.close()
        except Exception:
            pass


class _WorkerState:
    def __init__(self, server_instance, handler_signal=None):
        self._event = threading.Event()
        self._event.set()
        self.request_count = 0
        self.server_instance = server_instance
        self.handler_signal = handler_signal

    def is_set(self):
        return self._event.is_set()

    def set(self):
        self._event.set()

    def clear(self):
        self._event.clear()


class _ServerContext:
    def __init__(self, payload):
        self.__dict__.update(payload)

    def build_dispatch_payload(self):
        return self.__dict__


class _TimeoutController:
    def __init__(self, connection, control_conn, task_id, timeout, send_lock=None):
        self.connection = connection
        self.control_conn = control_conn
        self.task_id = task_id
        self.timeout = timeout if timeout and timeout > 0 else None
        self._finished = threading.Event()
        self._thread = None
        self._lock = threading.Lock()
        self._send_lock = send_lock
        self.timed_out = False

    def start(self):
        if not self.timeout:
            return
        with self._lock:
            if self._thread:
                return
            self._thread = threading.Thread(target=self._watchdog, daemon=True)
            self._thread.start()

    def end(self):
        if not self.timeout:
            return
        self._finished.set()

    def stop(self):
        if not self.timeout:
            return
        self._finished.set()
        thread = self._thread
        if thread and thread.is_alive():
            thread.join(timeout=0.05)

    def _watchdog(self):
        if self._finished.wait(self.timeout):
            return
        self._trigger_timeout()

    def _trigger_timeout(self):
        response = (
            b'HTTP/1.1 504 Gateway Timeout\r\n'
            b'Connection: close\r\n'
            b'Content-Length: 0\r\n\r\n'
        )
        self.timed_out = True
        try:
            self.connection.sendall(response)
        except Exception:
            pass
        try:
            self.connection.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        try:
            self.connection.close()
        except Exception:
            pass
        try:
            _send_control(self.control_conn, {'cmd': 'TIMEOUT', 'task_id': self.task_id}, self._send_lock)
        except Exception as exc:
            log(f'[WORKER_POOL] failed to report timeout: {exc}', log_lvl='debug')
