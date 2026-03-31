# Standard Library Shims

Ethos includes a stdlib shim (`stdlib_shim.py`) that forces Nuitka to bundle standard library modules into the compiled binary.

Without this, Nuitka's dead-code analysis would strip modules that Soft Traits load dynamically at runtime.

---

## Bundled Modules

| Module | Purpose |
|--------|---------|
| `hmac` | Keyed-hash message authentication |
| `hashlib` | MD5, SHA-1, SHA-256, etc. |
| `ssl` | TLS/SSL for sockets |
| `socket` | Low-level networking |
| `urllib.*` | URL handling (`request`, `parse`, `error`) |
| `http.*` | HTTP client/server (`client`, `server`, `cookies`, `cookiejar`) |
| `email.*` | Email parsing (`parser`, `message`) |
| `json` | JSON encode/decode |
| `xml.etree.ElementTree` | XML parsing |
| `sqlite3` | SQLite database |
| `base64` | Base64 encoding |
| `ctypes` | Foreign function interface (Hard Traits) |
| `math` | Math functions |
| `datetime` | Date/time types |
| `zipfile` | ZIP archives |
| `tarfile` | TAR archives |
| `threading` | Thread-based parallelism |
| `subprocess` | Spawn subprocesses |

---

## Why This Exists

Nuitka compiles to a standalone binary and only includes modules it can statically trace. Soft Traits are loaded from `~/.ethos/traits/` at runtime — Nuitka never sees their imports during compilation.

The shim is imported at compile time (so Nuitka includes the modules) but does nothing at runtime.

---

## Adding Modules

If a Soft Trait needs a stdlib module not listed above:

1. Add `import <module>` to `src/ethos/stdlib_shim.py`
2. Rebuild Ethos
3. Submit a PR if it's generally useful
