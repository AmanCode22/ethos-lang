# **Ethos**
![Ethos Logo](ethos_logo.png)
**A language that speaks for itself — literally.**

Ethos is a programming language with English-based syntax. Every statement is a sentence. Every sentence ends with a period. No brackets, no semicolons, no cryptic symbols. It transpiles to Python, so it's quick to get running and easy to extend.

Extensions come in two kinds — **Soft Traits** (Python packages) and **Hard Traits** (compiled C/C++/Rust binaries loaded via ctypes). Both are managed by **Forge**, the companion package manager.

I built this myself as a solo side project. I'm a Class 9 student from India and I wrote every line of this.

## **What it looks like**
```
ask "What's your name? " into name.

set greeting to "Hello, ".  
say greeting.  
say name.

set score to 95\.

if score is above 90\.  
    say "That's an A.".  
otherwise if score is at least 75\.  
    say "That's a B.".  
otherwise.  
    say "Keep going.".  
end.
```
## **Getting started**

### **Windows**

A combined installer for both **Ethos and Forge** is on the [releases page](https://www.google.com/search?q=https://github.com/AmanCode22/ethos-lang/releases). That's the easiest way to get both tools at once. There's also a standalone compiled .exe for Ethos only on the same page if that's all you need. The installer sets up PATH and registers the .ethos file extension automatically.

### **macOS**

A combined .pkg installer for both **Ethos and Forge** is on the [releases page](https://www.google.com/search?q=https://github.com/AmanCode22/ethos-lang/releases). It natively supports both Apple Silicon (M-chip) and Intel Macs.

### **Linux**

See [LINUX\_INSTALL.md](https://www.google.com/search?q=LINUX_INSTALL.md) for Linux installation instructions.

## **Standard Library**

Ethos bundles several Python standard libraries natively via shims. See [STDLIB\_SHIMS.md](https://www.google.com/search?q=STDLIB_SHIMS.md) for the full list.

## **What's next**

* Android via Termux  
* Hard Trait SDK for C/C++ and Rust  
* **Future Rust Rewrite:** Planning to rewrite the core Ethos transpiler and runtime in Rust for massive performance gains, true memory safety, and native compilation without relying on Python/Nuitka.

**Expected later (not planned right now):** LSP support, VSCode/Zed extensions, Ethos Studio GUI IDE.

## **Contributing**

Solo project, but contributions are welcome — especially Hard Trait SDK bindings for Go, Java, Zig, or any language other than C/C++ and Rust (which I'm handling myself). Bug reports and fixes always appreciated. Open an issue before starting anything large so we don't duplicate effort.

## **Project layout**

ethos-lang/  
├── main.py  
├── requirements.txt  
└── src/ethos/  
    ├── cli.py         — REPL and file runner  
    ├── lexer.py       — sentence splitter and tokenizer  
    ├── parser.py      — transpiler to Python  
    ├── executer.py    — runner and Hard Trait loader  
    ├── stdlib_shim.py — forces stdlib modules into the Nuitka binary  
    └── version.py     — version string

Build instructions: [BUILDING.md](http://docs.google.com/BUILDING.md)

Full language reference: [DOCS.md](https://www.google.com/search?q=DOCS.md)

Linux installation: [LINUX\_INSTALL.md](https://www.google.com/search?q=LINUX_INSTALL.md)

macOS installation: [MACOS\_INSTALL.md](https://www.google.com/search?q=MACOS_INSTALL.md)

Bundled stdlib modules: [STDLIB\_SHIMS.md](https://www.google.com/search?q=STDLIB_SHIMS.md)

## **Related**

* Forge (package manager) → [github.com/AmanCode22/forge](https://www.google.com/search?q=https://github.com/AmanCode22/forge)
