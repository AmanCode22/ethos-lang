# Installing Ethos on macOS

Pre-built binaries are standalone — no Python required at runtime.

---

## Option 1 — .pkg Installer (Recommended)

Single installer for both **Ethos and Forge**.

**Download** from [releases](https://github.com/AmanCode22/ethos-lang/releases) and double-click. Installs to `/usr/local/bin/`.

---

## Option 2 — Manual Install

**Download** standalone binaries from [releases](https://github.com/AmanCode22/ethos-lang/releases):

```bash
chmod +x ethos forge
sudo mv ethos /usr/local/bin/ethos
sudo mv forge /usr/local/bin/forge
```

**Verify:**

```bash
ethos --version
forge --version
```

---

## Option 3 — Build from Source

See [BUILDING.md](BUILDING.md) for native builds, universal binaries, and .pkg creation.

---

## Using Darling (Linux → macOS binary testing)

```bash
# Install Darling: https://docs.darlinghq.org/installation.html

darling shell
ethos --version
ethos myprogram.ethos
```

Darling is for testing only — build on real macOS for production.

---

## Verify

```bash
ethos --version
forge --version
```
