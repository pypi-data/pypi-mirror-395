import platform
import psutil
import cpuinfo
import subprocess
if platform.system() == "Windows":
    import winreg
    import ctypes
else:
    winreg = None
import os
from datetime import datetime
import re

# ---------------------------------------------------------------- FORMAT TEMPLATE ----------------------------------------------------------------

class FormatTemplate:

    @staticmethod
    def _check_value(value):
        if callable(value):
            return value()
        return value

    @staticmethod
    def type_1(symbol, name, value):
        value = FormatTemplate._check_value(value)
        return f"[{symbol}] {name}: {value}"
    
    @staticmethod
    def type_2(symbol, name, value):
        value = FormatTemplate._check_value(value)
        return f"({symbol}) {name}: {value}"
    
    @staticmethod
    def type_3(symbol, name, value):
        value = FormatTemplate._check_value(value)
        return "{" + f"{symbol}" + "} " + f"{name}: {value}"
    
    @staticmethod
    def type_4(symbol, name, value):
        value = FormatTemplate._check_value(value)
        return f"{symbol} {name}: {value}"


# ---------------------------------------------------------------- PRIVATE CHECK CLASSES ----------------------------------------------------------------

class _CheckCPU:
    """Interne Prüfungen für CPU"""
    def __init__(self, value):
        self._value = value

    def has_hyperthreading(self):
        try:
            cores = psutil.cpu_count(logical=False)
            threads = psutil.cpu_count(logical=True)
            return threads > cores
        except:
            return False

    def is_64bit(self):
        return "64" in platform.architecture()[0]


class _CheckGPU:
    """Interne Prüfungen für GPU"""
    def __init__(self, value):
        self._value = value

    def is_nvidia(self):
        return "nvidia" in self._value.lower()

    def is_amd(self):
        return "amd" in self._value.lower() or "radeon" in self._value.lower()


class _CheckRAM:
    """Interne Prüfungen für RAM"""
    def __init__(self, value):
        self._value = value

    def more_than(self, gb):
        return self._value > gb


class _CheckNetworkDevice:
    """Interne Prüfungen für Netzwerkgeräte"""
    def __init__(self, value):
        self._value = value.lower()

    def is_ethernet(self):
        return "ethernet" in self._value or "gigabit" in self._value or "lan" in self._value

    def is_wireless(self):
        return "wifi" in self._value or "wireless" in self._value or "802.11" in self._value


class _CheckMainboard:
    """Interne Prüfungen für Mainboard"""
    def __init__(self, value):
        self._value = value

    def is_asus(self):
        return "asus" in self._value.lower()

    def is_msi(self):
        return "msi" in self._value.lower()

    def is_gigabyte(self):
        return "gigabyte" in self._value.lower()


class _CheckBIOS:
    """Interne Prüfungen für BIOS"""
    def __init__(self, value):
        self._value = value

    def is_uefi(self):
        return "uefi" in self._value.lower() or "efi" in self._value.lower()


class _CheckOS:
    """Interne Prüfungen für OS"""
    def __init__(self, value):
        self._value = value

    def is_windows(self):
        return "windows" in self._value.lower()

    def is_linux(self):
        return "linux" in self._value.lower()

    def is_mac(self):
        return "darwin" in self._value.lower() or "mac" in self._value.lower()


# ---------------------------------------------------------------- WRAPPER CLASSES ----------------------------------------------------------------

class CPU:
    def __init__(self, value):
        self.cpu_name = value
        self.check = _CheckCPU(value)

    def __str__(self):
        return self.cpu_name

    def __repr__(self):
        return f"CPU('{self.cpu_name}')"


class GPU:
    def __init__(self, value):
        self.gpu_name = value
        self.check = _CheckGPU(value)

    def __str__(self):
        return self.gpu_name

    def __repr__(self):
        return f"GPU('{self.gpu_name}')"


class RAM:
    def __init__(self, gb):
        self.gb = gb
        self.check = _CheckRAM(gb)

    def __str__(self):
        return f"{self.gb} GB"

    def __repr__(self):
        return f"RAM({self.gb})"


class NetworkDevice:
    def __init__(self, name):
        self.name = name
        self.check = _CheckNetworkDevice(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"NetworkDevice('{self.name}')"


class Mainboard:
    def __init__(self, name):
        self.name = name
        self.check = _CheckMainboard(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Mainboard('{self.name}')"


class BIOS:
    def __init__(self, version):
        self.version = version
        self.check = _CheckBIOS(version)

    def __str__(self):
        return self.version

    def __repr__(self):
        return f"BIOS('{self.version}')"


class OS:
    def __init__(self, name):
        self.name = name
        self.check = _CheckOS(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"OS('{self.name}')"


# ---------------------------------------------------------------- GET FUNCTIONS ----------------------------------------------------------------

def get_cpu_name():
    """Get CPU name with fallback methods"""
    try:
        info = cpuinfo.get_cpu_info()
        if "brand_raw" in info and info["brand_raw"]:
            return CPU(info["brand_raw"])
        elif "ProcessorNameString" in info:
            return CPU(info["ProcessorNameString"])
    except:
        pass
    
    try:
        if platform.system() == "Windows":
            import wmi
            c = wmi.WMI()
            for processor in c.Win32_Processor():
                return CPU(processor.Name.strip())
        elif platform.system() == "Linux":
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if 'model name' in line:
                        return CPU(line.split(':')[1].strip())
        elif platform.system() == "Darwin":
            output = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"], 
                                            stderr=subprocess.DEVNULL).decode().strip()
            if output:
                return CPU(output)
    except:
        pass
    
    return CPU(platform.processor() or "Unknown CPU")


def get_cpu_driver_date():
    """Get CPU driver date from Windows Registry or system files"""
    try:
        if platform.system() == "Windows":
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                r"SYSTEM\CurrentControlSet\Enum\PCI\VEN_8086&DEV_*", 
                                0, winreg.KEY_READ)
            date_str, _ = winreg.QueryValueEx(key, "DriverDate")
            winreg.CloseKey(key)
            try:
                date_obj = datetime.strptime(date_str.split()[0], "%m/%d/%Y")
                return CPU(date_obj.strftime("%d/%m/%Y"))
            except:
                return CPU(date_str)
    except:
        pass
    
    try:
        if platform.system() == "Windows":
            import wmi
            c = wmi.WMI()
            for os_info in c.Win32_OperatingSystem():
                install_date = os_info.InstallDate
                if install_date:
                    date_str = install_date.split('.')[0]
                    date_obj = datetime.strptime(date_str[:8], "%Y%m%d")
                    return CPU(date_obj.strftime("%d/%m/%Y"))
        elif platform.system() == "Linux":
            # Check for microcode update date
            microcode_paths = [
                '/sys/devices/system/cpu/microcode/reload',
                '/sys/devices/system/cpu/cpu0/microcode/version'
            ]
            for path in microcode_paths:
                if os.path.exists(path):
                    mtime = os.path.getmtime(path)
                    date_obj = datetime.fromtimestamp(mtime)
                    return CPU(date_obj.strftime("%d/%m/%Y"))
        elif platform.system() == "Darwin":
            # Check system update history for Apple Silicon
            try:
                output = subprocess.check_output(["system_profiler", "SPInstallHistoryDataType"], 
                                                stderr=subprocess.DEVNULL).decode()
                for line in output.split('\n'):
                    if 'Install Date' in line:
                        date_str = line.split(':')[1].strip()
                        return CPU(date_str)
            except:
                pass
    except:
        pass
    
    return CPU("Unknown date")


def get_cpu_driver_url():
    """Get appropriate CPU driver URL based on detected CPU"""
    try:
        cpu = str(get_cpu_name()).lower()
        
        if "intel" in cpu:
            return CPU("https://downloadcenter.intel.com/product/80939/Intel-Processor-Identification-Utility")
        elif "amd" in cpu:
            return CPU("https://www.amd.com/en/support/chipsets/amd-socket-am4")
        elif "apple" in cpu or "m1" in cpu or "m2" in cpu or "m3" in cpu:
            return CPU("https://support.apple.com/downloads")
        elif "arm" in cpu or "qualcomm" in cpu:
            return CPU("https://developer.arm.com/downloads")
        
        if platform.system() == "Windows":
            return CPU("https://www.microsoft.com/en-us/windows/windows-update")
        elif platform.system() == "Linux":
            return CPU("https://kernel.org")
        elif platform.system() == "Darwin":
            return CPU("https://support.apple.com/software-update")
    except:
        pass
    
    return CPU("https://www.intel.com/content/www/us/en/download-center/home.html")


def get_gpu_name():
    """Get GPU name with multiple detection methods"""
    gpu_name = "Unknown GPU"
    
    try:
        if platform.system() == "Windows":
            import wmi
            c = wmi.WMI()
            for gpu in c.Win32_VideoController():
                if gpu.Name and gpu.Name.strip():
                    gpu_name = gpu.Name.strip()
                    break
    except:
        pass
    
    if gpu_name == "Unknown GPU":
        try:
            # Try nvidia-smi
            output = subprocess.check_output(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"], 
                                            stderr=subprocess.DEVNULL, shell=platform.system() == "Windows").decode().strip()
            if output:
                gpu_name = output
        except:
            pass
    
    if gpu_name == "Unknown GPU" and platform.system() == "Linux":
        try:
            # Use lspci for Linux
            output = subprocess.check_output(["lspci", "-v"], stderr=subprocess.DEVNULL).decode()
            for line in output.split('\n'):
                if "VGA compatible controller" in line or "3D controller" in line or "Display controller" in line:
                    parts = line.split(':')
                    if len(parts) > 2:
                        gpu_name = parts[2].strip()
                        break
        except:
            try:
                # Alternative: check /sys/class/drm
                drm_path = "/sys/class/drm/"
                if os.path.exists(drm_path):
                    for entry in os.listdir(drm_path):
                        if "card" in entry and not "-" in entry:
                            card_path = os.path.join(drm_path, entry, "device")
                            if os.path.exists(card_path):
                                vendor_path = os.path.join(card_path, "vendor")
                                if os.path.exists(vendor_path):
                                    with open(vendor_path, 'r') as f:
                                        vendor_id = f.read().strip()
                                        if "0x10de" in vendor_id:
                                            gpu_name = "NVIDIA Graphics"
                                        elif "0x1002" in vendor_id:
                                            gpu_name = "AMD Graphics"
                                        elif "0x8086" in vendor_id:
                                            gpu_name = "Intel Graphics"
            except:
                pass
    
    if gpu_name == "Unknown GPU" and platform.system() == "Darwin":
        try:
            # Use system_profiler for macOS
            output = subprocess.check_output(["system_profiler", "SPDisplaysDataType"], 
                                            stderr=subprocess.DEVNULL).decode()
            for line in output.split('\n'):
                if "Chipset Model" in line:
                    gpu_name = line.split(':')[1].strip()
                    break
                elif "Graphics" in line and "Intel" in line:
                    gpu_name = "Intel Integrated Graphics"
                    break
                elif "Graphics" in line and "Apple" in line:
                    gpu_name = "Apple Silicon Graphics"
                    break
        except:
            pass
    
    return GPU(gpu_name)


def get_gpu_driver_date():
    """Get GPU driver date"""
    try:
        if platform.system() == "Windows":
            import winreg
            try:
                # Try NVIDIA registry
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                    r"SOFTWARE\NVIDIA Corporation\Global\NVTweak", 
                                    0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
                driver_date, _ = winreg.QueryValueEx(key, "DriverDate")
                winreg.CloseKey(key)
                return GPU(driver_date)
            except:
                try:
                    # Try AMD registry
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                        r"SOFTWARE\AMD\Install", 
                                        0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
                    driver_date, _ = winreg.QueryValueEx(key, "InstallDate")
                    winreg.CloseKey(key)
                    return GPU(driver_date)
                except:
                    pass
            
            try:
                import wmi
                c = wmi.WMI()
                for gpu in c.Win32_VideoController():
                    if gpu.InstalledDriver and gpu.InstalledDriver.strip():
                        driver_path = gpu.InstalledDriver.strip()
                        if os.path.exists(driver_path):
                            mtime = os.path.getmtime(driver_path)
                            date_obj = datetime.fromtimestamp(mtime)
                            return GPU(date_obj.strftime("%d/%m/%Y"))
            except:
                pass
        elif platform.system() == "Linux":
            # Check for GPU driver module modification date
            modules = ["nvidia", "amdgpu", "radeon", "i915"]
            for module in modules:
                module_path = f"/lib/modules/{os.uname().release}/kernel/drivers/gpu/drm/{module}"
                if os.path.exists(module_path):
                    mtime = os.path.getmtime(module_path)
                    date_obj = datetime.fromtimestamp(mtime)
                    return GPU(date_obj.strftime("%d/%m/%Y"))
            
            # Check Xorg log
            xorg_log = "/var/log/Xorg.0.log"
            if os.path.exists(xorg_log):
                mtime = os.path.getmtime(xorg_log)
                date_obj = datetime.fromtimestamp(mtime)
                return GPU(date_obj.strftime("%d/%m/%Y"))
        elif platform.system() == "Darwin":
            # Check Metal driver
            metal_path = "/System/Library/Frameworks/Metal.framework"
            if os.path.exists(metal_path):
                mtime = os.path.getmtime(metal_path)
                date_obj = datetime.fromtimestamp(mtime)
                return GPU(date_obj.strftime("%d/%m/%Y"))
    except:
        pass
    
    return GPU("01/01/2023")


def get_gpu_driver_url():
    """Get GPU driver URL based on detected GPU"""
    try:
        gpu = str(get_gpu_name()).lower()
        
        if "nvidia" in gpu:
            return GPU("https://www.nvidia.com/Download/index.aspx")
        elif "amd" in gpu or "radeon" in gpu:
            return GPU("https://www.amd.com/en/support")
        elif "intel" in gpu:
            return GPU("https://downloadcenter.intel.com/product/80939/Graphics")
        elif "apple" in gpu or "silicon" in gpu:
            return GPU("https://support.apple.com/downloads/macos")
        
        if platform.system() == "Windows":
            return GPU("https://www.microsoft.com/en-us/windows/windows-update")
        elif platform.system() == "Linux":
            return GPU("https://nouveau.freedesktop.org/")
        elif platform.system() == "Darwin":
            return GPU("https://support.apple.com/software-update")
    except:
        pass
    
    return GPU("https://www.nvidia.com/Download/index.aspx")


def get_ram_storage():
    """Get total RAM in GB"""
    try:
        mem = psutil.virtual_memory()
        gb = round(mem.total / (1024**3))
        
        common_sizes = [4, 8, 16, 32, 64, 128, 256]
        for size in common_sizes:
            if gb <= size:
                gb = size
                break
        
        return RAM(gb)
    except:
        try:
            if platform.system() == "Windows":
                import wmi
                c = wmi.WMI()
                total = 0
                for mem in c.Win32_ComputerSystem():
                    total = int(mem.TotalPhysicalMemory) // (1024**3)
                return RAM(total)
            elif platform.system() == "Linux":
                with open('/proc/meminfo', 'r') as f:
                    for line in f:
                        if 'MemTotal' in line:
                            kb = int(line.split(':')[1].strip().split()[0])
                            gb = kb // (1024**2)
                            return RAM(gb)
            elif platform.system() == "Darwin":
                output = subprocess.check_output(["sysctl", "-n", "hw.memsize"]).decode().strip()
                bytes_total = int(output)
                gb = bytes_total // (1024**3)
                return RAM(gb)
        except:
            pass
        
        return RAM(8)


def get_network_device_name():
    """Get primary network device name"""
    try:
        if platform.system() == "Windows":
            import wmi
            c = wmi.WMI()
            for nic in c.Win32_NetworkAdapter(NetEnabled=True):
                if nic.Name and "virtual" not in nic.Name.lower() and "bluetooth" not in nic.Name.lower():
                    return NetworkDevice(nic.Name.strip())
        elif platform.system() == "Linux":
            try:
                # Try to get default route interface
                output = subprocess.check_output(["ip", "route", "show", "default"], 
                                                stderr=subprocess.DEVNULL).decode()
                if output:
                    interface = output.split()[4]
                    # Try to get driver info
                    try:
                        output = subprocess.check_output(["ethtool", "-i", interface], 
                                                        stderr=subprocess.DEVNULL).decode()
                        driver_name = ""
                        for line in output.split('\n'):
                            if 'driver:' in line:
                                driver_name = line.split(':')[1].strip()
                                break
                        if driver_name:
                            return NetworkDevice(f"{interface} ({driver_name})")
                    except:
                        pass
                    return NetworkDevice(interface)
            except:
                # Fallback to psutil
                for iface in psutil.net_if_stats():
                    if psutil.net_if_stats()[iface].isup:
                        return NetworkDevice(iface)
        elif platform.system() == "Darwin":
            try:
                output = subprocess.check_output(["networksetup", "-listallhardwareports"], 
                                                stderr=subprocess.DEVNULL).decode()
                current_device = ""
                for line in output.split('\n'):
                    if 'Device:' in line:
                        current_device = line.split(':')[1].strip()
                    elif 'Ethernet' in line or 'Wi-Fi' in line or 'AirPort' in line:
                        port_name = line.split(':')[1].strip()
                        return NetworkDevice(f"{port_name} ({current_device})")
            except:
                pass
    except:
        pass
    
    # Final fallback
    interfaces = psutil.net_if_addrs()
    for iface in interfaces:
        if iface and "lo" not in iface and "vbox" not in iface:
            return NetworkDevice(iface)
    
    return NetworkDevice("Ethernet Adapter")


def get_network_device_driver_date():
    """Get network driver date"""
    try:
        if platform.system() == "Windows":
            import winreg
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                    r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}", 
                                    0, winreg.KEY_READ)
                
                for i in range(100):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)
                        try:
                            driver_date, _ = winreg.QueryValueEx(subkey, "DriverDate")
                            if driver_date:
                                winreg.CloseKey(subkey)
                                winreg.CloseKey(key)
                                return NetworkDevice(driver_date)
                        except:
                            pass
                        winreg.CloseKey(subkey)
                    except:
                        break
                winreg.CloseKey(key)
            except:
                pass
        elif platform.system() == "Linux":
            # Check network driver module date
            try:
                interface = str(get_network_device_name()).split('(')[0].strip()
                driver_output = subprocess.check_output(["ethtool", "-i", interface], 
                                                       stderr=subprocess.DEVNULL).decode()
                driver_name = ""
                for line in driver_output.split('\n'):
                    if 'driver:' in line:
                        driver_name = line.split(':')[1].strip()
                        break
                
                if driver_name:
                    module_path = f"/lib/modules/{os.uname().release}/kernel/drivers/net"
                    if os.path.exists(module_path):
                        for root, dirs, files in os.walk(module_path):
                            for file in files:
                                if driver_name in file:
                                    full_path = os.path.join(root, file)
                                    mtime = os.path.getmtime(full_path)
                                    date_obj = datetime.fromtimestamp(mtime)
                                    return NetworkDevice(date_obj.strftime("%d/%m/%Y"))
            except:
                pass
    except:
        pass
    
    try:
        if platform.system() == "Windows":
            import wmi
            c = wmi.WMI()
            for os_info in c.Win32_OperatingSystem():
                install_date = os_info.InstallDate
                if install_date:
                    date_str = install_date.split('.')[0]
                    date_obj = datetime.strptime(date_str[:8], "%Y%m%d")
                    return NetworkDevice(date_obj.strftime("%d/%m/%Y"))
    except:
        pass
    
    return NetworkDevice("01/01/2023")


def get_network_device_driver_url():
    """Get network driver download URL"""
    try:
        device = str(get_network_device_name()).lower()
        
        if "intel" in device:
            return NetworkDevice("https://downloadcenter.intel.com/product/89859")
        elif "realtek" in device:
            return NetworkDevice("https://www.realtek.com/en/component/zoo/category/network-interface-controllers-10-100-1000m-gigabit-ethernet-pci-express-software")
        elif "broadcom" in device:
            return NetworkDevice("https://www.broadcom.com/support/download-search")
        elif "qualcomm" in device or "atheros" in device:
            return NetworkDevice("https://www.qualcomm.com/products/application/networking")
        elif "marvell" in device:
            return NetworkDevice("https://www.marvell.com/support/downloads.html")
        elif "apple" in device:
            return NetworkDevice("https://support.apple.com/downloads")
        
        if platform.system() == "Windows":
            return NetworkDevice("https://support.microsoft.com/en-us/windows")
        elif platform.system() == "Linux":
            return NetworkDevice("https://kernel.org")
        elif platform.system() == "Darwin":
            return NetworkDevice("https://support.apple.com/downloads")
    except:
        pass
    
    return NetworkDevice("https://downloadcenter.intel.com/product/89859")


def get_mainboard_name():
    """Get motherboard manufacturer and model"""
    try:
        if platform.system() == "Windows":
            import wmi
            c = wmi.WMI()
            for board in c.Win32_BaseBoard():
                if board.Manufacturer and board.Product:
                    name = f"{board.Manufacturer.strip()} {board.Product.strip()}"
                    if name and name != "  ":
                        return Mainboard(name)
        elif platform.system() == "Linux":
            try:
                # Try dmidecode first
                output = subprocess.check_output(["sudo", "dmidecode", "-t", "baseboard"], 
                                                stderr=subprocess.DEVNULL).decode()
                manufacturer = ""
                product = ""
                for line in output.split('\n'):
                    if 'Manufacturer:' in line:
                        manufacturer = line.split(':')[1].strip()
                    elif 'Product Name:' in line:
                        product = line.split(':')[1].strip()
                
                if manufacturer and product:
                    return Mainboard(f"{manufacturer} {product}")
            except:
                try:
                    # Try sysfs
                    with open('/sys/devices/virtual/dmi/id/board_vendor', 'r') as f:
                        manufacturer = f.read().strip()
                    with open('/sys/devices/virtual/dmi/id/board_name', 'r') as f:
                        product = f.read().strip()
                    if manufacturer and product:
                        return Mainboard(f"{manufacturer} {product}")
                except:
                    pass
            
            # Try to get from /proc/cpuinfo for ARM boards
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    content = f.read()
                    if 'Raspberry Pi' in content:
                        return Mainboard("Raspberry Pi Foundation Raspberry Pi")
                    elif 'Hardware' in content:
                        for line in content.split('\n'):
                            if 'Hardware' in line:
                                hardware = line.split(':')[1].strip()
                                return Mainboard(hardware)
            except:
                pass
        elif platform.system() == "Darwin":
            # For Apple, return the Mac model
            try:
                output = subprocess.check_output(["sysctl", "-n", "hw.model"], 
                                                stderr=subprocess.DEVNULL).decode().strip()
                if output:
                    return Mainboard(f"Apple {output}")
            except:
                pass
            
            try:
                output = subprocess.check_output(["system_profiler", "SPHardwareDataType"], 
                                                stderr=subprocess.DEVNULL).decode()
                model = ""
                for line in output.split('\n'):
                    if 'Model Name:' in line or 'Model Identifier:' in line:
                        model = line.split(':')[1].strip()
                        return Mainboard(f"Apple {model}")
            except:
                pass
    except:
        pass
    
    return Mainboard("Unknown Motherboard")


def get_bios_version():
    """Get BIOS/UEFI version"""
    try:
        if platform.system() == "Windows":
            import wmi
            c = wmi.WMI()
            for bios in c.Win32_BIOS():
                if bios.SMBIOSBIOSVersion:
                    version = bios.SMBIOSBIOSVersion.strip()
                    is_uefi = False
                    try:
                        if kernel32.GetFirmwareType(ctypes.byref(firmware_type)):
                            if firmware_type.value == 2:
                                is_uefi = True
                    except:
                        pass
                    
                    if is_uefi:
                        return BIOS(f"UEFI {version}")
                    else:
                        return BIOS(f"BIOS {version}")
        elif platform.system() == "Linux":
            try:
                # Try dmidecode
                output = subprocess.check_output(["sudo", "dmidecode", "-t", "bios"], 
                                                stderr=subprocess.DEVNULL).decode()
                version = ""
                for line in output.split('\n'):
                    if 'Version:' in line:
                        version = line.split(':')[1].strip()
                        break
                
                if version:
                    # Check if UEFI
                    if os.path.exists('/sys/firmware/efi'):
                        return BIOS(f"UEFI {version}")
                    else:
                        return BIOS(f"BIOS {version}")
            except:
                try:
                    # Try sysfs
                    with open('/sys/devices/virtual/dmi/id/bios_version', 'r') as f:
                        version = f.read().strip()
                    if version:
                        if os.path.exists('/sys/firmware/efi'):
                            return BIOS(f"UEFI {version}")
                        else:
                            return BIOS(f"BIOS {version}")
                except:
                    pass
                
                # For ARM devices
                try:
                    with open('/proc/device-tree/model', 'r') as f:
                        model = f.read().strip()
                        return BIOS(f"Bootloader - {model}")
                except:
                    pass
        elif platform.system() == "Darwin":
            try:
                # macOS uses EFI
                output = subprocess.check_output(["system_profiler", "SPHardwareDataType"], 
                                                stderr=subprocess.DEVNULL).decode()
                for line in output.split('\n'):
                    if 'Boot ROM Version:' in line:
                        version = line.split(':')[1].strip()
                        return BIOS(f"EFI {version}")
                    elif 'SMC Version:' in line:
                        version = line.split(':')[1].strip()
                        return BIOS(f"SMC {version}")
            except:
                pass
    except:
        pass
    
    return BIOS("Unknown Firmware")


def get_os_name():
    """Get operating system name"""
    try:
        system = platform.system()
        if system == "Windows":
            import wmi
            c = wmi.WMI()
            for os_info in c.Win32_OperatingSystem():
                return OS(os_info.Caption.strip())
        elif system == "Linux":
            try:
                # Try distro module first
                import distro
                name = distro.name(pretty=True)
                if name:
                    return OS(name)
            except:
                pass
            
            # Fallback to /etc/os-release
            if os.path.exists('/etc/os-release'):
                with open('/etc/os-release', 'r') as f:
                    content = f.read()
                    name_match = re.search(r'PRETTY_NAME="([^"]+)"', content)
                    if name_match:
                        return OS(name_match.group(1))
                    
                    name_match = re.search(r'NAME="([^"]+)"', content)
                    version_match = re.search(r'VERSION="([^"]+)"', content)
                    if name_match and version_match:
                        return OS(f"{name_match.group(1)} {version_match.group(1)}")
            
            # Check for specific distributions
            if os.path.exists('/etc/redhat-release'):
                with open('/etc/redhat-release', 'r') as f:
                    return OS(f.read().strip())
            elif os.path.exists('/etc/debian_version'):
                with open('/etc/debian_version', 'r') as f:
                    debian_version = f.read().strip()
                    return OS(f"Debian {debian_version}")
        elif system == "Darwin":
            try:
                product_name = subprocess.check_output(["sw_vers", "-productName"], 
                                                      stderr=subprocess.DEVNULL).decode().strip()
                product_version = subprocess.check_output(["sw_vers", "-productVersion"], 
                                                         stderr=subprocess.DEVNULL).decode().strip()
                return OS(f"{product_name} {product_version}")
            except:
                pass
    except:
        pass
    
    return OS(platform.platform(terse=True))


def get_os_release():
    """Get OS release version"""
    try:
        if platform.system() == "Windows":
            import wmi
            c = wmi.WMI()
            for os_info in c.Win32_OperatingSystem():
                version = os_info.Version.strip()
                build = os_info.BuildNumber.strip()
                return OS(f"{version} (Build {build})")
        elif platform.system() == "Linux":
            try:
                import distro
                version = distro.version(pretty=True)
                if version:
                    return OS(version)
            except:
                if os.path.exists('/etc/os-release'):
                    with open('/etc/os-release', 'r') as f:
                        for line in f:
                            if 'VERSION_ID=' in line:
                                version = line.split('=')[1].strip().strip('"')
                                return OS(version)
            
            # Kernel version as fallback
            return OS(platform.release())
        elif platform.system() == "Darwin":
            try:
                product_version = subprocess.check_output(["sw_vers", "-productVersion"], 
                                                         stderr=subprocess.DEVNULL).decode().strip()
                build_version = subprocess.check_output(["sw_vers", "-buildVersion"], 
                                                       stderr=subprocess.DEVNULL).decode().strip()
                return OS(f"{product_version} ({build_version})")
            except:
                pass
    except:
        pass
    
    return OS(platform.release())


def get_os_version():
    """Get detailed OS version"""
    try:
        if platform.system() == "Windows":
            import wmi
            c = wmi.WMI()
            for os_info in c.Win32_OperatingSystem():
                version_info = f"{os_info.Version} Build {os_info.BuildNumber}"
                if os_info.ServicePackMajorVersion:
                    version_info += f" SP{os_info.ServicePackMajorVersion}"
                return OS(version_info.strip())
        elif platform.system() == "Linux":
            try:
                output = subprocess.check_output(["lsb_release", "-a"], 
                                                stderr=subprocess.DEVNULL).decode()
                description = ""
                release = ""
                codename = ""
                for line in output.split('\n'):
                    if 'Description:' in line:
                        description = line.split(':')[1].strip()
                    elif 'Release:' in line:
                        release = line.split(':')[1].strip()
                    elif 'Codename:' in line:
                        codename = line.split(':')[1].strip()
                
                if description and release:
                    if codename:
                        return OS(f"{description} ({release} - {codename})")
                    else:
                        return OS(f"{description} ({release})")
            except:
                pass
            
            # Try uname
            kernel_version = platform.release()
            return OS(f"Linux Kernel {kernel_version}")
        elif platform.system() == "Darwin":
            try:
                product_name = subprocess.check_output(["sw_vers", "-productName"], 
                                                      stderr=subprocess.DEVNULL).decode().strip()
                product_version = subprocess.check_output(["sw_vers", "-productVersion"], 
                                                         stderr=subprocess.DEVNULL).decode().strip()
                build_version = subprocess.check_output(["sw_vers", "-buildVersion"], 
                                                       stderr=subprocess.DEVNULL).decode().strip()
                kernel_version = platform.release()
                return OS(f"{product_name} {product_version} (Build {build_version}, Kernel {kernel_version})")
            except:
                pass
    except:
        pass
    
    return OS(platform.version())


def get_os_url():
    """Get OS support/download URL"""
    try:
        system = platform.system()
        
        if system == "Windows":
            version = platform.version()
            if "10.0.2" in version or "10.0.22" in version:
                return OS("https://www.microsoft.com/en-us/software-download/windows11")
            elif "10.0" in version:
                return OS("https://www.microsoft.com/en-us/software-download/windows10")
            else:
                return OS("https://support.microsoft.com/en-us/windows")
        elif system == "Linux":
            try:
                import distro
                distro_id = distro.id()
                if distro_id == "ubuntu":
                    return OS("https://ubuntu.com/download")
                elif distro_id == "debian":
                    return OS("https://www.debian.org/distrib/")
                elif distro_id == "fedora":
                    return OS("https://getfedora.org/")
                elif distro_id == "centos" or distro_id == "rocky":
                    return OS("https://www.rockylinux.org/download/")
                elif distro_id == "arch":
                    return OS("https://archlinux.org/download/")
                elif distro_id == "raspbian":
                    return OS("https://www.raspberrypi.com/software/")
                elif distro_id == "alpine":
                    return OS("https://alpinelinux.org/downloads/")
                else:
                    return OS("https://kernel.org/")
            except:
                # Check for specific files
                if os.path.exists("/etc/redhat-release"):
                    return OS("https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux")
                elif os.path.exists("/etc/debian_version"):
                    return OS("https://www.debian.org/distrib/")
                else:
                    return OS("https://kernel.org/")
        elif system == "Darwin":
            return OS("https://support.apple.com/downloads/macos")
        else:
            return OS("https://www.microsoft.com/en-us/windows")
    except:
        pass
    
    return OS("https://www.microsoft.com/en-us/windows")