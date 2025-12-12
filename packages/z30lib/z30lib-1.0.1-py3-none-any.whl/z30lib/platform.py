import platform
import psutil
import cpuinfo
import subprocess
import winreg
import os
from datetime import datetime

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
        elif "apple" in cpu:
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
            output = subprocess.check_output(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"], 
                                            shell=True, stderr=subprocess.DEVNULL).decode().strip()
            if output and "NVIDIA" in output:
                gpu_name = output
        except:
            pass
    
    if gpu_name == "Unknown GPU" and platform.system() == "Linux":
        try:
            output = subprocess.check_output(["lspci", "-v"], stderr=subprocess.DEVNULL).decode()
            for line in output.split('\n'):
                if "VGA compatible controller" in line or "3D controller" in line:
                    parts = line.split(':')
                    if len(parts) > 2:
                        gpu_name = parts[2].strip()
                        break
        except:
            pass
    
    if gpu_name == "Unknown GPU" and platform.system() == "Darwin":
        try:
            output = subprocess.check_output(["system_profiler", "SPDisplaysDataType"], 
                                            stderr=subprocess.DEVNULL).decode()
            for line in output.split('\n'):
                if "Chipset Model" in line:
                    gpu_name = line.split(':')[1].strip()
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
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                    r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000", 
                                    0, winreg.KEY_READ)
                driver_date, _ = winreg.QueryValueEx(key, "DriverDate")
                winreg.CloseKey(key)
                
                try:
                    date_parts = driver_date.split('-')
                    if len(date_parts) == 3:
                        month, day, year = date_parts
                        date_obj = datetime(int(year), int(month), int(day))
                        return GPU(date_obj.strftime("%d/%m/%Y"))
                except:
                    return GPU(driver_date)
            except:
                pass
            
            try:
                import wmi
                import os
                from datetime import datetime
                
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
        elif "apple" in gpu:
            return GPU("https://support.apple.com/downloads/macos")
        
        if platform.system() == "Windows":
            return GPU("https://www.microsoft.com/en-us/windows/windows-update")
        elif platform.system() == "Linux":
            return GPU("https://nouveau.freedesktop.org/")
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
                output = subprocess.check_output(["ip", "route", "show", "default"], 
                                                stderr=subprocess.DEVNULL).decode()
                if output:
                    interface = output.split()[4]
                    output = subprocess.check_output(["ethtool", "-i", interface], 
                                                    stderr=subprocess.DEVNULL).decode()
                    for line in output.split('\n'):
                        if 'driver:' in line:
                            driver_name = line.split(':')[1].strip()
                            return NetworkDevice(f"{interface} ({driver_name})")
                    return NetworkDevice(interface)
            except:
                for iface in psutil.net_if_stats():
                    if psutil.net_if_stats()[iface].isup:
                        return NetworkDevice(iface)
        elif platform.system() == "Darwin":
            output = subprocess.check_output(["networksetup", "-listallhardwareports"], 
                                            stderr=subprocess.DEVNULL).decode()
            current_device = ""
            for line in output.split('\n'):
                if 'Device:' in line:
                    current_device = line.split(':')[1].strip()
                elif 'Ethernet' in line or 'Wi-Fi' in line:
                    return NetworkDevice(f"{line.split(':')[1].strip()} ({current_device})")
    except:
        pass
    
    interfaces = psutil.net_if_addrs()
    for iface in interfaces:
        if iface and "lo" not in iface:
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
        
        if platform.system() == "Windows":
            return NetworkDevice("https://support.microsoft.com/en-us/windows")
        elif platform.system() == "Linux":
            return NetworkDevice("https://kernel.org")
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
                    with open('/sys/devices/virtual/dmi/id/board_vendor', 'r') as f:
                        manufacturer = f.read().strip()
                    with open('/sys/devices/virtual/dmi/id/board_name', 'r') as f:
                        product = f.read().strip()
                    if manufacturer and product:
                        return Mainboard(f"{manufacturer} {product}")
                except:
                    pass
        elif platform.system() == "Darwin":
            output = subprocess.check_output(["system_profiler", "SPHardwareDataType"], 
                                            stderr=subprocess.DEVNULL).decode()
            model = ""
            for line in output.split('\n'):
                if 'Model Name:' in line:
                    model = line.split(':')[1].strip()
                    return Mainboard(f"Apple {model}")
    except:
        pass
    
    return Mainboard("ASUS ROG STRIX")


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
                        import ctypes
                        kernel32 = ctypes.windll.kernel32
                        firmware_type = ctypes.c_uint32()
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
                output = subprocess.check_output(["sudo", "dmidecode", "-t", "bios"], 
                                                stderr=subprocess.DEVNULL).decode()
                version = ""
                for line in output.split('\n'):
                    if 'Version:' in line:
                        version = line.split(':')[1].strip()
                        break
                
                if version:
                    try:
                        if os.path.exists('/sys/firmware/efi'):
                            return BIOS(f"UEFI {version}")
                        else:
                            return BIOS(f"BIOS {version}")
                    except:
                        return BIOS(version)
            except:
                try:
                    with open('/sys/devices/virtual/dmi/id/bios_version', 'r') as f:
                        version = f.read().strip()
                    if version:
                        if os.path.exists('/sys/firmware/efi'):
                            return BIOS(f"UEFI {version}")
                        else:
                            return BIOS(f"BIOS {version}")
                except:
                    pass
        elif platform.system() == "Darwin":
            output = subprocess.check_output(["system_profiler", "SPHardwareDataType"], 
                                            stderr=subprocess.DEVNULL).decode()
            for line in output.split('\n'):
                if 'Boot ROM Version:' in line:
                    version = line.split(':')[1].strip()
                    return BIOS(f"EFI {version}")
    except:
        pass
    
    return BIOS("UEFI 2.7")


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
                import distro
                name = distro.name(pretty=True)
                if name:
                    return OS(name)
            except:
                pass
        elif system == "Darwin":
            try:
                output = subprocess.check_output(["sw_vers", "-productName"], 
                                                stderr=subprocess.DEVNULL).decode().strip()
                version_output = subprocess.check_output(["sw_vers", "-productVersion"], 
                                                        stderr=subprocess.DEVNULL).decode().strip()
                return OS(f"{output} {version_output}")
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
                return OS(distro.version(pretty=True))
            except:
                if os.path.exists('/etc/os-release'):
                    with open('/etc/os-release', 'r') as f:
                        for line in f:
                            if 'VERSION_ID=' in line:
                                version = line.split('=')[1].strip().strip('"')
                                return OS(version)
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
                for line in output.split('\n'):
                    if 'Description:' in line:
                        description = line.split(':')[1].strip()
                    elif 'Release:' in line:
                        release = line.split(':')[1].strip()
                
                if description and release:
                    return OS(f"{description} ({release})")
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
                elif distro_id == "centos":
                    return OS("https://www.centos.org/download/")
                elif distro_id == "arch":
                    return OS("https://archlinux.org/download/")
                else:
                    return OS("https://kernel.org/")
            except:
                return OS("https://kernel.org/")
        elif system == "Darwin":
            return OS("https://support.apple.com/downloads/macos")
        else:
            return OS("https://www.microsoft.com/en-us/windows")
    except:
        pass
    
    return OS("https://www.microsoft.com/en-us/windows")
