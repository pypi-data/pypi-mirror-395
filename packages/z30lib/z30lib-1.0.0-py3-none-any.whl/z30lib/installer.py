import os
import platform
import subprocess
import sys
import requests
from typing import Optional, Dict, Tuple
import time
from urllib.parse import urlparse, unquote

CONFIG_FILE = "app_installer_config.json"

APP_DOWNLOADS_WINDOWS = {
    "7-Zip": "https://www.7-zip.org/a/7z2409-x64.exe",
    "Git": "https://github.com/git-for-windows/git/releases/latest/download/Git-64-bit.exe",
    "Node.js": "https://nodejs.org/dist/v22.21.0/node-v22.21.0-x64.msi",
    "Python": "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe",
    "Discord": "https://discord.com/api/download?platform=win&format=exe",
    "Google Chrome": "https://dl.google.com/chrome/install/latest/chrome_installer.exe",
    "Mozilla Firefox": "https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US",
    "Microsoft Edge": "https://go.microsoft.com/fwlink/?linkid=2108834&Channel=Stable&language=en",
    "Visual Studio Code": "https://update.code.visualstudio.com/latest/win32-x64-user/stable",
    "VLC Media Player": "https://get.videolan.org/vlc/3.0.20/win64/vlc-3.0.20-win64.exe",
    "OBS Studio": "https://cdn-fastly.obsproject.com/downloads/OBS-Studio-32.0.2-Full-x64.exe",
    "Blender": "https://download.blender.org/release/Blender4.2/blender-4.2.0-windows-x64.msi",
    "GIMP": "https://download.gimp.org/mirror/pub/gimp/v2.10/windows/gimp-2.10.38-setup.exe",
    "Notepad++": "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/latest/download/npp.8.6.4.Installer.x64.exe",
    "Postman": "https://dl.pstmn.io/download/latest/win64",
    "Docker Desktop": "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe",
    "Telegram": "https://telegram.org/dl/desktop/win",
    "Spotify": "https://download.scdn.co/SpotifySetup.exe",
    "Zoom": "https://zoom.us/client/latest/ZoomInstaller.exe",
    "TeamViewer": "https://download.teamviewer.com/download/TeamViewer_Setup.exe",
    "WinRAR": "https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-701.exe",
    "qBittorrent": "https://www.fosshub.com/qBittorrent.html?dwl=qbittorrent_4.6.5_x64_setup.exe",
    "Adobe Reader": "https://ardownload2.adobe.com/pub/adobe/reader/win/AcrobatDC/2400120051/AcroRdrDC2400120051_en_US.exe",
    "Java Runtime": "https://javadl.oracle.com/webapps/download/AutoDL?BundleId=250125_windows-x64_bin.exe",
    "PowerShell 7": "https://github.com/PowerShell/PowerShell/releases/latest/download/PowerShell-7.4.3-win-x64.msi",
    "MySQL Workbench": "https://dev.mysql.com/get/Downloads/MySQLGUITools/mysql-workbench-community-8.0.38-winx64.msi",
    "PuTTY": "https://the.earth.li/~sgtatham/putty/latest/w64/putty-64bit-0.81-installer.msi",
    "Wireshark": "https://2.na.dl.wireshark.org/win64/Wireshark-4.2.5-x64.exe",
    "VirtualBox": "https://download.virtualbox.org/virtualbox/7.0.18/VirtualBox-7.0.18-162988-Win.exe",
    "Steam": "https://cdn.cloudflare.steamstatic.com/client/installer/SteamSetup.exe"
}

APP_PACKAGES_LINUX = {
    "7-Zip": {"deb": "p7zip-full", "rpm": "p7zip", "arch": "p7zip", "flatpak": "com.github.dahenson.p7zip"},
    "Git": {"deb": "git", "rpm": "git", "arch": "git", "flatpak": "org.git.Git"},
    "Node.js": {"deb": "nodejs", "rpm": "nodejs", "arch": "nodejs", "flatpak": "io.nodejs.NodeJS"},
    "Python": {"deb": "python3", "rpm": "python3", "arch": "python", "flatpak": "org.python.Python"},
    "Discord": {"deb": "discord", "rpm": "discord", "arch": "discord", "flatpak": "com.discordapp.Discord"},
    "Google Chrome": {"deb": "google-chrome-stable", "rpm": "google-chrome-stable", "arch": "google-chrome", "flatpak": "com.google.Chrome"},
    "Mozilla Firefox": {"deb": "firefox", "rpm": "firefox", "arch": "firefox", "flatpak": "org.mozilla.firefox"},
    "Microsoft Edge": {"deb": "microsoft-edge-stable", "rpm": "microsoft-edge-stable", "arch": "microsoft-edge-stable-bin", "flatpak": None},
    "Visual Studio Code": {"deb": "code", "rpm": "code", "arch": "visual-studio-code-bin", "flatpak": "com.visualstudio.code"},
    "VLC Media Player": {"deb": "vlc", "rpm": "vlc", "arch": "vlc", "flatpak": "org.videolan.VLC"},
    "OBS Studio": {"deb": "obs-studio", "rpm": "obs-studio", "arch": "obs-studio", "flatpak": "com.obsproject.Studio"},
    "Blender": {"deb": "blender", "rpm": "blender", "arch": "blender", "flatpak": "org.blender.Blender"},
    "GIMP": {"deb": "gimp", "rpm": "gimp", "arch": "gimp", "flatpak": "org.gimp.GIMP"},
    "Notepad++": {"deb": "wine-notepad-plus-plus", "rpm": None, "arch": None, "flatpak": None},
    "Postman": {"deb": "postman", "rpm": "postman", "arch": "postman-bin", "flatpak": "com.getpostman.Postman"},
    "Docker Desktop": {"deb": "docker.io", "rpm": "docker", "arch": "docker", "flatpak": None},
    "Telegram": {"deb": "telegram-desktop", "rpm": "telegram-desktop", "arch": "telegram-desktop", "flatpak": "org.telegram.desktop"},
    "Spotify": {"deb": "spotify-client", "rpm": "spotify", "arch": "spotify", "flatpak": "com.spotify.Client"},
    "Zoom": {"deb": "zoom", "rpm": "zoom", "arch": "zoom", "flatpak": "us.zoom.Zoom"},
    "TeamViewer": {"deb": "teamviewer", "rpm": "teamviewer", "arch": "teamviewer", "flatpak": "com.teamviewer.TeamViewer"},
    "WinRAR": {"deb": "rar", "rpm": "rar", "arch": "rar", "flatpak": None},
    "qBittorrent": {"deb": "qbittorrent", "rpm": "qbittorrent", "arch": "qbittorrent", "flatpak": "org.qbittorrent.qBittorrent"},
    "Adobe Reader": {"deb": "acroread", "rpm": "AdobeReader", "arch": "acroread", "flatpak": None},
    "Java Runtime": {"deb": "default-jre", "rpm": "java-latest-openjdk", "arch": "jre-openjdk", "flatpak": None},
    "PowerShell 7": {"deb": "powershell", "rpm": "powershell", "arch": "powershell", "flatpak": None},
    "MySQL Workbench": {"deb": "mysql-workbench", "rpm": "mysql-workbench", "arch": "mysql-workbench", "flatpak": None},
    "PuTTY": {"deb": "putty", "rpm": "putty", "arch": "putty", "flatpak": None},
    "Wireshark": {"deb": "wireshark", "rpm": "wireshark", "arch": "wireshark", "flatpak": "org.wireshark.Wireshark"},
    "VirtualBox": {"deb": "virtualbox", "rpm": "VirtualBox", "arch": "virtualbox", "flatpak": None},
    "Steam": {"deb": "steam", "rpm": "steam", "arch": "steam", "flatpak": "com.valvesoftware.Steam"}
}

APP_PACKAGES_MAC = {
    "7-Zip": "p7zip",
    "Git": "git",
    "Node.js": "node",
    "Python": "python",
    "Discord": "discord",
    "Google Chrome": "google-chrome",
    "Mozilla Firefox": "firefox",
    "Microsoft Edge": "microsoft-edge",
    "Visual Studio Code": "visual-studio-code",
    "VLC Media Player": "vlc",
    "OBS Studio": "obs",
    "Blender": "blender",
    "GIMP": "gimp",
    "Notepad++": "notepad-plus-plus",
    "Postman": "postman",
    "Docker Desktop": "docker",
    "Telegram": "telegram",
    "Spotify": "spotify",
    "Zoom": "zoom",
    "TeamViewer": "teamviewer",
    "WinRAR": "rar",
    "qBittorrent": "qbittorrent",
    "Adobe Reader": "adobe-acrobat-reader",
    "Java Runtime": "java",
    "PowerShell 7": "powershell",
    "MySQL Workbench": "mysqlworkbench",
    "PuTTY": "putty",
    "Wireshark": "wireshark",
    "VirtualBox": "virtualbox",
    "Steam": "steam"
}

class InstallerError(Exception):
    """Custom exception for installer errors"""
    pass

class DownloadManager:
    """Manages downloads with retry logic and progress tracking"""
    
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def download_file(self, url: str, dest_folder: str, filename: Optional[str] = None, 
                     print_output: bool = True) -> str:
        """Download file with retry logic"""
        if not filename:
            parsed = urlparse(url)
            filename = os.path.basename(unquote(parsed.path))
            
            if not filename or '.' not in filename:
                filename = f"download_{int(time.time())}.exe"
            elif not filename.lower().endswith(('.exe', '.msi', '.dmg', '.pkg', '.app', '.zip', '.tar', '.gz')):
                if 'exe' in url.lower():
                    filename += '.exe'
                elif 'msi' in url.lower():
                    filename += '.msi'
                else:
                    filename += '.bin'
        
        filepath = os.path.join(dest_folder, filename)
        os.makedirs(dest_folder, exist_ok=True)
        
        for attempt in range(self.max_retries):
            try:
                if print_output:
                    print(f"Download attempt {attempt + 1}/{self.max_retries}: {filename}")
                
                response = self.session.get(url, stream=True, timeout=30)
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            if total_size > 0 and print_output:
                                percent = (downloaded / total_size) * 100
                                sys.stdout.write(f"\rProgress: {percent:.1f}% ({downloaded}/{total_size} bytes)")
                                sys.stdout.flush()
                
                if print_output:
                    if total_size > 0:
                        print()
                    print(f"Download completed: {filepath}")
                
                if os.path.getsize(filepath) == 0:
                    raise InstallerError("Downloaded file is empty")
                
                return filepath
                
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise InstallerError(f"Failed to download after {self.max_retries} attempts: {e}")
                if print_output:
                    print(f"Download failed, retrying in 2 seconds... ({e})")
                time.sleep(2)
        
        raise InstallerError("Download failed")

def _get_default_download_folder() -> str:
    """Get platform-specific default downloads folder"""
    system = platform.system()
    
    if system == "Windows":
        try:
            import ctypes
            from ctypes import windll, wintypes
            CSIDL_PERSONAL = 5
            SHGFP_TYPE_CURRENT = 0
            
            buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
            windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
            downloads = os.path.join(os.path.dirname(buf.value), "Downloads")
        except:
            downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    elif system == "Linux":
        xdg_download_dir = os.environ.get('XDG_DOWNLOAD_DIR')
        if xdg_download_dir:
            downloads = xdg_download_dir
        else:
            downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    elif system == "Darwin":
        downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    else:
        downloads = os.path.join(os.path.expanduser("~"), "Downloads")

    os.makedirs(downloads, exist_ok=True)
    return downloads

def _detect_linux_distro() -> str:
    """Detect Linux distribution with fallbacks"""
    try:
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release", "r") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("ID="):
                        distro_id = line.split("=")[1].strip().strip('"')
                        return distro_id
                    elif line.startswith("ID_LIKE="):
                        like = line.split("=")[1].strip().strip('"')
                        if "debian" in like:
                            return "debian"
                        elif "fedora" in like:
                            return "fedora"
                        elif "arch" in like:
                            return "arch"
    except Exception as e:
        print(f"Warning: Could not detect Linux distribution: {e}")
    
    if os.path.exists("/etc/debian_version"):
        return "debian"
    elif os.path.exists("/etc/fedora-release"):
        return "fedora"
    elif os.path.exists("/etc/arch-release"):
        return "arch"
    elif os.path.exists("/etc/redhat-release"):
        return "rhel"
    elif os.path.exists("/etc/SuSE-release"):
        return "suse"
    else:
        return "unknown"

def _get_linux_package_name(app_name: str, use_flatpak: bool = False) -> Optional[str]:
    """Get the appropriate package name for Linux distribution"""
    if app_name not in APP_PACKAGES_LINUX:
        return None
    
    distro = _detect_linux_distro()
    
    if use_flatpak:
        flatpak_name = APP_PACKAGES_LINUX[app_name].get("flatpak")
        if flatpak_name:
            return f"flatpak:{flatpak_name}"
    
    if distro in ["debian", "ubuntu", "mint", "pop", "kali"]:
        return APP_PACKAGES_LINUX[app_name].get("deb")
    elif distro in ["fedora", "rhel", "centos"]:
        return APP_PACKAGES_LINUX[app_name].get("rpm")
    elif distro == "arch":
        return APP_PACKAGES_LINUX[app_name].get("arch")
    elif distro == "opensuse":
        return APP_PACKAGES_LINUX[app_name].get("rpm")
    else:
        for pkg_type in ["deb", "rpm", "arch", "flatpak"]:
            pkg = APP_PACKAGES_LINUX[app_name].get(pkg_type)
            if pkg:
                return pkg
    
    return None

def _install_linux_package(package_name: str, print_output: bool = True) -> bool:
    """Install a package on Linux"""
    try:
        if not package_name:
            raise InstallerError("No package name provided")
        
        distro = _detect_linux_distro()
        
        if package_name.startswith("flatpak:"):
            flatpak_pkg = package_name.replace("flatpak:", "")
            cmd = ["flatpak", "install", "-y", "flathub", flatpak_pkg]
            if print_output:
                print(f"Installing {flatpak_pkg} via Flatpak...")
        else:
            if distro in ["debian", "ubuntu", "mint", "pop"]:
                subprocess.run(["sudo", "apt", "update"], check=False, 
                             capture_output=True, text=True)
                cmd = ["sudo", "apt", "install", "-y", package_name]
            elif distro in ["fedora", "rhel", "centos"]:
                cmd = ["sudo", "dnf", "install", "-y", package_name]
            elif distro == "arch":
                subprocess.run(["sudo", "pacman", "-Sy"], check=False,
                             capture_output=True, text=True)
                cmd = ["sudo", "pacman", "-S", "--noconfirm", package_name]
            elif distro == "opensuse":
                cmd = ["sudo", "zypper", "install", "-y", package_name]
            else:
                raise InstallerError(f"Unsupported Linux distribution: {distro}")
            
            if print_output:
                print(f"Installing {package_name} on {distro.capitalize()}...")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            if distro in ["debian", "ubuntu"] and not package_name.startswith("flatpak:"):
                snap_cmd = ["sudo", "snap", "install", package_name]
                snap_result = subprocess.run(snap_cmd, capture_output=True, text=True)
                if snap_result.returncode == 0:
                    if print_output:
                        print(f"Successfully installed {package_name} via Snap")
                    return True
            
            error_msg = f"Installation failed: {result.stderr[:200]}"
            raise InstallerError(error_msg)
        
        if print_output:
            print(f"Successfully installed {package_name}")
        return True
        
    except FileNotFoundError as e:
        raise InstallerError(f"Package manager not found: {e}")
    except subprocess.CalledProcessError as e:
        raise InstallerError(f"Installation process error: {e}")
    except Exception as e:
        raise InstallerError(f"Unexpected error during installation: {e}")

def _install_mac_package(package_name: str, print_output: bool = True) -> bool:
    """Install a package on macOS"""
    try:
        if not package_name:
            raise InstallerError("No Homebrew package available for this app")
        
        brew_check = subprocess.run(["which", "brew"], capture_output=True, text=True)
        if brew_check.returncode != 0:
            raise InstallerError("Homebrew not installed. Please install Homebrew first: https://brew.sh")
        
        is_cask = package_name in ["google-chrome", "visual-studio-code", "discord", 
                                  "spotify", "zoom", "teamviewer", "docker", "postman",
                                  "microsoft-edge", "firefox", "vlc", "notepad-plus-plus",
                                  "adobe-acrobat-reader", "virtualbox", "steam"]
        
        if is_cask:
            cmd = ["brew", "install", "--cask", package_name]
        else:
            cmd = ["brew", "install", package_name]
        
        if print_output:
            print(f"Installing {package_name} on macOS...")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            error_msg = f"Installation failed: {result.stderr[:200]}"
            raise InstallerError(error_msg)
        
        if print_output:
            print(f"Successfully installed {package_name}")
        return True
        
    except subprocess.CalledProcessError as e:
        raise InstallerError(f"Installation process error: {e}")
    except Exception as e:
        raise InstallerError(f"Unexpected error during macOS installation: {e}")

def _install_windows_file(filepath: str, print_output: bool = True) -> bool:
    """Install downloaded application on Windows"""
    try:
        if not os.path.exists(filepath):
            raise InstallerError(f"Downloaded file not found: {filepath}")
        
        filename = os.path.basename(filepath)
        
        if print_output:
            print(f"Installing {filename}...")
        
        if filename.lower().endswith('.msi'):
            cmd = ["msiexec", "/i", filepath, "/quiet", "/norestart"]
            shell_needed = True
        elif filename.lower().endswith('.exe'):
            cmd = [filepath, "/SILENT", "/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART", "/SP-"]
            shell_needed = True
        else:
            raise InstallerError(f"Unsupported file type: {filename}")
        
        if shell_needed:
            if filename.lower().endswith('.exe'):
                switches = " ".join(cmd[1:]) if len(cmd) > 1 else ""
                full_cmd = f'"{filepath}" {switches}'
                result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
            else:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, capture_output=True, text=True)
        
        success_codes = [0, 1641, 3010]
        if result.returncode not in success_codes:
            if print_output:
                print(f"Warning: Installation returned code {result.returncode}")
                if result.stdout:
                    print(f"Output: {result.stdout[:500]}...")
                if result.stderr:
                    print(f"Errors: {result.stderr[:500]}...")
            
            if print_output:
                print(f"Installation process completed (code: {result.returncode})")
        else:
            if print_output:
                print(f"Installation successful (code: {result.returncode})")
        
        return True
        
    except subprocess.CalledProcessError as e:
        raise InstallerError(f"Installation process error: {e}")
    except Exception as e:
        raise InstallerError(f"Unexpected error during Windows installation: {e}")

def _download_windows_app(app_name: str, dest_folder: str, print_output: bool = True) -> str:
    """Download a Windows application"""
    try:
        if app_name not in APP_DOWNLOADS_WINDOWS:
            raise ValueError(f"App '{app_name}' is not supported on Windows")
        
        url = APP_DOWNLOADS_WINDOWS[app_name]
        download_manager = DownloadManager()
        
        if print_output:
            print(f"Downloading {app_name} from: {url}")
        
        filepath = download_manager.download_file(url, dest_folder, print_output=print_output)
        
        if print_output:
            print(f"Successfully downloaded {app_name} to: {filepath}")
        
        return filepath
        
    except Exception as e:
        raise InstallerError(f"Failed to download {app_name}: {e}")

def _install_app_direct(app_name: str, print_output: bool = True, use_flatpak: bool = False) -> bool:
    """Install an application directly without downloading a file"""
    system = platform.system()
    
    try:
        if system == "Windows":
            raise InstallerError("Windows apps require download first. Use download_install_app() instead.")
        
        elif system == "Linux":
            package_name = _get_linux_package_name(app_name, use_flatpak)
            if not package_name:
                raise InstallerError(f"No installation method available for {app_name} on Linux")
            
            return _install_linux_package(package_name, print_output)
        
        elif system == "Darwin":
            if app_name not in APP_PACKAGES_MAC:
                raise ValueError(f"App '{app_name}' is not supported on macOS")
            
            package_name = APP_PACKAGES_MAC[app_name]
            if not package_name:
                raise InstallerError(f"No Homebrew package available for {app_name}")
            
            return _install_mac_package(package_name, print_output)
        
        else:
            raise InstallerError(f"Unsupported operating system: {system}")
    
    except Exception as e:
        raise InstallerError(f"Failed to install {app_name}: {e}")


def download_app(app_name: str, destination_folder: Optional[str] = None, print_output: bool = True) -> Optional[str]:
    """
    Download an application without installing it
    
    Args:
        app_name: Name of the application to download
        destination_folder: Folder to save the downloaded file (optional, defaults to Downloads folder)
        print_output: Whether to print progress information (default: True)
    
    Returns:
        Path to downloaded file or None if downloading is not applicable (Linux/macOS package managers)
    
    Raises:
        ValueError: If app_name is not supported
        InstallerError: If download fails
    """
    system = platform.system()
    
    try:
        if print_output:
            print(f"[DOWNLOAD] Starting download for: {app_name}")
        
        if destination_folder is None:
            destination_folder = _get_default_download_folder()
        
        os.makedirs(destination_folder, exist_ok=True)
        
        if system == "Windows":
            if app_name not in APP_DOWNLOADS_WINDOWS:
                raise ValueError(f"App '{app_name}' is not supported on Windows")
            
            return _download_windows_app(app_name, destination_folder, print_output)
        
        elif system == "Linux":
            if print_output:
                print("[DOWNLOAD] On Linux, apps are installed via package managers, not downloaded as files.")
                print("[DOWNLOAD] Use install_app() instead for Linux applications.")
            return None
        
        elif system == "Darwin":
            if print_output:
                print("[DOWNLOAD] On macOS, apps are installed via Homebrew, not downloaded as files.")
                print("[DOWNLOAD] Use install_app() instead for macOS applications.")
            return None
        
        else:
            raise InstallerError(f"Unsupported operating system: {system}")
    
    except ValueError as e:
        if print_output:
            print(f"[DOWNLOAD ERROR] {e}")
        raise
    except Exception as e:
        if print_output:
            print(f"[DOWNLOAD ERROR] Failed to download {app_name}: {e}")
        raise InstallerError(f"Download failed: {e}")

def install_app(app_name: str, print_output: bool = True, use_flatpak: bool = False) -> bool:
    """
    Install an application without downloading it first (uses package managers on Linux/macOS)
    
    Args:
        app_name: Name of the application to install
        print_output: Whether to print progress information (default: True)
        use_flatpak: On Linux, prefer Flatpak installation (if available)
    
    Returns:
        True if installation was successful or attempted
    
    Raises:
        ValueError: If app_name is not supported
        InstallerError: If installation fails
    """
    system = platform.system()
    
    try:
        if print_output:
            print(f"[INSTALL] Starting installation for: {app_name}")
        
        if system == "Windows":
            if print_output:
                print("[INSTALL] On Windows, apps must be downloaded first.")
                print("[INSTALL] Use download_install_app() for Windows applications.")
            raise InstallerError("Windows requires download before installation")
        
        return _install_app_direct(app_name, print_output, use_flatpak)
    
    except ValueError as e:
        if print_output:
            print(f"[INSTALL ERROR] {e}")
        raise
    except Exception as e:
        if print_output:
            print(f"[INSTALL ERROR] Failed to install {app_name}: {e}")
        raise InstallerError(f"Installation failed: {e}")

def download_install_app(app_name: str, destination_folder: Optional[str] = None, print_output: bool = True) -> Tuple[Optional[str], bool]:
    """
    Download and install an application
    
    Args:
        app_name: Name of the application to download and install
        destination_folder: Folder to save the downloaded file (optional, defaults to Downloads folder)
        print_output: Whether to print progress information (default: True)
    
    Returns:
        Tuple of (downloaded_file_path, installation_success)
    
    Raises:
        ValueError: If app_name is not supported
        InstallerError: If download or installation fails
    """
    system = platform.system()
    
    try:
        if print_output:
            print(f"[DOWNLOAD & INSTALL] Starting process for: {app_name}")
        
        if system == "Windows":
            downloaded_file = download_app(app_name, destination_folder, print_output)
            
            if downloaded_file and os.path.exists(downloaded_file):
                if print_output:
                    print(f"[DOWNLOAD & INSTALL] Installing {app_name}...")
                
                install_success = _install_windows_file(downloaded_file, print_output)
                return downloaded_file, install_success
            else:
                raise InstallerError(f"Downloaded file not found for {app_name}")
        
        elif system in ["Linux", "Darwin"]:
            if print_output:
                print(f"[DOWNLOAD & INSTALL] On {system}, installing directly via package manager...")
            
            install_success = install_app(app_name, print_output)
            return None, install_success
        
        else:
            raise InstallerError(f"Unsupported operating system: {system}")
    
    except ValueError as e:
        if print_output:
            print(f"[DOWNLOAD & INSTALL ERROR] {e}")
        raise
    except Exception as e:
        if print_output:
            print(f"[DOWNLOAD & INSTALL ERROR] Failed to process {app_name}: {e}")
        raise InstallerError(f"Download and install failed: {e}")

def list_available_apps() -> Dict[str, list]:
    """List all available applications for current platform"""
    system = platform.system()
    
    if system == "Windows":
        return {"Windows": sorted(APP_DOWNLOADS_WINDOWS.keys())}
    elif system == "Linux":
        apps = []
        for app_name in APP_PACKAGES_LINUX.keys():
            if _get_linux_package_name(app_name):
                apps.append(app_name)
        return {"Linux": sorted(apps)}
    elif system == "Darwin":
        apps = [app for app, pkg in APP_PACKAGES_MAC.items() if pkg]
        return {"macOS": sorted(apps)}
    else:
        return {"Unknown": []}

def batch_download(apps: list, destination_folder: Optional[str] = None, print_output: bool = True) -> Dict[str, str]:
    """Download multiple applications at once"""
    results = {}
    
    for app in apps:
        try:
            if print_output:
                print(f"\n{'='*50}")
                print(f"Downloading: {app}")
                print(f"{'='*50}")
            
            result = download_app(app, destination_folder, print_output)
            if result:
                results[app] = f"Success: {result}"
            else:
                results[app] = "Success: (No file - package manager system)"
            
            if print_output:
                print(f"✓ {app}: Download completed")
        
        except Exception as e:
            results[app] = f"Failed: {str(e)}"
            if print_output:
                print(f"✗ {app}: Failed - {str(e)}")
    
    return results

def batch_install(apps: list, print_output: bool = True, use_flatpak: bool = False) -> Dict[str, str]:
    """Install multiple applications at once"""
    results = {}
    
    for app in apps:
        try:
            if print_output:
                print(f"\n{'='*50}")
                print(f"Installing: {app}")
                print(f"{'='*50}")
            
            success = install_app(app, print_output, use_flatpak)
            results[app] = "Success" if success else "Failed"
            
            if print_output:
                print(f"✓ {app}: Successfully installed")
        
        except Exception as e:
            results[app] = f"Failed: {str(e)}"
            if print_output:
                print(f"✗ {app}: Failed - {str(e)}")
    
    if print_output:
        print(f"\n{'='*50}")
        print("Installation Summary:")
        print(f"{'='*50}")
        for app, status in results.items():
            print(f"{app}: {status}")
    
    return results