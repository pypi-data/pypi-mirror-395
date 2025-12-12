import os
import shutil

class CreateFile:
    """Erstellt eine neue Datei oder ein Verzeichnis"""
    
    @staticmethod
    def file(path: str, content: str = "", print_output: bool = True):
        """Erstellt eine Datei mit optionalem Inhalt"""
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            if print_output:
                print(f"[+] Datei erstellt: {path}")
        except Exception as e:
            if print_output:
                print(f"[-] Fehler beim Erstellen der Datei {path}: {e}")

    @staticmethod
    def directory(path: str, print_output: bool = True):
        """Erstellt ein Verzeichnis"""
        try:
            os.makedirs(path, exist_ok=True)
            if print_output:
                print(f"[+] Verzeichnis erstellt: {path}")
        except Exception as e:
            if print_output:
                print(f"[-] Fehler beim Erstellen des Verzeichnisses {path}: {e}")

class UpdateFile:
    """Ändert Datei-Eigenschaften"""
    
    @staticmethod
    def name(old_path: str, new_name: str, print_output: bool = True):
        try:
            folder = os.path.dirname(old_path)
            new_path = os.path.join(folder, new_name)
            os.rename(old_path, new_path)
            if print_output:
                print(f"[+] Datei umbenannt: {new_path}")
            return new_path
        except Exception as e:
            if print_output:
                print(f"[-] Fehler beim Umbenennen: {e}")
            return None

    @staticmethod
    def move_to_path(old_path: str, new_folder: str, print_output: bool = True):
        try:
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)
            new_path = os.path.join(new_folder, os.path.basename(old_path))
            shutil.move(old_path, new_path)
            if print_output:
                print(f"[+] Datei verschoben: {new_path}")
            return new_path
        except Exception as e:
            if print_output:
                print(f"[-] Fehler beim Verschieben: {e}")
            return None
        
    @staticmethod
    def content(path: str, new_content: str, print_output: bool = True):
        """Inhalt einer Datei überschreiben"""
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            if print_output:
                print(f"[+] Inhalt der Datei aktualisiert: {path}")
        except Exception as e:
            if print_output:
                print(f"[-] Fehler beim Aktualisieren des Inhalts {path}: {e}")


class DeleteFile:
    """Löscht eine Datei oder ein Verzeichnis"""
    
    @staticmethod
    def file(path: str, print_output: bool = True):
        """Löscht eine Datei"""
        try:
            if os.path.isfile(path):
                os.remove(path)
                if print_output:
                    print(f"[+] Datei gelöscht: {path}")
            else:
                if print_output:
                    print(f"[-] Datei existiert nicht: {path}")
        except Exception as e:
            if print_output:
                print(f"[-] Fehler beim Löschen der Datei {path}: {e}")

    @staticmethod
    def directory(path: str, print_output: bool = True):
        """Löscht ein Verzeichnis inklusive Inhalt"""
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
                if print_output:
                    print(f"[+] Verzeichnis gelöscht: {path}")
            else:
                if print_output:
                    print(f"[-] Verzeichnis existiert nicht: {path}")
        except Exception as e:
            if print_output:
                print(f"[-] Fehler beim Löschen des Verzeichnisses {path}: {e}")


class DuplicateFile:
    """Dupliziert eine Datei"""
    @staticmethod
    def file(path: str, new_path: str = None, print_output: bool = True):
        try:
            if not os.path.exists(path):
                if print_output:
                    print(f"[-] Datei existiert nicht: {path}")
                return None
            if new_path is None:
                folder, name = os.path.split(path)
                name_parts = name.split(".")
                if len(name_parts) > 1:
                    name_parts[-2] += "_copy"
                else:
                    name_parts[0] += "_copy"
                new_name = ".".join(name_parts)
                new_path = os.path.join(folder, new_name)
            shutil.copy2(path, new_path)
            if print_output:
                print(f"[+] Datei dupliziert: {new_path}")
            return new_path
        except Exception as e:
            if print_output:
                print(f"[-] Fehler beim Duplizieren der Datei {path}: {e}")
            return None


class GetFile:
    """Holt Informationen über eine Datei"""

    @staticmethod
    def name(path: str):
        """Gibt den Dateinamen zurück"""
        return os.path.basename(path)

    @staticmethod
    def content(path: str):
        """Gibt den Inhalt der Datei zurück"""
        if not os.path.isfile(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except:
            return None

    @staticmethod
    def path(path: str):
        """Gibt den absoluten Pfad der Datei zurück"""
        return os.path.abspath(path)

    @staticmethod
    def file_extension(path: str):
        """Gibt die Dateiendung zurück"""
        return os.path.splitext(path)[1]

    @staticmethod
    def file_type(path: str):
        """
        Prüft, ob es sich um eine Datei oder ein Verzeichnis handelt.
        Gibt 'file', 'directory' oder 'unknown' zurück.
        """
        if os.path.isfile(path):
            return "file"
        elif os.path.isdir(path):
            return "directory"
        else:
            return "unknown"
