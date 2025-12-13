import os
import sys
import time
import platform
import ctypes as C
from pathlib import Path
from dataclasses import dataclass, fields
from enum import IntEnum, IntFlag
from typing import Callable, TypeVar


DIR = Path(__file__).parent

class Str_C(C.Structure):
    _fields_ = [
        ("data"  , C.c_char_p),
        ("length", C.c_uint32),
    ]

    def to_bytes(self) -> bytes:
        return C.string_at(self.data, self.length)

def to_str_c(s: str | bytes) -> Str_C:
    if isinstance(s, str):
        s = s.encode()
    return Str_C(s, len(s))

_lib = C.CDLL(str(DIR / "libcode_intelligence.so"))

SCAN_CALLBACK = C.CFUNCTYPE(None, C.c_void_p)
_lib.enqueue_scan_file.argtypes = [SCAN_CALLBACK, C.c_void_p, Str_C, C.c_uint64]
_lib.enqueue_scan_file.restype = None

class Definition_Link_C(C.Structure):
    _fields_ = [
        ("start_offset_in_utf8_text", C.c_uint32),
        ("end_offset_in_utf8_text"  , C.c_uint32),
        ("source_file"              , C.c_char_p),
        ("line_0_based"             , C.c_uint32),
        ("column_0_based"           , C.c_uint32),
    ]

FIND_CALLBACK = C.CFUNCTYPE(None, C.c_void_p, C.POINTER(Definition_Link_C), C.c_int, C.c_void_p)
_lib.enqueue_find_symbols_in_text.argtypes = [FIND_CALLBACK, C.c_void_p, Str_C, C.c_bool, C.c_bool, C.POINTER(Str_C), C.c_uint32]
_lib.enqueue_find_symbols_in_text.restype = None

_lib.enqueue_stop.argtypes = []
_lib.enqueue_stop.restype = None

_lib.enqueue_clear.argtypes = []
_lib.enqueue_clear.restype = None

_lib.start_workers.argtypes = []
_lib.start_workers.restype = None

_lib.get_pending_tasks_count.argtypes = []
_lib.get_pending_tasks_count.restype = C.c_uint64

_lib.free_memory.argtypes = [C.c_void_p]
_lib.free_memory.restype = None


T = TypeVar("T")


def positional_repr(cls: type) -> type:
    def __repr__(self):
        values = ', '.join(repr(getattr(self, f.name)) for f in fields(self))
        return f"{cls.__name__}({values})"
    cls.__repr__ = __repr__
    return cls


class Language(IntEnum):
    UNKNOWN    = 0
    PYTHON     = 1
    JAVASCRIPT = 2
    GOLANG     = 3
    PHP        = 4
    RUST       = 5
    CPP        = 6
    JAVA       = 7
    C_SHARP    = 8
    KOTLIN     = 9
    SWIFT      = 10
    DART       = 11
    R_LANG     = 12
    RUBY       = 13
    LUA        = 14


@dataclass
@positional_repr
class Definition_Link:
    start_offset_in_text: int = 0
    end_offset_in_text  : int = 0
    source_file         : str = ""
    line_0_based        : int = 0
    column_0_based      : int = 0

    @classmethod
    def from_c(cls, link: Definition_Link_C) -> "Definition_Link":
        return cls(
            start_offset_in_text=link.start_offset_in_utf8_text,
            end_offset_in_text=link.end_offset_in_utf8_text,
            source_file=link.source_file.decode('utf-8'),
            line_0_based=link.line_0_based,
            column_0_based=link.column_0_based,
        )


# Using ["..."] syntax to create a copy independant of
# whether any other library sets the signature for those functions.
Py_IncRef = C.pythonapi["Py_IncRef"]
Py_IncRef.argtypes = [C.py_object]
Py_IncRef.restype = None

Py_DecRef = C.pythonapi["Py_DecRef"]
Py_DecRef.argtypes = [C.py_object]
Py_DecRef.restype = None


# IMPORTANT: KEEP THIS ALIVE FOR GO THREAD WORKER
C_NO_CALLBACK = SCAN_CALLBACK(0)


def _wrap_data_ptr(tup: T) -> int:
    # MANUALLY INCREMENT THE REFERENCE COUNT
    # We are now responsible for its lifetime
    Py_IncRef(C.py_object(tup))

    return id(tup)


def _unwrap_data_ptr(data_ptr: int) -> T:
    assert data_ptr, "Received a NULL pointer"

    tup = C.cast(data_ptr, C.py_object).value

    # MANUALLY DECREMENT THE REFERENCE COUNT.
    # We are fulfilling our promise
    Py_DecRef(C.py_object(tup))

    return tup


def scan_file(file: str | Path, language: Language, callback: Callable[[T | None], None] | None = None, data: T | None = None) -> bool:
    if callback is None:
        c_callback, data_ptr = C_NO_CALLBACK, 0
    else:
        c_callback, data_ptr = C_AFTER_SCAN, _wrap_data_ptr((callback, data))

    # print(f"[PY] sending next request {file}")
    _lib.enqueue_scan_file(c_callback, data_ptr, to_str_c(os.fsencode(file)), language)

    # never drop the request (it would be a memory leak)
    return True


@SCAN_CALLBACK
def C_AFTER_SCAN(data_ptr: int) -> None:
    callback, data = _unwrap_data_ptr(data_ptr)
    assert callback is not None, "Don't feed youself NULL callbacks!"
    callback(data)


def find_symbols_in_text(text: str, callback: Callable[[T | None, list[Definition_Link]], None] | None = None, data: T | None = None, ignore_word_like: bool = False, sync: bool = False, first_look_at_these_files: list[Path|str] = []) -> bool:
    if callback is None:
        return True

    c_callback, data_ptr = C_AFTER_FIND, _wrap_data_ptr((callback, data))

    first_look_at_these_files_c = (Str_C * len(first_look_at_these_files))()
    for i, it in enumerate(first_look_at_these_files):
        first_look_at_these_files_c[i] = to_str_c(os.fsencode(it))

    # print("[PY] sending find_symbols_in_text")
    _lib.enqueue_find_symbols_in_text(c_callback, data_ptr, to_str_c(text), ignore_word_like, sync, first_look_at_these_files_c, len(first_look_at_these_files))

    # never drop the request (it would be a memory leak)
    return True


@FIND_CALLBACK
def C_AFTER_FIND(data_ptr: int, links_ptr: C.POINTER(Definition_Link_C), count: int, strings_handle: int) -> None:
    callback, data = _unwrap_data_ptr(data_ptr)
    try:
        assert callback is not None, "Don't feed youself NULL callbacks!"
        results = [Definition_Link()] * count
        for i in range(count):
            results[i] = Definition_Link.from_c(links_ptr[i])
        callback(data, results)
    finally:
        if links_ptr: _lib.free_memory(links_ptr)
        if strings_handle: _lib.free_memory(strings_handle)


def pending_tasks() -> int:
    return int(_lib.get_pending_tasks_count())


def init() -> None:
    _lib.start_workers()


def stop() -> None:
    _lib.enqueue_stop()


def clear() -> None:
    _lib.enqueue_clear()


def wait_for_callbacks_in_seconds(timeout_s: float, step_s: float = 0.15) -> bool:
    # print(f"[PY] Waiting for callbacks (~{timeout_s}s)...")
    deadline = time.time() + timeout_s
    while True:
        if pending_tasks() == 0:
            # print("[PY] All pending tasks have completed.")
            return True

        if time.time() >= deadline:
            print("[PY] Timeout reached.")
            return False

        # print(f"[PY] pending_tasks={pending_tasks()}")
        time.sleep(step_s)


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print("usage: python goober.py text folder...")
        exit(1)

    import atexit
    atexit.register(stop)

    def scan_callback(data: Path) -> None:
        print(f"[PY] {data}")

    def find_callback(data: tuple[str, str], links: list[Definition_Link]) -> None:
        text, label = data
        print(f"[PY] Callback for '{label}': Found {len(links)} symbols in text \"{text}\"")
        for res in links:
            matched_symbol = text[res.start_offset_in_text:res.end_offset_in_text]
            print(f"  '{matched_symbol}' -> {res.source_file}:{res.line_0_based}:{res.column_0_based}")

    for folder in sys.argv[2:]:
        path = Path(folder)
        if path.is_dir():
            for file in path.rglob("*.py"):
                scan_file(file, Language.PYTHON, scan_callback, file)
        else:
            scan_file(path, Language.PYTHON, scan_callback, path)

    text = sys.argv[1]
    find_symbols_in_text(text, find_callback, data=(text, "before"),
                         first_look_at_these_files=["hello.py", "yay.so"])

    print("[PY] WAIT, WAIT, WAIT!")
    wait_for_callbacks_in_seconds(20)

    find_symbols_in_text(text, find_callback, data=(text, "after"))

    wait_for_callbacks_in_seconds(1)
