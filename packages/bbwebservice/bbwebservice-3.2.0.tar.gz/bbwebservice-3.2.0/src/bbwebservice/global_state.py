from __future__ import annotations

from multiprocessing import Manager
from threading import RLock
from typing import Callable, Dict

_MANAGER = None
_RESOURCES: Dict[str, object] = {}
_LOCK = RLock()


def _ensure_manager():
    global _MANAGER
    if _MANAGER is None:
        _MANAGER = Manager()
    return _MANAGER


def register(name: str, factory: Callable[[Manager], object], *, replace: bool = False):
    if not callable(factory):
        raise TypeError('factory must be callable.')
    with _LOCK:
        if not replace and name in _RESOURCES:
            raise ValueError(f'Resource "{name}" already registered.')
        manager = _ensure_manager()
        resource = factory(manager)
        _RESOURCES[name] = resource
        return resource


def get(name: str):
    with _LOCK:
        if name not in _RESOURCES:
            raise KeyError(f'Resource "{name}" is not registered.')
        return _RESOURCES[name]


def export() -> Dict[str, object]:
    with _LOCK:
        return dict(_RESOURCES)


def import_resources(resources: Dict[str, object]):
    with _LOCK:
        _RESOURCES.clear()
        _RESOURCES.update(resources)
