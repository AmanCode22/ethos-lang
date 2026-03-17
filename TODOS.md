# **📝 Ethos & Forge Roadmap**

Since this is a solo project in a heavy alpha state, this is where I'm tracking my personal progress for the Ethos language, the Forge package manager, and the surrounding ecosystem.

## **🧠 Core Language (Ethos)**

* \[x\] Basic Lexer (sentence splitting, tokenization, shlex handling)  
* \[x\] Parser (translating conversational English syntax to Python logic)  
* \[x\] Executer (isolated memory dictionary implementation)  
* \[x\] Persistent state tracking across REPL lines  
* \[x\] Multi-OS compatibility (Windows, macOS, Linux)  
* \[x\] Implement support for multi-line up/down arrow history in REPL (readline) 
* \[x\] Fix multiple arguments failing in functions (comma parsing bug)
## **📦 Package Manager (Forge)**

* [x] Zero-dependency CLI structure  
* [x] Support installing Python "Soft Traits" via custom pip sdist/bdist installation setup
* [x] Define Forge fetching strategy for pre-compiled binaries (Hard Traits)
* [ ] Extract and store traits locally in ~/.ethos/traits/  
* [ ] Add update and remove commands for installed traits

## **🔌 The Traits Ecosystem (SDKs & Plugins)**

* [x] Soft Traits: Python native package support
* [x] Core: Finalize the standard C-ABI loading protocol in Ethos (using ctypes)  
* [ ] SDK: Build the standard Ethos Trait API Header for C/C++ developers  
* [ ] SDK: Build the standard Ethos Trait API Crate for Rust developers (using cdylib)  
* [ ] SDK: Build the standard Ethos Trait API bindings for Java (GraalVM native-image)


## **🖥️ Ethos IDE (Alpha)**

* \[ \] Initial Qt-based GUI design  
* \[ \] Integrate built-in Runner  
* \[ \] Integrate built-in Compiler  
* \[ \] Implement syntax highlighting specifically for Ethos syntax  
* \[ \] Full stable release for IDE

## **🔮 Future Architecture & Platforms**

* \[ \] Android support (via Termux)  
* \[ \] Rewrite core Lexer, Parser, and Executer in C/Rust for performance
