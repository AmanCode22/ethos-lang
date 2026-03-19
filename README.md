
# Ethos

**A language that speaks for itself — literally.**

*Write code the way you'd explain it to someone.*

---

Ethos is a programming language with an English-based syntax. Every statement is a sentence. Every sentence ends with a period. No brackets, no semicolons, no cryptic symbols — just words.

It transpiles to Python under the hood, so it's fast to get running and easy to extend. Native extensions are called **Hard Traits** (compiled C/C++/Rust binaries). Python package extensions are called **Soft Traits**. Both are managed by **Forge**, Ethos's companion package manager.

> Built by [Aman Adlakha](https://github.com/amancode22) — a Class 9 student from India, doing this solo.

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

That's it. That's the language.

---

## Getting started

### Linux (pre-built binary)

Grab the latest binary from the [Releases](https://github.com/amancode22/ethos-lang/releases) page:

```bash
chmod +x ethos
sudo mv ethos /usr/local/bin/
```

> Windows, macOS, Android (Termux), and native Linux packages (`.deb`, `.rpm`, AUR) are on the roadmap.

### From source

You'll need Python 3.10 or newer.

```bash
git clone https://github.com/amancode22/ethos-lang.git
cd ethos-lang
pip install -r requirements.txt

python main.py                 # opens the REPL
python main.py hello.ethos     # runs a file
```

---

## The language

Every Ethos statement is a sentence ending with a `.` — that's the only rule you need to remember upfront.

### Variables

```
set x to 10.
set name to "Aman".
set result to x times 3 plus 1.
```

### Arithmetic

| Write this        | Means |
|-------------------|-------|
| `plus`            | `+`   |
| `minus`           | `-`   |
| `times`           | `*`   |
| `divided by`      | `/`   |
| `to the power of` | `**`  |

### In-place operations

```
add 5 to score.
subtract 1 from lives.
```

### String slicing

```
set piece to name from 0 to 3.
```

### Output

```
say "Hello.".
say result.
```

### Input

```
ask "Enter something: " into response.
```

### Conditionals

```
if score is above 90.
    say "A".
otherwise if score is at least 75.
    say "B".
otherwise.
    say "C".
end.
```

Comparisons: `is`, `is not`, `is above`, `is below`, `is at least`, `is at most`  
Logical: `and`, `or`, `not`

### Loops

```
repeat 5.
    say "again".
end.

count from 1 to 10 variable i.
    say i.
end.

count from 10 to 0 variable i stepping -1.
    say i.
end.

while lives is above 0.
    subtract 1 from lives.
end.
```

### Functions

```
how to greet with name.
    say "Hey,".
    say name.
end.

run greet with "Aman".
```

### Imports

```
bring in math.
```

### Comments

```
note this is a single line comment.

notes.
this spans
multiple lines.
endnotes.
```

### Delete a variable

```
delete variable temp.
```

### Inspect the generated Python

```
python.
set x to 5 plus 3.
pythonend.
```

Prints `PY_GEN: x =  5 + 3` instead of running it. Handy for debugging the transpiler.

### Debug mode

```
debug.
set x to 10.
debugend.
```

Prints the token list for each statement before executing it.

---

## Running Ethos

**Run a file:**
```bash
ethos myprogram.ethos
```

Files need the `.ethos` extension.

**Open the REPL:**
```bash
ethos
```

Type sentences, press Enter. Multi-line blocks buffer automatically until you type `end.` Type `exit` or `quit` to leave. Your history is saved to `~/.ethos/.ethos_history`.

---

## Traits

Ethos can be extended with **Traits** — external packages that plug into your programs.

- **Soft Traits** are Python packages. Install with Forge, use with `bring in`.
- **Hard Traits** are compiled native binaries (C, C++, Rust). They load automatically at startup via ctypes. The Hard Trait SDK is under development.

Traits are managed by **Forge** → [github.com/amancode22/forge](https://github.com/amancode22/forge)

---

## What's next

- [ ] Windows `.msi` installer
- [ ] macOS `.pkg` installer
- [ ] Linux: `.deb`, `.rpm`, AUR
- [ ] Android via Termux
- [ ] Hard Trait SDK for C/C++ and Rust
- [ ] Language Server Protocol (LSP)
- [ ] VSCode and Zed extensions
- [ ] Ethos Studio — a GUI IDE
- [ ] Eventually: rewrite the core in C, C++, or Rust

---

## Contributing

This is a solo project, but outside contributions are welcome — especially:

- **Hard Trait SDK bindings** for languages other than C/C++ and Rust (those I'm handling myself). If you want to write SDK support for Java, Go, Zig, or anything else, open a PR.
- Bug reports and fixes.
- Anything that feels broken or missing.

Open an issue before working on anything big so we don't duplicate effort.

---

## Project layout

```
ethos-lang/
├── main.py
├── requirements.txt
└── src/ethos/
    ├── cli.py        — REPL + file runner
    ├── lexer.py      — sentence splitter + tokenizer
    ├── parser.py     — transpiler
    └── executer.py   — runner + Hard Trait loader
```

---
For instructions on building yourself refer to [BUILDING.md](BUILDING.md) and the full documentation can be accesed at [DOCS.md](DOCS.md).
## License

Apache 2.0. See [LICENSE](LICENSE).

---
