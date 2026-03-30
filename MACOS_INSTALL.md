# Installing Ethos on macOS

The pre-built binary on the [releases page](https://github.com/AmanCode22/ethos-lang/releases) is a standalone compiled executable — no Python required to run it.

---

## Option 1 — .pkg Installer (recommended)

The `.pkg` on the [releases page](https://github.com/AmanCode22/ethos-lang/releases) installs both **Ethos and Forge** in one shot. There is no separate Forge `.pkg` — they ship together.

Download macos pkg files for your architecture and double-click it. The installer copies `ethos` and `forge` to `/usr/local/bin/` and they're immediately available in your terminal.

---

## Option 2 — Manual install from pre-built binary

Download the standalone `ethos` binary from the [releases page](https://github.com/AmanCode22/ethos-lang/releases), then:

```bash
chmod +x ethos
sudo mv ethos /usr/local/bin/ethos
```

Do the same for `forge` from the [Forge releases page](https://github.com/AmanCode22/forge/releases):

```bash
chmod +x forge
sudo mv forge /usr/local/bin/forge
```

Verify:

```bash
ethos --version
forge --version
```

---

## Option 3 — Build from source

See [BUILDING.md](BUILDING.md) for the full build instructions including native builds, universal binaries, cross-compilation via Rosetta, and how to produce the `.pkg` installer yourself.

---

## DarlingHQ (running macOS Ethos binaries on Linux)

[Darling](https://www.darlinghq.org/) is a macOS compatibility layer for Linux. If you want to run the macOS Ethos binary on a Linux machine:

```bash
# Install Darling for your distro — see https://docs.darlinghq.org/installation.html

# Enter the Darling shell
darling shell

# Run ethos inside Darling
ethos --version
ethos myprogram.ethos
```

Darling is useful for testing and running `.ethos` programs, but building the macOS binary itself should be done on a real Mac. See [BUILDING.md](BUILDING.md) for build steps.

---

## Verify

```bash
ethos --version
forge --version
```
