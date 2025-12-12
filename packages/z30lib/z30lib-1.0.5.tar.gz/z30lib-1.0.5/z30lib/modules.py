import subprocess
import sys

class Install:
    @staticmethod
    def module(module_name: str, print_output: bool = True):
        try:
            if print_output:
                print(f"[+] Installing module: {module_name}")
                subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
                print(f"[+] Module {module_name} installed successfully!")
            else:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", module_name],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
        except subprocess.CalledProcessError:
            if print_output:
                print(f"[-] Failed to install module {module_name}")

class Uninstall:
    @staticmethod
    def module(module_name: str, print_output: bool = True):
        try:
            if print_output:
                print(f"[+] Uninstalling module: {module_name}")
                subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", module_name])
                print(f"[+] Module {module_name} uninstalled successfully!")
            else:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "uninstall", "-y", module_name],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
        except subprocess.CalledProcessError:
            if print_output:
                print(f"[-] Failed to uninstall module {module_name}")

class Update:
    @staticmethod
    def module(module_name: str, version: str = None, print_output: bool = True):
        try:
            pkg = f"{module_name}=={version}" if version else module_name
            if print_output:
                if version:
                    print(f"[+] Updating module {module_name} to version {version}")
                else:
                    print(f"[+] Updating module {module_name} to latest version")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", pkg])
                print(f"[+] Module {module_name} updated successfully!")
            else:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "--upgrade", pkg],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
        except subprocess.CalledProcessError:
            if print_output:
                print(f"[-] Failed to update module {module_name}")
