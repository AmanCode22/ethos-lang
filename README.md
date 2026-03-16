# Ethos & Forge 🌌

**Ethos** is a cross-platform, natural-syntax programming language that translates conversational sentences into executable Python logic. 
**Forge** is its dedicated, zero-dependency package manager built to handle a dynamic plugin ecosystem.

## ✨ Features

* **Conversational Syntax:** Write code that reads like natural English. Ethos parses your sentences and runs them in a secure, isolated memory box.
* **Zero-Dependency Package Management:** Forge operates entirely on standard libraries (`argparse`, `urllib`, `sysconfig`, `zipfile`), bypassing the need for `pip`.
* **Soft Traits (Python):** Seamlessly download and extract Python wheels directly from PyPI's JSON API into your local `~/.ethos/traits/` backpack.
* **Hard Traits (Native):** Load high-performance native binaries (`.so`, `.dll`) written in C, Rust, or GraalVM Java using a strict C-ABI protocol via `ctypes`.
* **Interactive REPL:** A fully functional command-line interface with session history and multiline execution support.

## 🏗️ Architecture

The ecosystem is divided into two core components:

### Ethos (The Language Core)
* **Lexer & Parser:** Converts conversational commands (e.g., `bring in math`, `run math.sqrt with 1, 4, 5.`) into abstract Python logic.
* **Executer:** Evaluates the compiled logic inside an isolated state dictionary, ensuring variables and imports persist seamlessly across REPL lines.

### Forge (The Switchboard)
* Acts as the CLI entry point for extending the language.
* Identifies correct OS tags and manages the installation, updating, and linking of external "Traits" without cluttering the global Python environment.

## 🚀 Getting Started

*(Note: Installation steps will be updated as the binaries are finalized.)*

1. Clone the repository:
   ```bash
   git clone [https://github.com/AmanCode22/ethos-lang.git](https://github.com/AmanCode22/ethos-lang.git)
   cd ethos-lang
