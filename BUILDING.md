# Building ethos-lang

## Prerequisites

- Python 3.10+ (with pip)
- Git

---

## Linux

**Install build dependencies:**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-dev build-essential patchelf

# Fedora/RHEL
sudo dnf install python3 python3-devel gcc gcc-c++ patchelf

# Arch/Manjaro
sudo pacman -S python base-devel patchelf
```

**Build:**

```bash
git clone https://github.com/AmanCode22/ethos-lang
cd ethos-lang/
python3 -m venv ethos_build_env
./ethos_build_env/bin/pip install -r requirements.txt
mkdir binary/
unset LDFLAGS
./ethos_build_env/bin/python3 -m nuitka --standalone --onefile --unstripped -o binary/ethos main.py
```

Output: `binary/ethos`

> `--unstripped` is required. Without it, the system may strip the binary after Nuitka builds it, breaking the self-extracting payload.

---

## Windows

```powershell
pip install --upgrade pip
pip install -r requirements.txt
python -m nuitka --assume-yes-for-downloads --onefile main.py --output-filename=ethos.exe
```

Output: `ethos.exe`

---

## macOS

**Install dependencies:**

```bash
xcode-select --install
brew install python@3.12 ccache
```

### Native Build (single architecture)

```bash
git clone https://github.com/AmanCode22/ethos-lang
cd ethos-lang/
python3 -m venv ethos_build_env
./ethos_build_env/bin/pip install -r requirements.txt
mkdir binary/
./ethos_build_env/bin/python3 -m nuitka --standalone --onefile --unstripped -o binary/ethos main.py
```

Produces `arm64` binary on Apple Silicon, `x86_64` on Intel.

### Universal Binary (arm64 + x86_64)

Nuitka doesn't produce universal binaries directly. Build both architectures separately, then combine with `lipo`.

**Step 1 — Build arm64 (on Apple Silicon):**

```bash
arch -arm64 ./ethos_build_env/bin/python3 -m nuitka --standalone --onefile --unstripped -o binary/ethos-arm64 main.py
```

**Step 2 — Build x86_64 (on Intel or via Rosetta):**

```bash
arch -x86_64 /usr/bin/python3 -m venv ethos_build_env_x86
arch -x86_64 ./ethos_build_env_x86/bin/pip install -r requirements.txt
arch -x86_64 ./ethos_build_env_x86/bin/python3 -m nuitka --standalone --onefile --unstripped -o binary/ethos-x86_64 main.py
```

**Step 3 — Combine:**

```bash
lipo -create binary/ethos-arm64 binary/ethos-x86_64 -output binary/ethos
```

**Verify:**

```bash
file binary/ethos
# Should show: Mach-O universal binary with 2 architectures
lipo -info binary/ethos
```

### Building .pkg Installer

Requires `pkgbuild` and `productbuild` (Xcode command line tools).

```bash
mkdir -p pkg_root/usr/local/bin
cp binary/ethos pkg_root/usr/local/bin/ethos
cp /path/to/forge/binary/forge pkg_root/usr/local/bin/forge
chmod +x pkg_root/usr/local/bin/*

pkgbuild \
  --root pkg_root \
  --identifier com.amancode22.ethos \
  --install-location / \
  ethos-component.pkg

productbuild \
  --component ethos-component.pkg /usr/local \
  --identifier com.amancode22.ethos \
  Ethos-macos.pkg
```

Output: `Ethos-macos.pkg`

### Using Darling (Linux → macOS binary testing)

```bash
# Install Darling: https://docs.darlinghq.org/installation.html

darling shell
./ethos --version
```

Darling is for running/testing only — build on real macOS for production binaries.

---

## Android (Termux)

Just zipapps due to linker issue so no build required

---

For OBS spec files, Debian control files, and Windows installer scripts, see [ethos-builder](https://github.com/AmanCode22/ethos-builder).
