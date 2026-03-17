# **📝 Ethos & Forge To-Do List**

Track the progress of the Ethos language, the Forge package manager, and the surrounding ecosystem here.

## **🧠 Core Language (Ethos)**

* \[x\] Basic Lexer (sentence splitting, tokenization, shlex handling)  
* \[x\] Parser (translating conversational English syntax to Python logic)  
* \[x\] Executer (isolated memory dictionary implementation)  
* \[x\] Persistent state tracking across REPL lines  
* \[x\] Multi-OS compatibility (Windows, macOS, Linux)  
* \[ \] Implement support for multi-line up/down arrow history in REPL (readline)  
* \[ \] Fix multiple arguments failing in functions (comma parsing bug)

## **📦 Package Manager (Forge)**

* \[ \] Zero-dependency CLI structure  
* \[ \] Download Soft Traits (Python wheels) via PyPI JSON API  
* \[ \] Extract and store traits locally in \~/.ethos/traits/  
* \[ \] Add update and remove commands for installed traits

## **🔌 The Traits Ecosystem (Plugins)**

* \[ \] Soft Traits (Python) full support  
* \[ \] Hard Traits: C-ABI integration (ctypes)  
* \[ \] Hard Traits: Rust (cdylib) integration  
* \[ \] Hard Traits: Java (GraalVM native image) integration

## **🖥️ Ethos IDE**

* \[ \] Initial Qt-based GUI design (Alpha Stage)  
* \[ \] Integrate built-in Runner  
* \[ \] Integrate built-in Compiler  
* \[ \] Implement syntax highlighting specifically for Ethos syntax  
* \[ \] Full stable release for IDE

## **🔮 Future Architecture & Platforms**

* \[ \] Android support (via Termux)  
* \[ \] Rewrite core Lexer, Parser, and Executer in C/Rust for performance
