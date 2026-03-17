# **Currently not usable and in heavily alpha stage** #
# **Ethos & Forge 🌌**

**Ethos** is a cross-platform, natural-syntax programming language that translates conversational English into executable Python logic.

**Forge** is its dedicated, zero-dependency package manager built to handle a dynamic plugin ecosystem.

Developed as a **solo-developer passion project**, Ethos is designed to be the absolute easiest way for students and beginners to start writing code. Whether you are on a high-end desktop or writing code on your phone, Ethos runs everywhere.

### **🌍 Universal Platform Support**

Ethos and Forge are pre-compiled and fully supported on:

* **Windows**  
* **macOS**  
* **Linux**  
* **Android (via Termux)** \- Write and run code natively right from your mobile phone\!

## **✨ Why Ethos?**

* **Conversational Syntax:** Code reads exactly like English sentences. No more fighting with semicolons or brackets.  
* **Persistent Execution:** An isolated memory environment ensures your variables, states, and imports carry forward perfectly across interactive REPL lines.  
* **Zero-Dependency Packages:** Forge operates entirely on standard libraries, downloading Python wheels and native binaries without ever touching pip.

## **💻 Code Examples**

Ethos is built to be intuitive. Here is a quick look at what coding in Ethos looks like:

**Variables and Math:**

```
set age to 20.  
add 5 to age.  
say age.
```

**Loops and Conditions:**
```
set counter to 0.  
repeat 5.  
    add 1 to counter.  
    say counter.  
end.
```
**Using Functions and Packages:**
```
bring in math.  
run math.sqrt with 144.
```
## **🔌 The Traits Ecosystem (Plugins)**

Ethos plugins are called **Traits** and are managed by **Forge**.

* **Soft Traits:** Pure Python wheels. Forge downloads them directly from PyPI and extracts them to a local \~/.ethos/traits/ backpack.  
* **Hard Traits:** High-performance native binaries (.so, .dll, .dylib) accessed via a strict C-ABI protocol.

**Current Hard Trait API Status:**

| Language | Status | Integration Details |
| :---- | :---- | :---- |
| **C** | ⏳ *Pending* | Direct C-ABI ctypes integration. |
| **Rust** | ⏳ *Pending* | C-ABI compatible dynamic libraries (cdylib). |
| **Java** | ⏳ *Pending* | Native image shared libraries via GraalVM. |
| **C++ / Go / Zig / Any Other** | 🤝 *Open to PRs* | I welcomes contributions\! Please open an issue to discuss. |

## **🔮 The Future: C & Rust Rewrite**

Ethos is currently built on top of Python and compiled using Nuitka. This allows for rapid prototyping and access to Python's massive ecosystem. However, to achieve ultimate performance, lower memory footprints, and true low-level control, the core Lexer, Parser, and Executer will be **rewritten in C and Rust** in the future.

## **🚀 Getting Started**

Instruction would be added as soon as the project reaches beta/stable stage.


* If you want to know how Ethos works under the hood? Read the [DOCUMENTATION.md](DOCUMENTATION.md).  
* Want to contribute? Create a fork, make your changes, and open a Pull Request\!

**License:** Distributed under the MIT License. See LICENSE for more information.
