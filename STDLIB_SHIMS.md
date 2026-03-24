# Standard Library Shims

Ethos ships a stdlib shim (`stdlib_shim.py`) that forces Nuitka to bundle a set of heavy standard library modules into the compiled binary. Without this, Nuitka's dead-code analysis would strip them out at compile time — and since Soft Traits are loaded dynamically at runtime, they'd fail to import anything that wasn't already baked in.

If a Soft Trait you install tries to use a module not in this list, it will likely get an `ImportError` at runtime.

---

## Bundled modules

| Module | What it covers |
|---|---|
| `hmac` | Keyed-hash message authentication |
| `hashlib` | MD5, SHA-1, SHA-256 and other hash functions |
| `ssl` | TLS/SSL wrapping for sockets |
| `socket` | Low-level network interface |
| `urllib` | URL handling namespace |
| `urllib.request` | Opening and reading URLs |
| `urllib.parse` | URL parsing and encoding |
| `urllib.error` | Exceptions raised by urllib |
| `http` | HTTP namespace |
| `http.client` | HTTP and HTTPS client |
| `http.server` | Basic HTTP server |
| `http.cookies` | Cookie parsing and serialisation |
| `http.cookiejar` | Cookie storage and policy |
| `email` | Email handling namespace |
| `email.parser` | Parsing email messages |
| `email.message` | Email message objects |
| `json` | JSON encoding and decoding |
| `xml` | XML namespace |
| `xml.etree.ElementTree` | Lightweight XML parsing and writing |
| `sqlite3` | SQLite database interface |
| `base64` | Base64 encoding and decoding |
| `ctypes` | Foreign function interface (also used by Hard Traits) |
| `math` | Mathematical functions |
| `datetime` | Date and time types |
| `zipfile` | Reading and writing ZIP archives |
| `tarfile` | Reading and writing tar archives |
| `threading` | Thread-based parallelism |
| `subprocess` | Spawning subprocesses |

---

## Why this is needed

Nuitka compiles to a standalone binary and by default only includes modules it can statically trace through import statements. Soft Traits are Python packages that get loaded from `~/.ethos/traits/` at runtime — Nuitka never sees their import statements during compilation, so anything they depend on from the standard library would be missing unless it's explicitly forced in via this shim.

The shim file is imported during compilation (Nuitka sees its imports) but does nothing at runtime — it exists purely to tell Nuitka "include these".

`ctypes` is doubly important here because it's also what the Hard Trait loader uses to call into compiled `.so` libraries.

---

## Adding more modules

If you write or install a Soft Trait that needs a stdlib module not in this list, add an import for it to `stdlib_shim.py` in the `ethos-lang` repo and rebuild. Open a PR or issue if it's something generally useful — it might be worth bundling by default.
