import ctypes
import json
import os
import sys
from functools import wraps
from pathlib import Path

ctypes_map = {
    "char": ctypes.c_char,
    "unsigned char": ctypes.c_ubyte,
    "wchar_t": ctypes.c_wchar,
    "short": ctypes.c_short,
    "unsigned short": ctypes.c_ushort,
    "int": ctypes.c_int,
    "unsigned int": ctypes.c_uint,
    "long": ctypes.c_long,
    "unsigned long": ctypes.c_ulong,
    "long long": ctypes.c_longlong,
    "unsigned long long": ctypes.c_ulonglong,
    "int8_t": ctypes.c_int8,
    "uint8_t": ctypes.c_uint8,
    "int16_t": ctypes.c_int16,
    "uint16_t": ctypes.c_uint16,
    "float": ctypes.c_float,
    "double": ctypes.c_double,
    "long double": ctypes.c_longdouble,
    "char *": ctypes.c_char_p,
    "wchar_t *": ctypes.c_wchar_p,
    "void *": ctypes.c_void_p,
    "pointer_to_int": ctypes.POINTER(ctypes.c_int),
    "size_t": ctypes.c_size_t,
    "ssize_t": ctypes.c_ssize_t,
    "bool": ctypes.c_bool,
    "void": None,
}

_BYTES_TYPES = {ctypes.c_char_p, ctypes.c_char}

traits_path = Path.home() / ".ethos" / "traits"
if not traits_path.exists():
    traits_path.mkdir(parents=True, exist_ok=True)
hard_traits_path = traits_path / "hard_traits"
hard_traits_path.mkdir(parents=True, exist_ok=True)


def _make_smart_wrapper(c_func, argtypes):
    @wraps(c_func)
    def wrapper(*args):
        coerced = []
        for arg, atype in zip(args, argtypes):
            if atype in _BYTES_TYPES and isinstance(arg, str):
                arg = arg.encode("utf-8")
            elif atype == ctypes.c_wchar_p and isinstance(arg, bytes):
                arg = arg.decode("utf-8")
            coerced.append(arg)
        result = c_func(*coerced)
        if isinstance(result, bytes):
            return result.decode("utf-8")
        return result

    return wrapper


def create_environment():
    env = {}
    list_traits = os.listdir(hard_traits_path)
    for i in list_traits:
        if not (hard_traits_path / i).is_dir():
            continue
        manifest_file = hard_traits_path / i / "manifest.json"
        if not manifest_file.exists():
            print(
                f"Warning: Trait {i} does not have a manifest.json file. Failed to load it. Skipping..."
            )
            continue
        with open(manifest_file, "r") as f:
            try:
                manifest = json.load(f)
            except:
                print(
                    f"Warning: Trait {i} manifest.json file is invalid and does not contain proper content. Skipping..."
                )
                continue
        binary_path = manifest.get("binary")
        if not (hard_traits_path / i / binary_path).exists():
            print(
                f"Warning: Trait {i} binary path defined in manifest.json is invalid, no file is found at that path. Failed to load it. Skipping..."
            )
            continue
        binary = ctypes.CDLL(str(hard_traits_path / i / binary_path))
        if "functions" not in manifest:
            print(
                f"Warning: Trait {i} manifest.json does not have functions key defined. Failed to load trait {i}. Skipping..."
            )
            continue
        for j in manifest["functions"]:
            func_data = manifest["functions"][j]
            c_func = getattr(binary, j)
            try:
                restype = ctypes_map[func_data["return"]]
                argtypes = [ctypes_map[arg] for arg in func_data["args"]]
                c_func.restype = restype
                c_func.argtypes = argtypes
            except KeyError:
                print(
                    f"Warning: In trait {i}, function {j} has incorrectly written types in manifest.json. Skipping..."
                )
                continue
            setattr(binary, j, _make_smart_wrapper(c_func, argtypes))
        env[i] = binary
    return env


def run(python_code, memory_box=None):
    sys.path.append(str(traits_path))
    if not python_code or python_code == "":
        return
    if memory_box is None:
        memory_box = create_environment()
    try:
        exec(python_code, memory_box)
    except Exception as e:
        print("Ethos Runtime Error:", e)
