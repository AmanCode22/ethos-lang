# Ethos

![Ethos Logo](ethos_logo.png)

**A language that speaks for itself — literally.**

Ethos is a programming language with English-based syntax. Every statement is a sentence. Every sentence ends with a period. No brackets, no semicolons, no cryptic symbols. It transpiles to Python, so it's quick to get running and easy to extend.

Extensions come in two kinds — **Soft Traits** (Python packages) and **Hard Traits** (compiled C/C++/Rust binaries loaded via ctypes). Both are managed by **Forge**, the companion package manager.

I built this myself as a solo side project. I'm a Class 9 student from India and I wrote every line of this.

---

## What it looks like

```
ask "What's your name? " into name.

set greeting to "Hello, ".
say greeting.
say name.

set score to 95.

if score is above 90.
    say "That's an A.".
otherwise if score is at least 75.
    say "That's a B.".
otherwise.
    say "Keep going.".
end.
```

---

## Getting started

### Windows

A combined installer for both **Ethos and Forge** is on the [releases page](https://github.com/AmanCode22/ethos-lang/releases). That's the easiest way to get both tools at once. There's also a standalone compiled `.exe` for Ethos only on the same page if that's all you need. The installer sets up PATH and registers the `.ethos` file extension automatically.

### Linux

See [LINUX_INSTALL.md](LINUX_INSTALL.md) for all options — OBS repos, AUR, and the universal tarball.

The pre-built binary on the [releases page](https://github.com/AmanCode22/ethos-lang/releases) is a standalone compiled executable. No Python needed.

### From source

Python 3.10 or newer.

```bash
git clone https://github.com/AmanCode22/ethos-lang.git
cd ethos-lang
pip install -r requirements.txt

python main.py              # opens the REPL
python main.py hello.ethos  # runs a file
```

---

## The language

### Sentences and periods

Every statement ends with `.`. The lexer splits on `.` that aren't inside quoted strings, so decimal numbers like `3.14` work fine inside expressions.

### Case insensitivity

All keywords are case-insensitive. `SET`, `Say`, `REPEAT`, `HOW TO` all work. String contents are never touched — only bare words outside quotes get lowercased.

### Indentation

Indentation is completely ignored. The parser tracks block depth through block-opening keywords and `end.` statements. Indent for readability, not correctness.

---

## Variables

```
set x to 10.
set name to "Aman".
set result to x times 3 plus 1.
```

String slicing:

```
set piece to name from 0 to 3.
```

In-place operations:

```
add 5 to score.
subtract 1 from lives.
```

Delete a variable:

```
delete variable temp.
```

---

## Arithmetic

| Write this        | Means |
|-------------------|-------|
| `plus`            | `+`   |
| `minus`           | `-`   |
| `times`           | `*`   |
| `divided by`      | `/`   |
| `to the power of` | `**`  |

---

## Output and input

```
say "Hello.".
say result.
say 42.

ask "Enter something: " into response.
```

`ask` takes exactly four tokens: `ask`, the prompt string, `into`, and the variable name.

---

## Conditionals

```
if score is above 90.
    say "A".
otherwise if score is at least 75.
    say "B".
otherwise.
    say "C".
end.
```

One `end.` closes the whole chain. Comparisons: `is`, `is not`, `is above`, `is below`, `is at least`, `is at most`. Logical: `and`, `or`, `not`.

---

## Loops

Repeat N times:

```
repeat 5.
    say "again".
end.
```

Counted range:

```
count from 1 to 10 variable i.
    say i.
end.
```

With a custom step:

```
count from 10 to 0 variable i stepping -1.
    say i.
end.
```

While loop:

```
while lives is above 0.
    subtract 1 from lives.
end.
```

---

## Functions

```
how to greet with name.
    say "Hey,".
    say name.
end.

run greet with "Aman".
```

`run` and `run function` do the same thing. Multiple parameters are comma-separated after `with`.

---

## Imports

```
bring in math.
```

---

## Comments

```
note this is a single line comment.

notes.
this spans
multiple lines.
endnotes.
```

---

## Debugging

Inspect generated Python without running it:

```
python.
set x to 5 plus 3.
pythonend.
```

Prints `PY_GEN: x =  5 + 3`.

Trace tokens before each statement:

```
debug.
set x to 10.
debugend.
```

Prints `DEBUG: set x to 10`.

---

## Running Ethos

```bash
ethos myprogram.ethos   # run a file
ethos                   # open the REPL
ethos --version         # check version
ethos -v
```

The REPL tracks open blocks — when you start an `if`, `while`, `repeat`, `count`, or `how to`, the prompt switches to `...` and buffers input until you close with `end.`. Session history saves to `~/.ethos/.ethos_history`. Type `exit` or `quit` to leave.

---

## Traits

**Soft Traits** are Python packages. Forge installs them into `~/.ethos/traits/`, which Ethos prepends to `sys.path` at startup. Use them with `bring in`.

**Hard Traits** are compiled shared libraries. At startup, Ethos scans `~/.ethos/traits/hard_traits/`, reads each trait's `manifest.json`, loads the `.so` with `ctypes.CDLL`, and wires up every exported function's signature. The Hard Trait SDK for C/C++ and Rust is currently under development.

Both kinds are managed by Forge → [github.com/AmanCode22/forge](https://github.com/AmanCode22/forge)

The compiled binary bundles a set of standard library modules so Soft Traits can use them at runtime without needing a system Python install. See [STDLIB_SHIMS.md](STDLIB_SHIMS.md) for the full list.

---

## What's next

- macOS `.pkg` installer
- Android via Termux
- Hard Trait SDK for C/C++ and Rust
- Eventually: rewrite the core in C, C++, or Rust

**Expected later (not planned right now):** LSP support, VSCode/Zed extensions, Ethos Studio GUI IDE.

---

## Contributing

Solo project, but contributions are welcome — especially Hard Trait SDK bindings for Go, Java, Zig, or any language other than C/C++ and Rust (which I'm handling myself). Bug reports and fixes always appreciated. Open an issue before starting anything large so we don't duplicate effort.

---

## Project layout

```
ethos-lang/
├── main.py
├── requirements.txt
└── src/ethos/
    ├── cli.py        — REPL and file runner
    ├── lexer.py      — sentence splitter and tokenizer
    ├── parser.py     — transpiler to Python
    └── executer.py   — runner and Hard Trait loader
```

Build instructions: [BUILDING.md](BUILDING.md)  
Full language reference: [DOCS.md](DOCS.md)  
Linux installation: [LINUX_INSTALL.md](LINUX_INSTALL.md)  
Bundled stdlib modules: [STDLIB_SHIMS.md](STDLIB_SHIMS.md)

---

## Related

- Forge (package manager) → [github.com/AmanCode22/forge](https://github.com/AmanCode22/forge)
- ethos-builder (build scripts, packaging) → [github.com/AmanCode22/ethos-builder](https://github.com/AmanCode22/ethos-builder)

---

## License

Apache 2.0. See [LICENSE](LICENSE).
