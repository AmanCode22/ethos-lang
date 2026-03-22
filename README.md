# Ethos

![Ethos Logo](ethos_logo.png)

**A language that speaks for itself — literally.**

Ethos is a programming language with an English-based syntax. Every statement is a sentence. Every sentence ends with a period. No brackets, no semicolons, no cryptic symbols.

It transpiles to Python, so it's fast to get running and easy to extend. Native extensions are called **Hard Traits** — compiled C/C++/Rust binaries loaded via ctypes at startup. Python package extensions are called **Soft Traits**. Both are managed by **Forge**, the companion package manager.

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

A combined installer for both **Ethos and Forge** lives in the [ethos-lang releases](https://github.com/amancode22/ethos-lang/releases). That's the easiest way to get both tools at once. There's also a standalone compiled `.exe` for Ethos only in the same releases page if that's all you need.

### Linux (pre-built binary)

Grab the binary from [Releases](https://github.com/amancode22/ethos-lang/releases):

```bash
chmod +x ethos
sudo mv ethos /usr/local/bin/
```

Linux package builds are coming soon — `.tar.gz` with a compiler and `install.sh`, COPR, PPA, and AUR (both PKGBUILD and a pre-compiled binary package).

### From source

Python 3.10 or newer.

```bash
git clone https://github.com/amancode22/ethos-lang.git
cd ethos-lang
pip install -r requirements.txt

python main.py              # opens the REPL
python main.py hello.ethos  # runs a file
```

---

## The language

### Sentences and periods

Every statement ends with `.`. That's the only punctuation rule. The lexer splits on `.` that aren't inside quoted strings, so decimal numbers like `3.14` work fine inside expressions.

### Case insensitivity

All keywords are case-insensitive. `SET`, `Say`, `REPEAT`, `If`, `HOW TO` all work. String contents are never touched — only bare words outside quotes get lowercased.

### Indentation and spaces

Indentation is completely ignored. The parser tracks block depth itself through block-opening keywords and `end.` statements — extra or missing spaces don't affect parsing at all. Indent for readability, not correctness.

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

One `end.` closes the whole chain. Logical operators work inside conditions:

```
if age is at least 18 and verified is 1.
    say "Access granted.".
end.
```

Comparisons: `is`, `is not`, `is above`, `is below`, `is at least`, `is at most`

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

`run` and `run function` do exactly the same thing. Multiple parameters are comma-separated after `with`.

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

## Debugging tools

Inspect the generated Python without running it:

```
python.
set x to 5 plus 3.
pythonend.
```

Prints `PY_GEN: x =  5 + 3`.

Trace tokens before each statement executes:

```
debug.
set x to 10.
debugend.
```

Prints `DEBUG: set x to 10`.

---

## Running Ethos

Run a file:

```bash
ethos myprogram.ethos
```

Open the REPL:

```bash
ethos
```

The REPL tracks open blocks. When you start an `if`, `while`, `repeat`, `count`, or `how to`, the prompt switches to `...` and buffers your input until you close with `end.`, then the whole block executes at once. Session history is saved to `~/.ethos/.ethos_history`.

Type `exit` or `quit` to leave.

---

## Traits

**Soft Traits** are Python packages. Forge installs them into `~/.ethos/traits/`, which Ethos prepends to `sys.path` at startup. Use them with `bring in`.

**Hard Traits** are compiled shared libraries. At startup, Ethos scans `~/.ethos/traits/hard_traits/`, reads each trait's `manifest.json`, loads the `.so` with `ctypes.CDLL`, and wires up every exported function's signature from the manifest. The library is then available in your program's execution environment under the trait name.

Both kinds are managed by **Forge** → [github.com/amancode22/forge](https://github.com/amancode22/forge)

---

## What's next

- Linux `.tar.gz` (compiler + install.sh), COPR, PPA, and AUR with pre-compiled package
- macOS `.pkg` installer
- Android via Termux
- Hard Trait SDK for C/C++ and Rust
- Language Server Protocol (LSP)
- VSCode and Zed extensions
- Ethos Studio — a GUI IDE
- Eventually: rewrite the core in C, C++, or Rust

---

## Contributing

Solo project, but contributions are welcome — especially Hard Trait SDK bindings for languages other than C/C++ and Rust, which I'm handling myself. If you want to write SDK support for Go, Java, Zig, or anything else, open a PR. Bug reports and fixes always appreciated.

Open an issue before starting anything large so we don't duplicate effort.

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

Build instructions: [BUILDING.md](BUILDING.md). Full language reference: [DOCS.md](DOCS.md).

## License

Apache 2.0. See [LICENSE](LICENSE).
