# **Ethos — Language Reference**

The Hard Trait SDK for C/C++ and Rust is under development and will ship separately. This document covers the full language syntax, how the lexer and parser work internally, and the runtime format for both Soft and Hard Traits.

## **Contents**

1. [How the syntax works](https://www.google.com/search?q=%231-how-the-syntax-works)  
2. [How the lexer works](https://www.google.com/search?q=%232-how-the-lexer-works)  
3. [Statements](https://www.google.com/search?q=%233-statements)  
4. [Operators](https://www.google.com/search?q=%234-operators)  
5. [Type Casting](https://www.google.com/search?q=%235-type-casting)  
6. [Hard Trait runtime format](https://www.google.com/search?q=%236-hard-trait-runtime-format)  
7. [Soft Trait runtime](https://www.google.com/search?q=%237-soft-trait-runtime)  
8. [Errors](https://www.google.com/search?q=%238-errors)

## **1\. How the syntax works**

Ethos programs are .ethos files. The rules:

* Every statement is a sentence typically ending with a period.  
* Keywords are case-insensitive. SET, Say, REPEAT, HOW TO all work. String contents are never modified — only bare words outside quotes get lowercased.  
* Strings go in "double" or 'single' quotes.  
* Indentation is completely ignored. The parser tracks block depth itself through block-opening keywords and end. statements. Extra or missing spaces don't affect parsing.  
* Blank lines are ignored.  
* Trailing periods on block keywords (like end., otherwise., if.) are safely ignored by the parser, allowing you to write natural-sounding sentences without breaking execution blocks.

## **2\. How the lexer works**

Two passes happen before anything runs.

**Pass 1 — split into sentences.** The source text is cut at every . that isn't inside a quoted string. Decimal numbers like 3.14 are protected by the regex pattern. Each chunk becomes one statement. Blank chunks are dropped.

**Pass 2 — tokenize.** Each sentence is split into words using POSIX-style shell splitting via shlex.split, which keeps quoted strings intact. Every token that isn't a quoted string is lowercased. The trailing . is stripped from the last token.

A pre-processing step then merges multi-word phrases into single tokens before the parser sees them:
```
is not           is above        is below         is at least  
is at most       divided by      to the power of  bring in  
how to           otherwise if    run function     delete variable  
to number        to decimal      to text          to boolean  
to list          to tuple        to set           to dictionary  
to bytes         to complex
```
The merger tries lengths 4, 3, and 2 in that order — so to the power of (length 4\) takes priority over any shorter overlap.

## **3\. Statements**

### **say — print**
```
say <value>.

say "Hello.".  
say score.  
say 42\.
```
Transpiles to print(\<value\>).

### **set — assign a variable**
```
set <var> to <expression>.
```
Expressions can mix variables, literals, and arithmetic operators.
```
set x to 10.  
set name to "Aman".  
set total to x times 3 plus 1.
```
**String Slicing:** Detected when both from and to appear in the token list:
```
set <var> to <source> from <start> to <end>.  
set piece to name from 0 to 3.
```
Transpiles to piece \= name\[0:3\].

**Storing Function Output:** You can assign the result of a function or method directly to a variable using run:
```
set response to run requests.get with "https://google.com".  
set random_num to run random.randint with 1, 10.
```
Transpiles to response \= requests.get("https://google.com").

### **add / subtract — in-place arithmetic**
```
add <value> to <var>.  
subtract <value> from <var>.

add 1 to counter.  
subtract 5 from health.
```
Transpiles to counter \+= 1 and health \-= 5.

### **delete variable — delete a variable**
```
delete variable <name>.
```
Transpiles to del name.

### **ask — read input**
```
ask "<prompt>" into <var>.
```
Must be exactly four tokens. into is required in position 3\. Note that ask always returns text (a string). If you need a number, use type casting (see section 5).
```
ask "Your name: " into username.
```
Transpiles to username \= input("Your name: ").

### **if / otherwise / end — conditionals**
```
if <condition>.  
    ...  
otherwise if <condition>.  
    ...  
otherwise.  
    ...  
end.
```
One end. closes the whole chain. otherwise if becomes elif, bare otherwise becomes else. Conditions can chain with and, or, and not:
```
if age is at least 18 and verified is 1.  
    say "Access granted.".  
end.
```
### **repeat — loop N times**
```
repeat <n>.  
    ...  
end.
```
Loop variable is anonymous (\_). Transpiles to for \_ in range(n):.

### **count — ranged loop**
```
count from <start> to <end> variable <var>.  
    ...  
end.
```
Optional step:
```
count from <start> to <end> variable <var> stepping <step>.  
    ...  
end.

count from 1 to 5 variable i.  
    say i.  
end.

count from 10 to 0 variable i stepping -2.  
    say i.  
end.
```
The parser detects direction from the step sign and adjusts the range end by \+1 for forward loops and \-1 for backward loops.

### **while — condition loop**
```
while <condition>.  
    ...  
end.

while lives is above 0.  
    subtract 1 from lives.  
end.
```
### **how to / run — functions**

Define:
```
how to <name>.  
    ...  
end.

how to <name> with <param1>, <param2>.  
    ...  
end.
```
Call:
```
run <name>.  
run <name> with <arg1>, <arg2>.  
run function <name> with <arg1>.
```
run and run function are identical — both exist so code reads naturally either way. **Dot-notation** is natively supported for calling nested functions and module methods:
```
bring in requests.  
run requests.get with "https://api.github.com".

how to greet with name.  
    say name.  
end.

run greet with "Aman".
```
### **bring in — import a module or Soft Trait**
```
bring in <module>.
```
Transpiles to import \<module\>.

### **note / notes — comments**
```
note single line comment.

notes.  
block comment  
spanning lines.  
endnotes.
```
Single-line notes transpile to \# .... Block notes use ''' ... '''.

### **python / pythonend — inspect generated Python**

Statements inside this block print the transpiled Python instead of running it.
```
python.  
set x to 5 plus 3.  
pythonend.
```
Output: PY\_GEN: x \= 5 \+ 3

### **debug / debugend — trace tokens**

Prints the full token list for each statement before it executes.
```
debug.  
set x to 10.  
debugend.
```
Output: DEBUG: set x to 10

## **4\. Operators**

### **Arithmetic**

| Ethos | Python |
| :---- | :---- |
| plus | \+ |
| minus | \- |
| times | \* |
| divided by | / |
| to the power of | \*\* |

### **Comparison**

| Ethos | Python |
| :---- | :---- |
| is | \== |
| is not | \!= |
| is above | \> |
| is below | \< |
| is at least | \>= |
| is at most | \<= |

### **Logical**

| Ethos | Python |
| :---- | :---- |
| and | and |
| or | or |
| not | not |

## **5\. Type Casting**

Ethos supports **postfix type casting** on the right side of set assignments. This is especially useful for converting string input from the ask command into mathematical values.

| Ethos Casting Phrase | Python Equivalent | Example |
| :---- | :---- | :---- |
| to number | int() | set age to "25" to number. |
| to decimal | float() | set pi to "3.14" to decimal. |
| to text | str() | set label to 42 to text. |
| to boolean | bool() | set flag to 1 to boolean. |
| to list | list() | set items to my\_tuple to list. |
| to tuple | tuple() | set locked to my\_list to tuple. |
| to set | set() | set unique to my\_list to set. |
| to dictionary | dict() | set mapping to pairs to dictionary. |
| to bytes | bytes() | set data to "raw" to bytes. |
| to complex | complex() | set math\_c to 5 to complex. |

**Chaining casts:** You can chain conversions together. They process from left to right.
```
set score to "95.5" to decimal to number.
```
*(Transpiles to score \= int(float("95.5")))*

## **6\. Hard Trait runtime format**

The Hard Trait SDK is still in development. This section documents what the Ethos runtime expects from an installed Hard Trait — enough to understand loading, not enough to write one from scratch yet. Community SDK contributions for languages other than C/C++ and Rust are welcome via PR.

### **Directory layout**
```
~/.ethos/traits/hard\_traits/\<trait-name\>/
├── manifest.json  
└── \<binary\>.so
```
The folder name must match the name field in manifest.json.

### **manifest.json**
```
{  
  "name": "mymath",  
  "binary": "mymath.so",  
  "functions": {  
    "add\_ints": {  
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
| :---- | :---- | :---- |
| name | yes | Trait name. Must match the directory name. |
| binary | yes | Shared library filename, relative to the trait folder. |
| functions | yes | Map of exported function names to their signatures. |
| functions.\<n\>.return | yes | Return type string. Use "void" for no return. |
| functions.\<n\>.args | yes | List of argument type strings. Use \[\] for none. |

### **Supported types**

| manifest string | C type |
| :---- | :---- |
| "char" | char |
| "unsigned char" | unsigned char |
| "wchar\_t" | wchar\_t |
| "short" | short |
| "unsigned short" | unsigned short |
| "int" | int |
| "unsigned int" | unsigned int |
| "long" | long |
| "unsigned long" | unsigned long |
| "long long" | long long |
| "unsigned long long" | unsigned long long |
| "int8\_t" | int8\_t |
| "uint8\_t" | uint8\_t |
| "int16\_t" | int16\_t |
| "uint16\_t" | uint16\_t |
| "float" | float |
| "double" | double |
| "long double" | long double |
| "char \*" | char \* |
| "wchar\_t \*" | wchar\_t \* |
| "void \*" | void \* |
| "pointer\_to\_int" | int \* |
| "size\_t" | size\_t |
| "ssize\_t" | ssize\_t |
| "bool" | bool |
| "void" | (no return value) |

An unrecognized type skips that one function with a warning. The rest of the trait still loads.

### **SDK language support**

| Language | Status |
| :---- | :---- |
| C / C++ | Official SDK — under development |
| Rust | Official SDK — under development |
| Everything else | Community PRs welcome |

### **How loading works**

On startup, Ethos scans \~/.ethos/traits/hard\_traits/ and for each subfolder:

1. Looks for manifest.json. Missing → warning, skip.  
2. Parses it as JSON. Invalid → warning, skip.  
3. Checks the binary file exists. Missing → warning, skip.  
4. Loads it with ctypes.CDLL.  
5. For each function in "functions", sets restype and argtypes. Bad type string → warning for that function only, rest of trait still loads.  
6. Puts the library object into the execution environment under the trait's name. Ethos programs can then call its functions directly.

## **7\. Soft Trait runtime**

Soft Traits are Python packages sitting in \~/.ethos/traits/. Ethos prepends that path to sys.path at startup, so bring in works exactly like a normal import.

Forge recursively resolves dependencies via PyPI's JSON API. Forge never runs install scripts. It only extracts the wheel or sdist archive. For a package to be importable, its top-level module folder must land directly inside \~/.ethos/traits/ after extraction.

## **8\. Errors**

### **Parser**

| Message | What happened |
| :---- | :---- |
| Error: 'end' found without a matching block | end. with no matching if, while, repeat, count, or how to. |
| Error: 'say' needs a value | say used with nothing after it. |
| Invalid syntax used, correct syntax is ask 'Prompt string' into variable\_name | ask missing into, or wrong token count. |

### **Runtime**

| Message | What happened |
| :---- | :---- |
| Ethos Runtime Error: \<msg\> | Exception during exec(). The Python error is shown. |

### **Hard Trait loading**

| Message | What happened |
| :---- | :---- |
| Warning: Trait \<n\> does not have a manifest.json file... | No manifest in the trait folder. |
| Warning: Trait \<n\> manifest.json file is invalid... | Manifest isn't valid JSON. |
| Warning: Trait \<n\> binary path defined in manifest.json is invalid... | The .so listed in "binary" doesn't exist. |
| Warning: In trait \<n\> there is a function named \<fn\> of which types are not correctly written... | Type string not in the supported types table. |

### **Forge errors (when used with Ethos)**

| Message | What happened |
| :---- | :---- |
| \[-\] This package does not exist or its a network error/pypi might be blocked | PyPI lookup failed or the package name is wrong. |
| \[-\] Cannot get results from pypi... | PyPI response couldn't be decoded. |
| \[-\] This package doesnt support your system and its tar sdist isnt published | No compatible wheel or sdist for your platform. |
| \[-\] Invalid Hard Trait: No manifest.json found | Zip has no manifest.json at any depth. |
| \[-\] Trait cannot be installed due to invalid manifest.json. | Manifest is missing name or binary. |
| \[-\] Failed to remove. Soft trait \<n\> is not installed. | Package not in \~/.ethos/traits/. |
| \[-\] Failed to remove. Hard trait \<n\> is not installed. | Trait not in \~/.ethos/traits/hard\_traits/. |
