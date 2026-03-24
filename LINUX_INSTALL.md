# Installing Ethos on Linux

The binary on the [releases page](https://github.com/AmanCode22/ethos-lang/releases) is a standalone compiled executable — no Python required to run it. Pick whichever install method suits your distro.

---

## Option 1 — OBS Repository

The easiest option for supported distros. Your package manager handles installs and updates automatically.

Click the link, pick your distro, and the page shows you the exact commands:

🔗 [Add repository and install ethos-lang](https://software.opensuse.org/download.html?project=home:AmanCode22&package=ethos-lang)

**Supported distros**

| Distribution | Architectures |
|---|---|
| openSUSE Leap 15.6 | x86_64 |
| Arch Linux | x86_64 |
| Debian 12 | i586, x86_64 |
| Debian 13 | x86_64 |
| Debian Unstable | x86_64 |
| Fedora 42 | aarch64, x86_64 |
| Fedora 43 | aarch64, x86_64 |
| Fedora Rawhide | x86_64 |
| openEuler 24.03 | aarch64, x86_64 |
| openSUSE Factory ARM | aarch64, armv7l |
| openSUSE Slowroll | i586, x86_64 |
| openSUSE Tumbleweed | i586, x86_64 |
| Ubuntu 24.04 | x86_64 |
| Ubuntu 25.04 | x86_64 |
| Ubuntu 25.10 | x86_64 |

> `ethos-lang` recommends `ethos-forge` — your package manager may offer to install it alongside. It's optional here but you'll probably want it eventually for managing Traits.

---

## Option 2 — AUR (Arch Linux)

Builds from source using Nuitka. You need `base-devel` and an AUR helper.

🔗 [AUR: ethos-lang](https://aur.archlinux.org/packages/ethos-lang)

```bash
# yay
yay -S ethos-lang

# paru
paru -S ethos-lang

# manually
git clone https://aur.archlinux.org/ethos-lang.git
cd ethos-lang
makepkg -si
```

> The PKGBUILD lists `ethos-forge` as `optdepends`. Install it separately with `yay -S ethos-forge` if you want it.

---

## Option 3 — Universal Tarball

Works on any Linux distro. The tarball from the [releases page](https://github.com/AmanCode22/ethos-lang/releases) ships **both ethos and forge** as pre-compiled binaries — one download, both tools.

Download `ethos-build.tar.gz` from the [releases page](https://github.com/AmanCode22/ethos-lang/releases), then:

```bash
tar -xzf ethos-build.tar.gz
cd ethos-build
chmod +x install.sh
sudo ./install.sh
```

Running with `sudo` copies `ethos` and `forge` to `/usr/local/bin/` — available for every user on the machine.

Running **without** `sudo` triggers a prompt asking if you want a local install instead. If you say yes, the binaries go to `~/bin/` and the installer adds that to your PATH in `.bashrc` automatically.

---

## Verify

```bash
ethos --version
```
