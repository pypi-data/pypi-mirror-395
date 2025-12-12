from __future__ import annotations

import base64
import builtins
import importlib
import marshal
import pickle
import types
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

from types import SimpleNamespace


class CallableSerializationError(RuntimeError):
    """Raised when a handler cannot be serialized into a blueprint."""


def _b64_encode(data: bytes) -> str:
    return base64.b64encode(data).decode('ascii')


def _b64_decode(payload: str) -> bytes:
    return base64.b64decode(payload.encode('ascii'))


def _make_cell(value):
    def inner():
        return value
    return inner.__closure__[0]


def _import_attribute(module_name: str, qualname: str) -> Any:
    module = importlib.import_module(module_name)
    target = module
    for part in qualname.split('.'):
        if part == '<locals>':
            raise AttributeError('Cannot resolve local attribute.')
        target = getattr(target, part)
    return target


def _resolve_attribute_ref(value) -> Tuple[str, str] | None:
    module_name = getattr(value, '__module__', None)
    qualname = getattr(value, '__qualname__', None)
    if not module_name or not qualname or '<locals>' in qualname:
        return None
    try:
        attr = _import_attribute(module_name, qualname)
    except (ImportError, AttributeError):
        return None
    if attr is value:
        return (module_name, qualname)
    return None


def _serialize_sequence(items, converter):
    return [converter(item) for item in items]


def _serialize_mapping(mapping, key_converter, value_converter):
    return [[key_converter(key), value_converter(val)] for key, value in mapping.items()]


def serialize_value(value):
    if value is None or isinstance(value, (bool, int, float, str)):
        return {'kind': 'literal', 'value': value}
    if isinstance(value, bytes):
        return {'kind': 'bytes', 'value': _b64_encode(value)}
    if isinstance(value, Path):
        return {'kind': 'path', 'value': str(value)}
    if isinstance(value, SimpleNamespace):
        return {
            'kind': 'namespace',
            'items': {key: serialize_value(val) for key, val in value.__dict__.items()},
        }
    if isinstance(value, types.ModuleType):
        return {'kind': 'module', 'name': value.__name__}
    if isinstance(value, dict):
        return {
            'kind': 'dict',
            'items': _serialize_mapping(value, serialize_value, serialize_value),
        }
    if isinstance(value, (list, tuple)):
        return {
            'kind': 'sequence',
            'type': 'tuple' if isinstance(value, tuple) else 'list',
            'items': _serialize_sequence(value, serialize_value),
        }
    if isinstance(value, (set, frozenset)):
        return {
            'kind': 'set',
            'type': 'frozenset' if isinstance(value, frozenset) else 'set',
            'items': _serialize_sequence(list(value), serialize_value),
        }
    ref = _resolve_attribute_ref(value)
    if ref:
        return {'kind': 'attribute', 'module': ref[0], 'qualname': ref[1]}
    try:
        data = pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL)
        return {'kind': 'pickle', 'payload': _b64_encode(data)}
    except Exception as exc:  # pragma: no cover - safety path
        raise CallableSerializationError(f'Cannot serialize value {value!r}: {exc}') from exc


def deserialize_value(payload):
    kind = payload.get('kind')
    if kind == 'literal':
        return payload.get('value')
    if kind == 'bytes':
        return _b64_decode(payload['value'])
    if kind == 'path':
        return Path(payload['value'])
    if kind == 'namespace':
        return SimpleNamespace(**{key: deserialize_value(val) for key, val in payload['items'].items()})
    if kind == 'module':
        return importlib.import_module(payload['name'])
    if kind == 'dict':
        result = {}
        for key_payload, value_payload in payload['items']:
            result[deserialize_value(key_payload)] = deserialize_value(value_payload)
        return result
    if kind == 'sequence':
        items = [deserialize_value(item) for item in payload['items']]
        return tuple(items) if payload.get('type') == 'tuple' else items
    if kind == 'set':
        items = {deserialize_value(item) for item in payload['items']}
        return frozenset(items) if payload.get('type') == 'frozenset' else set(items)
    if kind == 'attribute':
        return _import_attribute(payload['module'], payload['qualname'])
    if kind == 'pickle':
        return pickle.loads(_b64_decode(payload['payload']))
    raise CallableSerializationError(f'Unknown serialized payload kind "{kind}".')


def _encode_optional_pickle(value):
    if value is None:
        return None
    data = pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL)
    return _b64_encode(data)


def _decode_optional_pickle(payload):
    if payload is None:
        return None
    return pickle.loads(_b64_decode(payload))


@dataclass(frozen=True)
class CallableBlueprint:
    """Serializable representation of a Python callable along with its globals/closures."""

    name: str
    qualname: str
    module: str | None
    code: str
    defaults: str | None
    kwdefaults: str | None
    globals_map: Dict[str, Dict[str, Any]]
    freevars: List[Tuple[str, Dict[str, Any]]] | None

    @classmethod
    def from_callable(cls, func):
        if not isinstance(func, types.FunctionType):
            raise CallableSerializationError(f'Unsupported callable type: {type(func)!r}')
        code_bytes = marshal.dumps(func.__code__)
        global_names = {name for name in func.__code__.co_names if name in func.__globals__ and name != '__builtins__'}
        globals_map = {name: serialize_value(func.__globals__[name]) for name in sorted(global_names)}
        freevars = None
        if func.__closure__:
            freevars = []
            for name, cell in zip(func.__code__.co_freevars, func.__closure__):
                freevars.append((name, serialize_value(cell.cell_contents)))
        return cls(
            name=func.__name__,
            qualname=getattr(func, '__qualname__', func.__name__),
            module=getattr(func, '__module__', None),
            code=_b64_encode(code_bytes),
            defaults=_encode_optional_pickle(func.__defaults__),
            kwdefaults=_encode_optional_pickle(func.__kwdefaults__),
            globals_map=globals_map,
            freevars=freevars,
        )

    def instantiate(self):
        namespace = {'__builtins__': builtins.__dict__}
        for name, payload in self.globals_map.items():
            namespace[name] = deserialize_value(payload)
        code_obj = marshal.loads(_b64_decode(self.code))
        defaults = _decode_optional_pickle(self.defaults)
        kwdefaults = _decode_optional_pickle(self.kwdefaults)
        closure = None
        if self.freevars:
            values = [deserialize_value(payload) for _, payload in self.freevars]
            closure = tuple(_make_cell(val) for val in values)
        func = types.FunctionType(code_obj, namespace, self.name, defaults, closure)
        func.__kwdefaults__ = kwdefaults
        func.__qualname__ = self.qualname
        if self.module:
            func.__module__ = self.module
        return func
