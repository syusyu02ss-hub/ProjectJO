"""Convert the approved artwork and embed ICO resources using Windows APIs."""
import ctypes
from ctypes import wintypes
from pathlib import Path
import struct

from PIL import Image


def prepare_icon(project):
    with Image.open(project / "game/images/app_icon.png") as image:
        image.convert("RGBA").save(
            project / "icon.ico", sizes=[(n, n) for n in (16, 24, 32, 48, 64, 128, 256)]
        )


def embed_icon(executable, icon):
    data = Path(icon).read_bytes()
    reserved, kind, count = struct.unpack_from("<HHH", data)
    assert reserved == 0 and kind == 1 and count > 0
    api = ctypes.WinDLL("kernel32", use_last_error=True)
    begin = api.BeginUpdateResourceW
    begin.argtypes = [wintypes.LPCWSTR, wintypes.BOOL]
    begin.restype = wintypes.HANDLE
    update = api.UpdateResourceW
    update.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.c_void_p,
                       wintypes.WORD, ctypes.c_void_p, wintypes.DWORD]
    update.restype = wintypes.BOOL
    end = api.EndUpdateResourceW
    end.argtypes = [wintypes.HANDLE, wintypes.BOOL]
    end.restype = wintypes.BOOL
    handle = begin(str(Path(executable).resolve()), False)
    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())
    group = struct.pack("<HHH", 0, 1, count)
    try:
        for index in range(count):
            entry = struct.unpack_from("<BBBBHHII", data, 6 + index * 16)
            width, height, colors, zero, planes, bits, size, offset = entry
            resource_id = index + 1
            payload = ctypes.create_string_buffer(data[offset:offset + size])
            if not update(handle, 3, resource_id, 0, payload, size):
                raise ctypes.WinError(ctypes.get_last_error())
            group += struct.pack("<BBBBHHIH", width, height, colors, zero,
                                 planes, bits, size, resource_id)
        payload = ctypes.create_string_buffer(group)
        if not update(handle, 14, 1, 0, payload, len(group)):
            raise ctypes.WinError(ctypes.get_last_error())
    except BaseException:
        end(handle, True)
        raise
    if not end(handle, False):
        raise ctypes.WinError(ctypes.get_last_error())


if __name__ == "__main__":
    prepare_icon(Path(__file__).resolve().parents[1])
