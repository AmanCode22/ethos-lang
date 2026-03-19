# Building
## Prerequisites
- Python3.10+(with pip installed) in path
- Git installed(Or you can download the repo zip also)
## Building on linux
You must install the basic developement packages reqiured by nuitka to build ethos according to your distro
- Ubuntu/Debian and derrivatives
```
sudo apt update
sudo apt install python3 python3-dev build-essential patchelf
```
- Fedora/RHEL and derrivaties
```
sudo dnf install python3 python3-devel gcc gcc-c++ patchelf
```
- Arch Linux/Manjaro and derrivaties
```
sudo pacman -S python base-devel patchelf
```

After this you can build using given commands
```
git clone https://github.com/amancode22/ethos-lang # you can  skip this if you have zip(you must extract it yourself)
cd ethos-lang/
python3 -m venv ethos_build_env
./ethos_build_env/bin/pip install -r requirements.txt
mkdir binary/
./ethos_build_env/bin/python3 -m nuitka --standalone --onefile -o binary/ethos main.py
```
After this completes you would have a compiled binary of ethos in binary folder.
Use it  ```./binary/ethos```
## Building on Windows
Would be added soon
## Building on Macos
Would be added soon.
## Building on Android(Termux)
Termux support is currently in future roadmap and would be added after project reaches stable release.
