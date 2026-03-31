# Installing Ethos on Linux

Pre-built binaries are standalone — no Python required at runtime.

---

## Option 1 — OBS Repository (Recommended)

Automatic updates via your package manager.

**Add repo and install:** [software.opensuse.org/download.html?project=home:AmanCode22&package=ethos-lang](https://software.opensuse.org/download.html?project=home:AmanCode22&package=ethos-lang)

**Supported distros:**

| Distribution | Architectures |
|--------------|---------------|
| openSUSE Leap 15.6 | x86_64 |
| Arch Linux | x86_64 |
| Debian 12/13/Unstable | i586, x86_64 |
| Fedora 42/43/Rawhide | aarch64, x86_64 |
| openEuler 24.03 | aarch64, x86_64 |
| openSUSE Factory/Tumbleweed/Slowroll | aarch64, armv7l, i586, x86_64 |
| Ubuntu 24.04/25.04/25.10 | x86_64 |

`ethos-lang` recommends `ethos-forge` (optional package manager).

---

## Option 2 — AUR (Arch Linux)

```bash
# yay
yay -S ethos-lang

# paru
paru -S ethos-lang

# Manual
git clone https://aur.archlinux.org/ethos-lang.git
cd ethos-lang
makepkg -si
```

`ethos-forge` is available as `optdepends`.

---

## Option 3 — Universal Tarball

Works on any distro. Includes both `ethos` and `forge`.

**Download** `ethos-build.tar.gz` from [releases](https://github.com/AmanCode22/ethos-lang/releases), then:

```bash
tar -xzf ethos-build.tar.gz
cd ethos-build
chmod +x install.sh
sudo ./install.sh
```

Installs to `/usr/local/bin/`. Without `sudo`, installs to `~/bin/` and updates `.bashrc`.

---

## Verify

```bash
ethos --version
```
