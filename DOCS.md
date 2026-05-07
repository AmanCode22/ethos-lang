# Ethos — Language Reference

Complete syntax reference. Covers lexer, parser, runtime, and Hard Trait format.

## Contents

1. [Syntax Rules](#1-syntax-rules)
2. [Lexer Internals](#2-lexer-internals)
3. [Statements](#3-statements)
4. [Operators](#4-operators)
5. [Type Casting](#5-type-casting)
6. [Hard Trait Format](#6-hard-trait-format)
7. [Soft Trait Runtime](#7-soft-trait-runtime)
8. [Errors](#8-errors)

---

## 1. Syntax Rules

- Every statement ends with a period (`.`)
- Keywords are case-insensitive (`SET`, `Say`, `set` all work)
- Strings use `"double"` or `'single'` quotes
- Indentation is ignored — parser tracks blocks via keywords
- Blank lines are ignored
- Trailing periods on block keywords (`end.`, `otherwise.`) are optional

---

## 2. Lexer Internals

**Pass 1 — Sentence Splitting**

Text is split at `.` characters, except:
- Inside quoted strings
- Decimal numbers (`3.14`)
- Dot notation (`math.sqrt`)

**Pass 2 — Tokenization**

Each sentence is split via `shlex.split()`. Quoted strings stay intact. Non-quoted tokens are lowercased. The trailing period is stripped.

**Multi-word Phrase Merging**

Before parsing, these phrases are merged into single tokens:

```
is not          is above         is below         is at least
is at most      divided by       to the power of  bring in
how to          otherwise if     run function     delete variable
to number       to decimal       to text          to boolean
to list         to tuple         to set           to dictionary
to bytes        to complex
```

Merger tries lengths 4, 3, 2 in order — `to the power of` (length 4) takes priority.

---

## 3. Statements

### `say` — Print

```ethos
say <value>.

say "Hello.".
say score.
say 42.
```

Transpiles to `print(<value>)`.

---

### `set` — Assignment

```ethos
set <var> to <expression>.

set x to 10.
set name to "Aman".
set total to x times 3 plus 1.
```

**String Slicing:**

```ethos
set <var> to <source> from <start> to <end>.

set piece to name from 0 to 5.
```

Transpiles to `piece = name[0:5]`.

**Function Return Value:**

```ethos
set response to run requests.get with "https://api.github.com".
set random_num to run random.randint with 1, 10.
```

---

### `add` / `subtract` — In-place Arithmetic

```ethos
add <value> to <var>.
subtract <value> from <var>.

add 1 to counter.
subtract 5 from health.
```

---

### `delete variable` — Delete

```ethos
delete variable <name>.
```

---

### `ask` — Input

```ethos
ask "<prompt>" into <var>.

ask "Your name: " into username.
```

Exactly 4 tokens required. `into` is mandatory. Returns string — use type casting for numbers.

---

### `if` / `otherwise if` / `otherwise` / `end` — Conditionals

```ethos
if <condition>.
    ...
otherwise if <condition>.
    ...
otherwise.
    ...
end.
```

Conditions support `and`, `or`, `not`:

```ethos
if age is at least 18 and verified is 1.
    say "Access granted.".
end.
```

---

### `repeat` — Count Loop

```ethos
repeat <n>.
    ...
end.
```

Anonymous loop variable (`_`).

---

### `count` — Ranged Loop

```ethos
count from <start> to <end> variable <var>.
    ...
end.

count from 1 to 5 variable i.
    say i.
end.
```

**With Step:**

```ethos
count from <start> to <end> variable <var> stepping <step>.
    ...
end.

count from 10 to 0 variable i stepping -2.
    say i.
end.
```

Parser adjusts range end by `+1` (forward) or `-1` (backward).

---

### `while` — Condition Loop

```ethos
while <condition>.
    ...
end.

while lives is above 0.
    subtract 1 from lives.
end.
```

---

### `how to` / `run` — Functions

**Define:**

```ethos
how to <name>.
    ...
end.

how to <name> with <param1>, <param2>.
    ...
end.
```

**Call:**

```ethos
run <name>.
run <name> with <arg1>, <arg2>.
run function <name> with <arg1>.
```

`run` and `run function` are identical. Dot notation works:

```ethos
bring in requests.
run requests.get with "https://api.github.com".
```

---

### `bring in` — Import

```ethos
bring in <module>.

bring in math.
bring in requests.
```

Access module attributes and functions:

```ethos
bring in math.
set pi to math.pi.
set result to run function math.sqrt with 16.
```

---

### `note` / `notes` — Comments

```ethos
note single line comment.

notes.
block comment
spanning lines.
endnotes.
```

---

### `python` / `pythonend` — Inspect Generated Code

```ethos
python.
set x to 5 plus 3.
pythonend.
```

Output: `PY_GEN: x = 5 + 3`

---

### `debug` / `debugend` — Token Trace

```ethos
debug.
set x to 10.
debugend.
```

Output: `DEBUG: set x to 10`

---

## 4. Operators

### Arithmetic

| Ethos | Python |
|-------|--------|
| `plus` | `+` |
| `minus` | `-` |
| `times` | `*` |
| `divided by` | `/` |
| `to the power of` | `**` |

### Comparison

| Ethos | Python |
|-------|--------|
| `is` | `==` |
| `is not` | `!=` |
| `is above` | `>` |
| `is below` | `<` |
| `is at least` | `>=` |
| `is at most` | `<=` |

### Logical

| Ethos | Python |
|-------|--------|
| `and` | `and` |
| `or` | `or` |
| `not` | `not` |

---

## 5. Type Casting

Postfix casts on `set` right-hand side:

| Ethos | Python | Example |
|-------|--------|---------|
| `to number` | `int()` | `set age to "25" to number.` |
| `to decimal` | `float()` | `set pi to "3.14" to decimal.` |
| `to text` | `str()` | `set label to 42 to text.` |
| `to boolean` | `bool()` | `set flag to 1 to boolean.` |
| `to list` | `list()` | `set items to my_tuple to list.` |
| `to tuple` | `tuple()` | `set locked to my_list to tuple.` |
| `to set` | `set()` | `set unique to my_list to set.` |
| `to dictionary` | `dict()` | `set mapping to pairs to dictionary.` |
| `to bytes` | `bytes(..., "utf-8")` | `set data to "raw" to bytes.` |
| `to complex` | `complex()` | `set math_c to 5 to complex.` |

**Chaining:**

```ethos
set score to "95.5" to decimal to number.
```

Transpiles to `score = int(float("95.5"))`.

---

## 6. Hard Trait Format

Compiled C/C++/Rust binaries loaded via ctypes.
**Ethos auto loads all hard traits installed on runtime.**

### Directory Layout

```
~/.ethos/traits/hard_traits/<trait-name>/
├── manifest.json
└── (compiled binary here)
```

### manifest.json

```json
{
  "name": "mymath",
  "functions": {
    "add_ints": {
      "return": "int",
      "args": ["int", "int"]
    },
    "get_message": {
      "return": "char *",
      "args": []
    }
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | yes | Must match directory name |
| `binary` | yes | `.so` filename relative to trait folder |
| `functions` | yes | Map of function names to signatures |
| `functions.<n>.return` | yes | Return type (`"void"` for none) |
| `functions.<n>.args` | yes | List of argument types |

### Supported Types
#### C/C++
| manifest string | C type |
|-----------------|--------|
| `char` | `char` |
| `unsigned char` | `unsigned char` |
| `wchar_t` | `wchar_t` |
| `short` | `short` |
| `unsigned short` | `unsigned short` |
| `int` | `int` |
| `unsigned int` | `unsigned int` |
| `long` | `long` |
| `unsigned long` | `unsigned long` |
| `long long` | `long long` |
| `unsigned long long` | `unsigned long long` |
| `int8_t` | `int8_t` |
| `uint8_t` | `uint8_t` |
| `int16_t` | `int16_t` |
| `uint16_t` | `uint16_t` |
| `float` | `float` |
| `double` | `double` |
| `long double` | `long double` |
| `char *` | `char *` |
| `wchar_t *` | `wchar_t *` |
| `void *` | `void *` |
| `pointer_to_int` | `int *` |
| `size_t` | `size_t` |
| `ssize_t` | `ssize_t` |
| `bool` | `bool` |
| `void` | (no return) |

#### Rust
| manifest string | C type | Rust Type(core:ffi) |
|-----------------|--------|-----------------|
| `char` | `char` | `c_char` |
| `unsigned char` | `unsigned char` | 
| `wchar_t` | `wchar_t` | `c_wchar` |
| `short` | `short` | `c_wchar` |
| `unsigned short` | `unsigned short` | `c_ushort` |
| `int` | `int` | `c_int` |
| `unsigned int` | `unsigned int` | `c_uint` |
| `long` | `long` | `c_long` |
| `unsigned long` | `unsigned long` |`c_ulong` |
| `long long` | `long long` | `c_longlong` |
| `unsigned long long` | `unsigned long long` | `c_ulonglong` |
| `int8_t` | `int8_t` | `i8` |
| `uint8_t` | `uint8_t` | `u8` |
| `int16_t` | `int16_t` | `i16` |
| `uint16_t` | `uint16_t` | `u16` |
| `float` | `float` | `c_float` | `c_float` |
| `double` | `double` | `c_double` | `c_double` |
| `long double` | `long double` | `c_double` (platform dependent can vary, experimental) |
| `char *` | `char *` | `*mut c_char` |
| `wchar_t *` | `wchar_t *` | `*mut c_wchar` |
| `void *` | `void *` | `*mut c_void` |
| `pointer_to_int` | `int *` |  `*mut c_int` |
| `size_t` | `size_t` | `usize` |
| `ssize_t` | `ssize_t` | `isize` |
| `bool` | `bool` |  `bool` |
| `void` | (no return) | `()` |

For rust, core:cffi must be used for better compatibility.

Unrecognized types skip that function with a warning.

### SDK Status

| Language | Status |
|----------|--------|
| C | [https://github.com/AmanCode22/ethos-trait-c-template](https://github.com/AmanCode22/ethos-trait-c-template) |
| C++ | [https://github.com/AmanCode22/ethos-trait-cpp-template](https://github.com/AmanCode22/ethos-trait-cpp-template) |
| Rust | [https://github.com/AmanCode22/ethos-trait-rust-template](https://github.com/AmanCode22/ethos-trait-rust-template) |
| Other | Community PRs welcome |

### Ethos foundry
Ethos foundry is a collection of community hard traits pre hosted on github pages and cloudfare pages, see more at : [https://github.com/AmanCode22/ethos-foundry](https://github.com/AmanCode22/ethos-foundry)

### Loading Process

1. Scan `~/.ethos/traits/hard_traits/`
2. Load `manifest.json` (skip if missing/invalid)
3. Verify binary exists (skip if missing)
4. Load with `ctypes.CDLL`
5. Set `restype` / `argtypes` per function
6. Add to execution environment under trait name

---

## 7. Soft Trait Runtime

Soft Traits are Python packages in `~/.ethos/traits/`. Ethos prepends this to `sys.path` at startup.

Forge resolves dependencies via PyPI's JSON API and extracts wheels/sdists directly — no install scripts run.

---

## 8. Errors

### Parser Errors

| Message | Cause |
|---------|-------|
| `Error: 'end' found without a matching block` | `end.` with no matching block opener |
| `Error: 'say' needs a value` | `say` used without argument |
| `Invalid syntax used, correct syntax is ask 'Prompt string' into variable_name` | `ask` missing `into` or wrong token count |

### Runtime Errors

| Message | Cause |
|---------|-------|
| `Ethos Runtime Error: <msg>` | Exception during `exec()` — shows Python error |

### Hard Trait Loading Warnings

| Message | Cause |
|---------|-------|
| `Warning: Trait <n> does not have a manifest.json file...` | Missing manifest |
| `Warning: Trait <n> manifest.json file is invalid...` | Invalid JSON |
| `Warning: Trait <n> binary path defined in manifest.json is invalid...` | Binary not found |
| `Warning: In trait <n>, function <fn> has incorrectly written types...` | Unknown type string |

### Forge Errors

| Message | Cause |
|---------|-------|
| `[-] This package does not exist or its a network error/pypi might be blocked` | PyPI lookup failed |
| `[-] Cannot get results from pypi...` | Decode error |
| `[-] This package doesnt support your system and its tar sdist isnt published` | No compatible wheel/sdist |
| `[-] Invalid Hard Trait: No manifest.json found` | Zip lacks manifest |
| `[-] Trait cannot be installed due to invalid manifest.json.` | Missing `name` or `binary` |
| `[-] Failed to remove. Soft trait <n> is not installed.` | Package not found |
| `[-] Failed to remove. Hard trait <n> is not installed.` | Trait not found |
