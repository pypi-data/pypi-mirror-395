import os
from pathlib import Path
from . import MAIN_PATH

_BASE_PATH = Path(MAIN_PATH).resolve()


def _resolve_path(path: str) -> Path:
    relative = path.lstrip('/\\')
    candidate = (_BASE_PATH / relative).resolve()
    try:
        candidate.relative_to(_BASE_PATH)
    except ValueError:
        raise ValueError('Requested asset is outside of the content directory.')
    return candidate


def load_bin_file_partial(path, start_byte, end_byte) -> bytes:
    if isinstance(path, Path):
        target = path
    else:
        target = _resolve_path(path)
    size = end_byte - start_byte
    if size <= 0:
        return b''
    buffer = bytearray()
    with target.open('rb') as file:
        file.seek(start_byte)
        remaining = size
        chunk_size = 64 * 1024
        while remaining > 0:
            chunk = file.read(min(chunk_size, remaining))
            if not chunk:
                break
            buffer.extend(chunk)
            remaining -= len(chunk)
    return bytes(buffer)


def get_file_size(path: str) -> int:
    try:
        target = _resolve_path(path)
        return target.stat().st_size
    except (FileNotFoundError, ValueError):
        return -1


class PartialContent:

    def __init__(self, path, default_size) -> None:
        self.path = path
        self.default_size = default_size
        self._resolved = None

    def _ensure_path(self) -> Path:
        if self._resolved is None:
            self._resolved = _resolve_path(self.path)
        return self._resolved

    def get_range(self, start, end) -> bytes:
        target = self._ensure_path()
        try:
            file_size = target.stat().st_size
        except FileNotFoundError:
            return b''
        if file_size <= 0 or start >= file_size:
            return b''
        if end is None:
            end = start + self.default_size - 1
        end = min(end, start + self.default_size - 1, file_size - 1)
        if end < start:
            return b''
        return load_bin_file_partial(target, start, end + 1)

    def get_size(self) -> int:
        try:
            return self._ensure_path().stat().st_size
        except FileNotFoundError:
            return -1

class Redirect:
    
    def __init__(self, path, status= None) -> None:
        self.path = path
        self.status = status 


class Dynamic:
    
    def __init__(self, content, mime_type, encoding='utf-8'):
        self.content = content
        self.mime_type = mime_type
        self.encoding = encoding

    def get_bytes(self):
        if isinstance(self.content, bytes):
            return self.content
        if isinstance(self.content, str):
            return self.content.encode(self.encoding)
        raise TypeError('Dynamic content must be bytes or str.')


class Response:
    
    def __init__(self, content=None, status=None, headers=None, mime_type=None):
        self.content = content
        self.status = status
        self.headers = headers or []
        self.mime_type = mime_type


class StreamResponse:

    def __init__(self, chunks, mime_type="application/octet-stream", status=200, headers=None, encoding='utf-8'):
        self.chunks = chunks
        self.mime_type = mime_type
        self.status = status
        self.headers = headers or []
        self.encoding = encoding


class SseEvent:

    def __init__(self, data: str, event: str | None = None) -> None:
        self.data = data
        self.event = event

    def to_bytes(self, encoding: str = 'utf-8') -> bytes:
        lines = []
        if self.event:
            lines.append(f'event: {self.event}')
        data_lines = str(self.data).split('\n')
        for line in data_lines:
            lines.append(f'data: {line}')
        payload = '\n'.join(lines) + '\n\n'
        return payload.encode(encoding)
