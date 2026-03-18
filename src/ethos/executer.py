import ctypes
import json
import os
import platform
import sys
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

traits_path = Path.home() / ".ethos" / "traits"
if not traits_path.exists():
    traits_path.mkdir(parents=True, exist_ok=True)
hard_traits_path = traits_path / "hard_traits"
hard_traits_path.mkdir(parents=True, exist_ok=True)


def create_enviroment():
    env = {}
    list_traits = os.listdir(hard_traits_path)
    for i in list_traits:
        if not (hard_traits_path / i).is_dir():
            continue
        manifest_file = hard_traits_path / i / "manifest.json"
        if not manifest_file.exists():
            print(
                f"Warning: Trait {i} does not have a manifest.json file. Failed to load it. Skipping...."
            )
            continue
        with open(manifest_file, "r") as f:
            try:
                manifest = json.load(f)
            except:
                print(
                    f"Warning: Trait {i} manifest.json file is invalid and does not contains proper content, skipping it...."
                )
                continue
        binary_path = manifest.get("binary")
        if not (hard_traits_path / i / binary_path).exists():
            print(
                f"Warning: Trait {i} binary path defined in manifest.json is invalid, no file is found at that path. Failed to load it.Skipping...."
            )
            continue
        binary = ctypes.CDLL(str(hard_traits_path / i / binary_path))
        if not "functions" in manifest:
            print(
                f"Warning: Trait {i} manifest.json does not have functions key defined,failed to load trait {i}. Skipping it...."
            )
            continue
        for j in manifest["functions"]:
            func_data = manifest["functions"][j]
            c_func = getattr(binary, j)
            try:
                c_func.restype = ctypes_map[func_data["return"]]
                c_func.argtypes = [ctypes_map[arg] for arg in func_data["args"]]
            except KeyError:
                print(
                    f"Warning: In trait {i} there is a function named {j} of which types are not correctly written in manifest.json, skipping loading it...."
                )
                continue

        env[i] = binary

    return env


def run(python_code, memory_box=None):
    sys.path.append(str(traits_path))
    if not python_code or python_code == "":
        return
    if memory_box == None:
        memory_box = create_enviroment()
    try:
        exec(python_code, memory_box)
    except Exception as e:
        print("Ethos Runtime Error:", e)
