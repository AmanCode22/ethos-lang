# Building ethos-lang

## Prerequisites

- Python 3.10 or newer (with pip)
- Git (or download the repo zip and extract it yourself)

---

## Linux

Install the packages Nuitka needs for your distro first:

**Ubuntu / Debian and derivatives**
```bash
sudo apt update
sudo apt install python3 python3-dev build-essential patchelf
```

**Fedora / RHEL and derivatives**
```bash
sudo dnf install python3 python3-devel gcc gcc-c++ patchelf
```

**Arch Linux / Manjaro and derivatives**
```bash
sudo pacman -S python base-devel patchelf
```

Then build:

```bash
git clone https://github.com/AmanCode22/ethos-lang
cd ethos-lang/
python3 -m venv ethos_build_env
./ethos_build_env/bin/pip install -r requirements.txt
mkdir binary/
unset LDFLAGS
./ethos_build_env/bin/python3 -m nuitka --standalone --onefile --unstripped -o binary/ethos main.py
```

The compiled binary lands in `binary/ethos`.

> `--unstripped` is important — without it the environment may strip the binary after Nuitka builds it, which destroys the self-extracting payload and causes a `couldn't find attached data header` error at runtime.

---

## Windows

Open PowerShell in the source directory:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
python -m nuitka --assume-yes-for-downloads --onefile main.py --output-filename=ethos.exe
```

You get `ethos.exe` in the current folder.

---

## macOS

You need Python 3.10+ and the Xcode command line tools:

```bash
xcode-select --install
```

Then install Nuitka's dependencies. The simplest way is via Homebrew:

```bash
brew install python@3.12 ccache
```

### Native build (build for the architecture you're running on)

This works on both Apple Silicon (arm64) and Intel (x86_64) Macs. Run this on the machine you want to build for:

```bash
git clone https://github.com/AmanCode22/ethos-lang
cd ethos-lang/
python3 -m venv ethos_build_env
./ethos_build_env/bin/pip install -r requirements.txt
mkdir binary/
./ethos_build_env/bin/python3 -m nuitka --standalone --onefile --unstripped -o binary/ethos main.py
```

This produces a binary for the architecture you're currently on — arm64 if you're on Apple Silicon, x86_64 if you're on Intel.

### Building a Universal Binary (arm64 + x86_64 in one file)

Nuitka doesn't natively produce universal binaries directly, so the approach is to build both architectures separately and then combine them with `lipo`. You need access to both architectures — either two machines, or an Intel Mac using Rosetta.

**Step 1 — build the arm64 binary** (on an Apple Silicon Mac):

```bash
arch -arm64 ./ethos_build_env/bin/python3 -m nuitka --standalone --onefile --unstripped -o binary/ethos-arm64 main.py
```

**Step 2 — build the x86_64 binary** (on an Intel Mac, or on Apple Silicon using Rosetta):

```bash
# On Apple Silicon using Rosetta:
arch -x86_64 /usr/bin/python3 -m venv ethos_build_env_x86
arch -x86_64 ./ethos_build_env_x86/bin/pip install -r requirements.txt
arch -x86_64 ./ethos_build_env_x86/bin/python3 -m nuitka --standalone --onefile --unstripped -o binary/ethos-x86_64 main.py
```

**Step 3 — combine with lipo:**

```bash
lipo -create binary/ethos-arm64 binary/ethos-x86_64 -output binary/ethos
```

**Verify:**

```bash
file binary/ethos
# Should show: Mach-O universal binary with 2 architectures: [x86_64] [arm64]
lipo -info binary/ethos
```

### Building x86_64 on x86_64 (Intel Mac)

Straightforward — just run the native build above on an Intel Mac. No extra flags needed.

### Building arm64 on arm64 (Apple Silicon)

Same — just run the native build above on an Apple Silicon Mac.

### Cross-compiling x86_64 on Apple Silicon (Rosetta)

```bash
# Install an x86_64 Python via Homebrew under Rosetta
arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
arch -x86_64 /usr/local/bin/brew install python@3.12

arch -x86_64 /usr/local/bin/python3.12 -m venv ethos_build_env_x86
arch -x86_64 ./ethos_build_env_x86/bin/pip install -r requirements.txt
arch -x86_64 ./ethos_build_env_x86/bin/python3 -m nuitka --standalone --onefile --unstripped -o binary/ethos-x86_64 main.py
```

### Cross-compiling arm64 on Intel (not recommended)

True cross-compilation from x86_64 to arm64 on macOS is not straightforward with Nuitka. The recommended approach is to build natively on Apple Silicon or use a CI runner with an arm64 Mac (GitHub Actions has `macos-14` which runs on Apple Silicon).

### Building a .pkg installer for macOS

The `.pkg` installer ships both `ethos` and `forge` together. There is no separate Forge `.pkg`. To build the installer yourself you need `pkgbuild` and `productbuild`, which come with Xcode command line tools.

First build both binaries (ethos and forge), then:

```bash
# Create staging directory
mkdir -p pkg_root/usr/local/bin
cp binary/ethos pkg_root/usr/local/bin/ethos
cp /path/to/forge/binary/forge pkg_root/usr/local/bin/forge
chmod +x pkg_root/usr/local/bin/ethos
chmod +x pkg_root/usr/local/bin/forge

# Build the component package
pkgbuild \
  --root pkg_root \
  --identifier com.amancode22.ethos \
  --version 0.3.0 \
  --install-location / \
  ethos-component.pkg

# Build the final distribution package
productbuild \
  --component ethos-component.pkg /usr/local \
  --identifier com.amancode22.ethos \
  --version 0.3.0 \
  Ethos-v0.3.0-macos.pkg
```

The resulting `Ethos-v0.3.0-macos.pkg` installs both `ethos` and `forge` to `/usr/local/bin/`.

> You can also use the pre-built binaries from the [releases page](https://github.com/AmanCode22/ethos-lang/releases) instead of building from source — just swap them into `pkg_root/usr/local/bin/` and run the pkgbuild steps above.

### Using DarlingHQ (running macOS binaries on Linux)

[Darling](https://www.darlinghq.org/) is a macOS compatibility layer for Linux. If you have Darling installed and want to run or test the macOS Ethos binary on Linux:

```bash
# Install Darling — see https://docs.darlinghq.org/installation.html for your distro

# Enter the Darling shell
darling shell

# Inside the Darling shell, run ethos normally
./ethos --version
./ethos myprogram.ethos
```

Building the macOS binary itself inside Darling is not recommended — Darling doesn't expose the full Xcode toolchain needed by Nuitka. Build the macOS binary on a real Mac and use Darling only for running and testing it on Linux.

---

## Android (Termux)

Coming soon.

---

For packaging scripts, OBS spec files, Debian control files, and the Windows installer script, see [ethos-builder](https://github.com/AmanCode22/ethos-builder).
