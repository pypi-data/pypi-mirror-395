[![z30lib Repository](https://img.shields.io/badge/GitHub-Repository-0ab5e2?style=flat&logo=github&logoColor=white)](https://github.com/Z30-Development/z30lib)

[![Join our Discord](https://img.shields.io/badge/Discord-Join%20Server-7289DA?logo=discord&logoColor=white)](https://discord.gg/z30) [![PyPI](https://img.shields.io/pypi/v/z30lib?color=blue&logo=python&logoColor=white)](https://pypi.org/project/z30lib/)

[![Windows](https://img.shields.io/badge/OS-Windows-333333?style=flat&logo=icloud&logoColor=white)](https://www.microsoft.com/de-de/software-download/windows11)
[![Linux](https://img.shields.io/badge/OS-Linux-333333?style=flat&logo=linux&logoColor=white)](https://www.linux.org/pages/download/)
[![macOS](https://img.shields.io/badge/OS-MacOS-333333?style=flat&logo=apple&logoColor=white)](https://support.apple.com/de-de/102662)

# Z30 Library for Python

Cross-platform Python library to retrieve detailed system and hardware information.

---

## Overview

**Z30Lib** is a versatile Python library designed to provide detailed system and hardware information across multiple platforms, including **Windows**, **Linux**, and **macOS**. It allows developers to easily access CPU, GPU, RAM, motherboard, BIOS, OS, and network device details with a simple and consistent API.

---

## Features

- Detect **CPU**, **GPU**, and **RAM** specifications
- Check **motherboard** and **BIOS** information
- Identify **operating system** version and type
- Retrieve **network device** details and drivers
- Cross-platform support (**Windows**, **Linux**, **macOS**)
- Optional modules for **network info** and **internet speed tests**

Z30Lib is perfect for developers building system monitoring tools, hardware diagnostics applications, or cross-platform utilities that require accurate hardware and system insights.

---

## Installation

Install via pip:

```bash
pip install z30lib
````

Or, for Python 3 specifically:

```bash
pip3 install z30lib
```

---

## Usage

Here is a simple example to get system information:

```python
from z30lib import get_cpu_name, get_gpu_name, get_ram_storage, get_os_name

cpu = get_cpu_name()
gpu = get_gpu_name()
ram = get_ram_storage()
os_info = get_os_name()

print(f"CPU: {cpu}")
print(f"GPU: {gpu}")
print(f"RAM: {ram}")
print(f"OS: {os_info}")
```

Optional features:

```python
from z30lib import get_network_device_name, speedtest_download

network = get_network_device_name()
print(f"Network Device: {network}")

# If speedtest module is installed
# speed = speedtest_download()
# print(f"Internet Speed: {speed} Mbps")
```

---

## Optional Dependencies

* **Network info:** `pip install z30lib[network]`
* **Speedtest:** `pip install z30lib[speedtest]`

---

## Supported Platforms

* Windows 10+
* Linux (major distributions)
* macOS

---

## License

MIT License © Z30-Development

---

## Links

* **Homepage:** [https://github.com/Z30-Development/z30lib](https://github.com/Z30-Development/z30lib)
* **Issue Tracker:** [https://github.com/Z30-Development/z30lib/issues](https://github.com/Z30-Development/z30lib/issues)

---

## How to Contribute

Feel free to submit issues or pull requests. Contributions, suggestions, and bug reports are welcome!
