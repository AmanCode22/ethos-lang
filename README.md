# Project Stopped
Due to lack of testers I am halting developement of Ethos and all it's components, if I would get testers I would restart the developement and would start rust rewrite.
If you want to test then send me reddit dm to username AmanCode22.
Testers who can test current version and can help me finding bugs and issues in my code by testing it. I need some begineers who are starting proggraming to try out Ethos and need their reviews.


# Ethos
<img src="ethos_logo.png" alt="Ethos Logo" width="500">

**A language that speaks for itself.**

Ethos transpiles English-like syntax to Python. Every statement ends with a period. No brackets, no semicolons.

I built this solo. Class 9 student from India.

You can try Ethos in live playground at any one of following
- https://ethos-lang.pages.dev/
- https://amancode22.github.io/ethos-lang/

  
## Rust Rewrite in progress stopped
Ethos was started being rewritten in rust but due to lack of testers I am stopping it also.


## Quick Example

```ethos
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

## Installation

### Windows / macOS

Download the installer from [releases](https://github.com/AmanCode22/ethos-lang/releases). The installer includes both Ethos and Forge (the package manager).

### Linux

See [LINUX_INSTALL.md](LINUX_INSTALL.md) for distro-specific instructions.

### Android via Termux
Nuitka builds on termux are not supported due to restrictions and linker issue so ethos in termux requires python and is just a wrapper to run python source code compressed using zipapp. After rust rewrite the termux prebuilt binaries would be provided till then .deb file and termux pkg integration is just done. Supported after v0.5.0 beta.
You can also add repo of ethos in termux.
#### By downlaoading debs
Run after downloading the deb file manually or using wget or curl
```bash
pkg update && pkg upgrade
pkg install python
pkg install ./termux-deb-path-here-which-you-downloaded.deb
```
#### By adding repo
Run
```
mkdir -p $PREFIX/etc/apt/sources.list.d/
echo "deb [trusted=yes] https://amancode22.github.io/ethos-termux-repo/repo termux extras" >> $PREFIX/etc/apt/sources.list.d/ethos-repo.list
pkg update
pkg install ethos-lang ethos-forge
```

## Core Features

- **English syntax** - `if`, `while`, `repeat`, `count` loops all read like sentences
- **Type casting** - `set age to "25" to number.`
- **String slicing** - `set piece to text from 0 to 5.`
- **Functions** - `how to greet with name.` / `run greet with "Aman".`
- **Imports** - `bring in math.` then `run math.sqrt with 16.`
- **Hard Traits** - Load compiled C/C++/Rust binaries via ctypes
- **Soft Traits** - Install Python packages to `~/.ethos/traits/`

## Project Structure

```
ethos-lang/
├── main.py
├── requirements.txt
└── src/ethos/
    ├── cli.py          # REPL + file runner
    ├── lexer.py        # Sentence splitter + tokenizer
    ├── parser.py       # Transpiler (Ethos → Python)
    ├── executer.py     # Runtime + Hard Trait loader
    ├── stdlib_shim.py  # Forces stdlib into Nuitka binary
    └── version.py      # Version string
```

## What's Next

- [ ] Rust rewrite of the transpiler (planned for performance + memory safety)

Not planning right now: LSP, VSCode extensions, GUI IDE.

## Contributing

Solo project. Contributions welcome, especially:
- Hard Trait SDK bindings (Go, Java, Zig — I'm handling C/C++/Rust)
- Bug reports and fixes

Open an issue before starting large features to avoid duplicate work.

## Docs

- Full language reference: [DOCS.md](DOCS.md)
- Build instructions: [BUILDING.md](BUILDING.md)
- Standard library shims: [STDLIB_SHIMS.md](STDLIB_SHIMS.md)

## Related

- **Forge** (package manager): [github.com/AmanCode22/forge](https://github.com/AmanCode22/forge)
- **Ethos Foundry** (Collection of hard traits): [github.com/amancode22/ethos-foundry](https://github.com/amancode22/ethos-foundry)
