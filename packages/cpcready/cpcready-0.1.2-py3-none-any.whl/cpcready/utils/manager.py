# Copyright 2025 David CH.F (destroyer)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.

import os
import click
import subprocess
from pathlib import Path
from tabulate import tabulate
from rich.console import Console
from cpcready.utils.console import ok, debug,warn, error,info2,blank_line
from cpcready.utils.toml_config import ConfigManager

console = Console()

class discManager:
    """
    Clase para interactuar con idsk20 desde Python.
    Permite listar, importar, extraer, borrar y crear imágenes DSK de Amstrad CPC.
    """

    def __init__(self, idsk_path="idsk20"):
        """
        Inicializa la clase con la ruta del ejecutable idsk20.
        """
        self.idsk_path = idsk_path

    def _run(self, args):
        """
        Ejecuta un comando idsk20 y devuelve la salida.
        """
        cmd = [self.idsk_path] + args
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            # raise RuntimeError(f"Error ejecutando idsk20: {e.stderr.strip()}") from e
            # error(f"Error ejecutando idsk20: {e.stderr.strip()}")
            return None


    def cat(self, dsk_file):
        """Lista el contenido de la imagen DSK."""
        dsk_path = Path(dsk_file)
        if not dsk_path.exists():
            error(f"\nDSK file not found: {dsk_file}\n")
            return None
        return self._run([dsk_file, "-l"])

    def cat_list(self, dsk_file):
        """Lista el contenido de la imagen DSK."""
        dsk_path = Path(dsk_file)
        if not dsk_path.exists():
            error(f"\nDSK file not found: {dsk_file}\n")
            return None
        return self._run([dsk_file, "--ls"])

    def new(self, dsk_file):
        """Crea una nueva imagen DSK vacía."""
        self._run([dsk_file, "-n"])
        ok("disc created successfully")
        return True


    def get(self, dsk_file, filename):
        """Extrae un archivo (o archivos con wildcard) de la imagen DSK."""
        dsk_path = Path(dsk_file)
        if not dsk_path.exists():
            error(f"\nDSK file not found: {dsk_file}\n")
            return None
        
        # Si contiene wildcard (* o ?), obtener lista de archivos y extraer todos
        if '*' in filename or '?' in filename:
            import fnmatch
            
            # Obtener listado de archivos del disco
            listing = self.cat_list(dsk_file)
            if not listing:
                warn(f"Could not read disc contents")
                return None
            
            # Parsear nombres de archivos del listado
            files_to_extract = []
            for line in listing.splitlines():
                parts = line.split()
                if len(parts) >= 2:
                    # Extraer nombre del archivo
                    if parts[1].startswith('.'):
                        # NOMBRE .EXT formato
                        file_name = f"{parts[0]}{parts[1]}"
                    else:
                        # NOMBRE.EXT formato
                        file_name = parts[0]
                    
                    # Verificar si coincide con el patrón wildcard
                    if fnmatch.fnmatch(file_name.upper(), filename.upper()):
                        files_to_extract.append(file_name)
            
            if not files_to_extract:
                warn(f"No files match pattern '{filename}'")
                return None
            
            # Extraer cada archivo
            extracted_count = 0
            for file_name in files_to_extract:
                cmd = [self.idsk_path, dsk_file, "-g", file_name]
                try:
                    result = subprocess.run(
                        cmd, capture_output=True, text=True, check=True
                    )
                    ok(f"Extracted: {file_name}")
                    extracted_count += 1
                except subprocess.CalledProcessError as e:
                    warn(f"Failed to extract: {file_name}")
            
            return f"Extracted {extracted_count} of {len(files_to_extract)} file(s)"
        else:
            # Extracción simple de un solo archivo - sin mostrar warnings del DSK
            cmd = [self.idsk_path, dsk_file, "-g", filename]
            try:
                result = subprocess.run(
                    cmd, capture_output=True, text=True, check=True
                )
                # Solo retornar éxito sin los warnings
                return "File extracted successfully"
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr.strip() if e.stderr else "Unknown error"
                if "not found" in error_msg.lower():
                    error(f"File '{filename}' not found in disc")
                else:
                    error(f"Error extracting file: {error_msg}")
                return None

    def era(self, dsk_file, filename):
        """Elimina un archivo del DSK."""
        dsk_path = Path(dsk_file)
        if not dsk_path.exists():
            error(f"DSK file not found: '{dsk_file}'")
            return None
        
        cmd = [self.idsk_path, dsk_file, "-r", filename]
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )
            ok(f"File '{filename}' erased successfully from disc.")
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            # Si el error es porque el archivo no existe en el disco, mostrar warning
            if "not found" in e.stderr.lower() or "file not found" in e.stderr.lower():
                warn(f"File '{filename}' not found in disc, nothing to delete")
                return None
            else:
                error(f"Error ejecutando idsk20: {e.stderr.strip()}")
                return None
    def ren(self, dsk_file, file_old, file_new):
        """Renombra un archivo en el DSK."""
        dsk_path = Path(dsk_file)
        if not dsk_path.exists():
            error(f"DSK file not found: '{dsk_file}'")
            return None
        
        cmd = [self.idsk_path, dsk_file, "-m", file_old, "--to", file_new]
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )
            ok(f"File '{file_old}' renamed successfully to '{file_new}' on disc.")
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            # Capturar tanto stdout como stderr
            error_msg = e.stderr.strip() if e.stderr else ""
            output_msg = e.stdout.strip() if e.stdout else ""
            
            # Combinar mensajes
            full_error = error_msg or output_msg or "Unknown error"
            
            # Si el error es porque el archivo no existe en el disco
            if "not found" in full_error.lower() or "file not found" in full_error.lower():
                error(f"File '{file_old}' not found in disc")
                return None
            else:
                error(f"Error renaming file: {full_error}")
                return None
            
    def list(self, dsk_file, filename):
        """Lista el contenido de un archivo BASIC del DSK."""
        dsk_path = Path(dsk_file)
        if not dsk_path.exists():
            error(f"DSK file not found: '{dsk_file}'")
            return None
        
        cmd = [self.idsk_path, dsk_file, "-b", filename]
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )
            # ok(f"File '{filename}' erased successfully from disc.")
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            # Si el error es porque el archivo no existe en el disco, mostrar warning
            if "not found" in e.stderr.lower() or "file not found" in e.stderr.lower():
                error(f"File '{filename}' not found in disc")
                return None
            else:
                # error(f"Error ejecutando idsk20: {e.stderr.strip()}")
                return None

    def save(self, dsk_file, src_file, type_file=None, load_addr=None, exec_addr=None, force=False, readonly=False, system=False, user=None):
        """
        Inserta un archivo en la imagen DSK.

        file_type: 0=ASCII, 1=BINARY, 2=raw
        load_addr, exec_addr: direcciones hex opcionales (ej. '4000', 'C000')
        """
        # Validar que el archivo DSK existe
        dsk_path = Path(dsk_file)
        if not dsk_path.exists():
            blank_line(1)
            error(f"\nDSK file not found: {dsk_file}\n")
            return False
        
        # Validar que el archivo fuente existe
        src_path = Path(src_file)
        if not src_path.exists():
            blank_line(1)
            error(f"File not found: {src_file}")
            return False
        
        args = [dsk_file, "-i", src_file]

        if type_file is not None:
            args += ["-t", str(type_file)]
        if load_addr:
            args += ["-c", load_addr]
        if exec_addr:
            args += ["-e", exec_addr]
        if force:
            args.append("-f")
        if readonly:
            args.append("-o")
        if system:
            args.append("-s")
        if user is not None:
            args += ["-u", str(user)]

        return self._run(args)

    
    def list_basic(self, dsk_file, filename, split=False):
        dsk_path = Path(dsk_file)
        if not dsk_path.exists():
            error(f"\nDSK file not found: {dsk_file}\n")
            return None
        
        args = [dsk_file, "-b", filename]
        if split:
            args.append("-p")
        return self._run(args)

    def list_ascii(self, dsk_file, filename):
        dsk_path = Path(dsk_file)
        if not dsk_path.exists():
            error(f"\nDSK file not found: {dsk_file}\n")
            return None
        
        return self._run([dsk_file, "-a", filename])

    def list_dams(self, dsk_file, filename):
        dsk_path = Path(dsk_file)
        if not dsk_path.exists():
            error(f"\nDSK file not found: {dsk_file}\n")
            return None
        
        return self._run([dsk_file, "-d", filename])

    def list_hex(self, dsk_file, filename):
        dsk_path = Path(dsk_file)
        if not dsk_path.exists():
            error(f"\nDSK file not found: {dsk_file}\n")
            return None
        
        return self._run([dsk_file, "-h", filename])

    def disassemble(self, dsk_file, filename):
        dsk_path = Path(dsk_file)
        if not dsk_path.exists():
            error(f"\nDSK file not found: {dsk_file}\n")
            return None
        
        return self._run([dsk_file, "-z", filename])

    def file_type(self, dsk_file, filename):
        """
        Muestra el tipo de archivo en el DSK.
        
        Args:
            dsk_file (str): Ruta al archivo DSK
            filename (str): Nombre del archivo a consultar
            
        Returns:
            str: Salida del comando con el tipo de archivo (ej: "8BP.BIN: BINARY")
                 None si el archivo no existe en el disco
        """
        dsk_path = Path(dsk_file)
        if not dsk_path.exists():
            error(f"\nDSK file not found: {dsk_file}\n")
            return None
        
        cmd = [self.idsk_path, dsk_file, "-y", filename]
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            # Si el error es porque el archivo no existe en el disco
            if "not found" in e.stderr.lower() or "file not found" in e.stderr.lower():
                error(f"File '{filename}' not found in disc")
                return None
            else:
                error(f"Error ejecutando idsk20: {e.stderr.strip()}")
                return None

    def cat_table(self, dsk_file):
        """
        Muestra el contenido del disco en formato tabla usando Rich.
        
        Args:
            dsk_file (str): Ruta al archivo DSK
        """
        from rich.console import Console
        from rich.table import Table
        from rich import box
        
        console = Console()
        
        # Validar que el archivo DSK existe
        dsk_path = Path(dsk_file)
        if not dsk_path.exists():
            error(f"\nDSK file not found: {dsk_file}\n")
            return False
        
        # Obtener el listado del disco
        try:
            result = self.cat_list(dsk_file)
        except RuntimeError as e:
            error(f"Error reading disc: {e}")
            return False
        
        if not result:
            warn("Empty disc or no data available")
            return False
        
        # Convertir el resultado en líneas
        result_lines = result.strip().splitlines()
        
        # Crear tabla
        table = Table(
            title=f"[bold]{Path(dsk_file).name}[/bold]",
            border_style="bright_blue",
            box=box.ROUNDED
        )
        
        table.add_column("File", style="bold yellow")
        table.add_column("Size", justify="right", style="green")
        table.add_column("Load Addr", justify="center", style="bright_magenta")
        table.add_column("Exec Addr", justify="center", style="bright_magenta")
        table.add_column("User", justify="center", style="white")
        
        # Parsear cada línea del listado
        free_space = None
        for line in result_lines:
            # Detectar línea de espacio libre (ej: "151K free")
            if "free" in line.lower():
                free_space = line.strip()
                continue
            
            # Ignorar líneas de advertencia, vacías o líneas de borde
            if (not line.strip() or 
                "warning" in line.lower() or 
                "track" in line.lower() or
                line.strip().startswith("─") or
                line.strip().startswith("│") or
                line.strip().startswith("├")):
                continue
            
            # Dividir por espacios
            parts = line.split()
            
            # Ignorar líneas que no cumplan con el formato esperado
            # Formato esperado: NOMBRE .EXT TAMAÑO K LOAD EXEC User NUMERO
            # o: NOMBRE.EXT TAMAÑO K LOAD EXEC User NUMERO
            try:
                if len(parts) >= 6:
                    # Verificar si la extensión está separada (empieza con punto)
                    if parts[1].startswith('.'):
                        # NOMBRE .EXT TAMAÑO K LOAD EXEC User NUMERO
                        filename = f"{parts[0]}{parts[1]}"
                        size_str = f"{parts[2]} {parts[3]}"
                        load = parts[4]
                        exec_addr = parts[5]
                        user = parts[7] if len(parts) > 7 else "0"
                    else:
                        # NOMBRE.EXT TAMAÑO K LOAD EXEC User NUMERO
                        filename = parts[0]
                        size_str = f"{parts[1]} {parts[2]}"
                        load = parts[3]
                        exec_addr = parts[4]
                        user = parts[6] if len(parts) > 6 else "0"
                    
                    table.add_row(filename, size_str, load, exec_addr, user)
            except (ValueError, IndexError):
                # Ignorar líneas que no se puedan parsear
                continue
        
        # Añadir línea de separación y espacio libre si existe
        if free_space:
            # Marcar la última fila como fin de sección solo si hay filas
            if len(table.rows) > 0:
                table.rows[-1].end_section = True
            table.add_row(
                f"[bold bright_green]{free_space}[/bold bright_green]",
                "", "", "", ""
            )
        
        # Mostrar tabla
        console.print(table)
        return True

    def info_disc(self, dsk_file, verbose=False):
        """Print a human-friendly information summary for a DSK file.

        This mirrors the behaviour of `generate-disc-readme.sh` but prints
        the summary to stdout using colorized output.
        """
        
        path = Path(dsk_file)
        disc_manager = discManager(self.idsk_path)
        if not path.exists():
            error(f"\nDSK file not found: {dsk_file}\n")
            return False

        # Use the existing cat method to get listing
        try:
            listing_raw = self.cat(dsk_file) or ""
        except RuntimeError:
            listing_raw = ""

        if not listing_raw.strip():
            disc_listing = ["(Empty disc)"]
            file_lines = []
        else:
            # Extract file data lines from the table (lines with │ that contain file info)
            file_lines = []
            for line in listing_raw.splitlines():
                # Skip table borders and headers, look for lines with file data
                if "│" in line and not line.strip().startswith("│     File") and not "─" in line and not "free" in line.lower():
                    # Clean the line and extract file info
                    clean_line = line.replace("│", "").strip()
                    if clean_line and not clean_line.startswith("File"):
                        file_lines.append(clean_line)
            
            disc_listing = file_lines if file_lines else ["(Empty disc)"]

        # Count types from the cleaned file lines
        basic_files = sum(1 for l in file_lines if ".BAS" in l.upper())
        binary_files = sum(1 for l in file_lines if ".BIN" in l.upper())
        text_files = sum(1 for l in file_lines if any(ext in l.upper() for ext in (".TXT", ".DOC")))
        other_files = max(0, len(file_lines) - basic_files - binary_files - text_files) if file_lines else 0

        # File size
        try:
            disc_size = path.stat().st_size
        except Exception:
            disc_size = "Unknown"

        # Header
        name = path.stem.upper()
        console.print(f"[bold cyan]{name} disc INFORMATION[/bold cyan]")
        print("=" * 60)
        print(f"disc file: {dsk_file}")
        print(f"disc size: {disc_size} bytes")
        blank_line(1)

        # Summary
        print("-" * 60)
        console.print(f"[yellow]disc SUMMARY[/yellow]")
        print("-" * 60)
        total_files = len(file_lines) if file_lines else 0
        print(f"Total files: {total_files}")
        print(f"- BASIC programs: {basic_files}")
        print(f"- Binary files: {binary_files}")
        print(f"- Text files: {text_files}")
        print(f"- Other files: {other_files}")
        blank_line(1)
        print("-" * 60)
        console.print(f"[yellow]CAT FILES[/yellow]")
        print("-" * 60)
        blank_line(1)
        # File listing - show the formatted table from cat method
        disc_manager.cat_table(dsk_file)

        # # BASIC program short descriptions if verbose
        # if verbose and basic_files > 0 and file_lines:
        #     blank_line(1)
        #     print(f"{Fore.MAGENTA}BASIC PROGRAMS{Style.RESET_ALL}")
        #     print("-" * 60)
        #     # Try to extract some lines from first BASIC files
        #     for line in file_lines:
        #         if ".BAS" in line.upper():
        #             # Extract filename from the cleaned line
        #             parts = line.split()
        #             if len(parts) >= 2:
        #                 filename = parts[0] + parts[1]  # e.g., "DEMO13" + ".BAS"
        #                 try:
        #                     basic_content = self._run([dsk_file, "-b", filename])
        #                 except RuntimeError:
        #                     basic_content = ""
        #                 if basic_content:
        #                     sample = "\n".join(basic_content.splitlines()[:6])
        #                     print(f"{filename}:")
        #                     for l in sample.splitlines():
        #                         print(f"  {l}")
        #                     blank_line(1)

        # print(f"{Fore.CYAN}Generated with idsk20 (if available){Style.RESET_ALL}")
        blank_line(1)
        return True

class DriveManager:
    def __init__(self, drive_file="cpcready.toml"):
        # Usar ConfigManager en vez de shelve
        self.config = ConfigManager(drive_file)

    def _initial_structure(self):
        """Devuelve la estructura base del sistema de drives."""
        return {
            "drive_a": "",
            "drive_b": "",
            "selected_drive": "A"
        }

    def _secure_structure(self):
        """Ya no es necesario, ConfigManager se encarga de la estructura inicial."""
        pass

    # --- RESET A VALORES ---
    def reset(self, forzar=False):
        """Resetea la estructura de drives a valores iniciales."""
        self.config.reset()
        return True

    # --- LECTURA ---
    def read_drive_a(self):
        return self.config.get("drive", "drive_a", "")

    def read_drive_b(self):
        return self.config.get("drive", "drive_b", "")

    def read_drive_select(self):
        return self.config.get("drive", "selected_drive", "A")

    # --- MODIFICACIÓN ---
    def insert_drive_a(self, valor):
        # Verificar si el mismo disc ya está insertado en drive A
        current_a = self.config.get("drive", "drive_a", "")
        if current_a == valor and valor != "":
            warn(f"disc is already inserted in drive A.")
            return False
        
        # Verificar que el mismo disc no esté en drive B
        current_b = self.config.get("drive", "drive_b", "")
        if current_b == valor and valor != "":
            # Si está en B, lo quitamos de B antes de ponerlo en A
            self.config.set("drive", "drive_b", "")
            warn(f"disc was removed from drive B.")
        
        self.config.set("drive", "drive_a", valor)
        ok(f"Inserted into drive A.")
        return True

    def insert_drive_b(self, valor):
        # Verificar si el mismo disc ya está insertado en drive B
        current_b = self.config.get("drive", "drive_b", "")
        if current_b == valor and valor != "":
            warn(f"disc is already inserted in drive B.")
            return False
        
        # Verificar que el mismo disc no esté en drive A
        current_a = self.config.get("drive", "drive_a", "")
        if current_a == valor and valor != "":
            # Si está en A, lo quitamos de A antes de ponerlo en B
            self.config.set("drive", "drive_a", "")
            warn(f"disc was removed from drive A.")
        
        self.config.set("drive", "drive_b", valor)
        ok(f"Inserted into drive B.")
        return True

    def select_drive(self, valor):
        if valor not in ("a", "b"):
            error(f"Invalid value. Use 'a' or 'b'.")
            return
        self.config.set("drive", "selected_drive", valor)
        ok(f"Drive {valor.upper()} as selected")

    def eject(self, drive):
        """Eject disc from specified drive (A or B)."""
        drive = drive.lower()
        if drive not in ("a", "b"):
            error("Invalid drive. Use 'A' or 'B'.")
            return False
        
        key = f"drive_{drive}"
        current_disc = self.config.get("drive", key, "")
        if current_disc == "":
            blank_line(1)
            warn(f"There is no disc in the drive {drive.upper()}\n")
            return False
        
        self.config.set("drive", key, "")
        ok(f"disc ejected from drive {drive.upper()}\n")
        return True

    def get_disc_name(self, drive_a=False, drive_b=False):
        """
        Obtiene el nombre del disco según las opciones de unidad.
        
        Args:
            drive_a (bool): Si True, obtiene el disco del drive A
            drive_b (bool): Si True, obtiene el disco del drive B
            
        Returns:
            str or None: Nombre del disco o None si hay error
        """
        # Validar que solo se especifique una unidad
        if drive_a and drive_b:
            error("Cannot specify both -A and -B options. Choose one drive.")
            return None
        
        if drive_a:
            return self.read_drive_a()
        elif drive_b:
            return self.read_drive_b()
        else:
            drive = self.read_drive_select().upper()
            if drive == 'A':
                return self.read_drive_a()
            else:
                return self.read_drive_b()

    # --- EMULATOR CONFIGURATION ---
    def read_emulator(self):
        """Lee el emulador configurado."""
        return self.config.get("emulator", "default", "RetroVirtualMachine")
    
    def set_emulator(self, emulator):
        """Establece el emulador."""
        valid_emulators = ["RetroVirtualMachine", "CPCEmu", "M4Board"]
        if emulator not in valid_emulators:
            error(f"Invalid emulator. Use one of: {', '.join(valid_emulators)}")
            return False
        
        self.config.set("emulator", "default", emulator)
        ok(f"Emulator set to '{emulator}'")
        return True
    
    def read_m4board_ip(self):
        """Lee la IP del M4Board."""
        return self.config.get("emulator", "m4board_ip", "")
    
    def set_m4board_ip(self, ip):
        """Establece la IP del M4Board."""
        self.config.set("emulator", "m4board_ip", ip)
        ok(f"M4Board IP set to '{ip}'")
        return True

    def drive_info(self):
        return self.config.get_section("drive")

    def drive_table(self, estilo="fancy_grid", devolver=False):
        """
        Imprime una tabla profesional con color resaltando el drive seleccionado usando Rich.
        Si devolver=True, devuelve la tabla como texto plano (sin color).
        """
        from rich.console import Console
        from rich.table import Table
        from rich import box
        
        console = Console()
        
        # Leer configuración
        drive_a = self.config.get("drive", "drive_a", "")
        drive_b = self.config.get("drive", "drive_b", "")
        select = self.config.get("drive", "selected_drive", "A").lower()

        # Crear tabla Rich
        table = Table(
            border_style="bright_blue",
            box=box.ROUNDED
        )
        
        table.add_column("Select", justify="center")
        table.add_column("Drive", justify="center")
        table.add_column("disc", style="white")
        table.add_column("Path", style="dim white")
        
        # Símbolos y estilos según selección
        if select == "a":
            symbol_a = "[bold green]◉[/bold green]"
            drive_a_label = "[bold green]A[/bold green]"
            symbol_b = "[yellow]◎[/yellow]"
            drive_b_label = "[bold yellow]B[/bold yellow]"
        else:
            symbol_a = "[yellow]◎[/yellow]"
            drive_a_label = "[bold yellow]A[/bold yellow]"
            symbol_b = "[bold green]◉[/bold green]"
            drive_b_label = "[bold green]B[/bold green]"
        
        # Procesar disco A
        if drive_a:
            disc_a_path = Path(drive_a)
            disc_a_name = disc_a_path.name
            disc_a_dir = str(disc_a_path.parent)
            if disc_a_path.exists():
                disc_a = f"[green]{disc_a_name}[/green]"
                path_a = f"[dim green]{disc_a_dir}[/dim green]"
            else:
                disc_a = f"[red]{disc_a_name}[/red]"
                path_a = f"[dim red]{disc_a_dir}[/dim red]"
        else:
            disc_a = "[yellow]No disc inserted[/yellow]"
            path_a = ""
        
        # Procesar disco B
        if drive_b:
            disc_b_path = Path(drive_b)
            disc_b_name = disc_b_path.name
            disc_b_dir = str(disc_b_path.parent)
            if disc_b_path.exists():
                disc_b = f"[green]{disc_b_name}[/green]"
                path_b = f"[dim green]{disc_b_dir}[/dim green]"
            else:
                disc_b = f"[red]{disc_b_name}[/red]"
                path_b = f"[dim red]{disc_b_dir}[/dim red]"
        else:
            disc_b = "[yellow]No disc inserted[/yellow]"
            path_b = ""
        
        table.add_row(
            symbol_a,
            drive_a_label,
            disc_a,
            path_a
        )
        table.add_row(
            symbol_b,
            drive_b_label,
            disc_b,
            path_b
        )
        
        # Mostrar tabla
        console.print(table)
        blank_line(1)
        
        # Si se solicita devolver, crear versión sin color
        if devolver:
            datos_sin_color = [
                [symbol_a, "A", drive_a],
                [symbol_b, "B", drive_b],
            ]
            tabla_sin_color = tabulate(
                datos_sin_color, headers=["Select", "Drive", "disc"],
                tablefmt=estilo, stralign="left"
            )
            return tabla_sin_color
    
    def render_drive_panel(self, drive):
        """
        Renderiza un panel con información del drive y disco usando Rich.
        
        Args:
            drive (str): Letra del drive (ej: "A", "B")
        """
        from rich.console import Console
        from rich.panel import Panel
        from rich.columns import Columns
        from rich.align import Align
        
        console = Console()
        
        # Leer el disco asociado al drive
        drive_lower = drive.lower()
        if drive_lower == "a":
            disc_name = self.read_drive_a()
            disc_name = Path(disc_name).name
        elif drive_lower == "b":
            disc_name = self.read_drive_b()
            disc_name = Path(disc_name).name
        else:
            disc_name = "Invalid drive"
        
        # Verificar si este drive está seleccionado
        selected_drive = self.read_drive_select().lower()
        is_selected = drive_lower == selected_drive
        
        # Símbolo y colores según si está seleccionado o no
        symbol = "◉" if is_selected else "◯"
        drive_color = "green" if is_selected else "yellow"
        border_color = "green" if is_selected else "yellow"
        
        # Verificar el estado del disco y ajustar colores
        disc_missing = False
        if disc_name == "":
            disc_name = f"[dim {drive_color}]No disc inserted[/dim {drive_color}]"
        else:
            # Verificar si el archivo del disco existe
            disc_path_obj = Path(disc_name)
            if not disc_path_obj.exists():
                # Disco no existe - solo el texto del disco en rojo, pero mantener colores originales para drive
                disc_name = f"[bold red]{disc_name}[/bold red]"
                disc_missing = True
            else:
                # Disco existe - usar colores normales (verde si seleccionado, amarillo si no)
                disc_name = f"[bold {drive_color}]{disc_path_obj}[/bold {drive_color}]"
        
        # Panel izquierdo → letra de unidad (centrado)
        # Si el disco no existe, usar borde rojo pero mantener símbolo con color original
        panel_border_color = "red" if disc_missing else border_color
        
        drive_panel = Panel.fit(
            Align.center(f"[bold {drive_color}]{symbol} {drive.upper()}[/bold {drive_color}]"),
            border_style=panel_border_color,
            width=7
        )
        
        # Panel derecho → ruta del disco (centrado)
        path_panel = Panel.fit(
            Align.center(disc_name),
            border_style=border_color
        )
        
        # Mostrar ambos paneles en una sola línea
        console.print(Columns([drive_panel, path_panel]))

    def show_drive_info(self, drive=None):
        """
        Renderiza un panel con información del drive y disco usando Rich.
        
        Args:
            drive (str, optional): Letra del drive (ej: "A", "B"). 
                                   Si no se especifica, usa el drive seleccionado.
        """
        from rich.console import Console
        from rich.panel import Panel
        from rich.columns import Columns
        from rich.align import Align
        from rich.padding import Padding
        from rich.layout import Layout
        from rich import box
        
        console = Console()
        
        # Obtener información de los drives
        disc_a = self.read_drive_a()
        disc_b = self.read_drive_b()
        selected_drive = self.read_drive_select().upper()
        
        # Si no se pasa la unidad, usar la seleccionada
        if drive is None:
            drive = selected_drive
        else:
            drive = drive.upper()
        
        # Determinar qué disco mostrar según la unidad pasada
        disc_path = disc_a if drive == "A" else disc_b
        
        # Extraer solo el nombre del archivo (sin path)
        if disc_path == "":
            disc_name = "No disc inserted"
        else:
            disc_name = os.path.basename(disc_path)
        
        # Panel drive A
        symbol_a = "▲" if selected_drive == "A" else "▼"
        border_a = "red" if selected_drive == "A" else "red"
        drive_panel_a = Panel(
            Align.center(f"[bold white]A {symbol_a}[/bold white]"),
            border_style=border_a,
            width=7
        )

        # Panel drive B
        symbol_b = "▲" if selected_drive == "B" else "▼"
        border_b = "red" if selected_drive == "B" else "red"
        drive_panel_b = Padding(
            Panel(
                Align.center(f"[bold bright_white]B {symbol_b}[/bold bright_white]"),
                border_style=border_b,
                width=7
            ),
            (0, 0, 0, 0)
        )

        # Panel ruta del disco (solo nombre del archivo)
        path_panel = Panel(
            Align.center(f"[bold white]{disc_name}[/bold white]"),
            border_style="white",
            width=34
        )

        # Agrupar los tres paneles
        drive_panel_a_padded = Padding(drive_panel_a, (0, 0, 0, 0))
        path_panel_padded = Padding(path_panel, (0, 0, 0, 0))
        inner_columns = Columns([drive_panel_a_padded, path_panel_padded, drive_panel_b], padding=0)
        inner_columns_padded = Padding(inner_columns, (0, 0, 1, 0))

        # Layout
        layout = Layout()
        layout.split_column(
            Layout(Align.center(inner_columns_padded, vertical="middle"), ratio=1)
        )

        grouped_panel = Panel(
            layout,
            border_style="grey82",
            width=52,
            height=5,
            title=f"Drive {drive}"
        )
        console.print(grouped_panel)


class SystemCPM:
    """
    Clase para gestionar configuraciones del sistema CP/M.
    """
    
    def __init__(self, config_file="cpcready.toml"):
        """
        Inicializa la clase con la ruta del fichero de configuración.
        """
        self.config = ConfigManager(config_file)
    
    def get_user_number(self):
        """
        Obtiene el user number guardado en TOML.
        
        Returns:
            int: User number (0-15), por defecto 0
        """
        return self.config.get("system", "user", 0)

    def get_model(self):
        """
        Obtiene el modelo CPC configurado.
        
        Returns:
            str: Modelo ('464', '664', '6128'), por defecto '6128'
        """
        return self.config.get("system", "model", "6128")

    def set_model(self, model):
        """
        Establece el modelo CPC.
        
        Args:
            model (str): Modelo ('464', '664', '6128')
        """
        if model not in ["464", "664", "6128"]:
            raise ValueError("Invalid model. Must be 464, 664 or 6128")
        self.config.set("system", "model", model)
        return True

    def get_mode(self):
        """
        Obtiene el modo de pantalla CPC configurado.
        
        Returns:
            str: Modo ('0', '1', '2'), por defecto '1'
        """
        return str(self.config.get("system", "mode", "1"))

    def set_mode(self, mode):
        """
        Establece el modo de pantalla CPC.
        
        Args:
            mode (str): Modo ('0', '1', '2')
        """
        if str(mode) not in ["0", "1", "2"]:
            raise ValueError("Invalid mode. Must be 0, 1 or 2")
        self.config.set("system", "mode", str(mode))
        return True


class LegacyConfigManager:
    """
    Clase para gestionar toda la configuración del sistema (drives, emulador, etc).
    Unifica DriveManager y añade configuración de emulador.
    DEPRECATED: Usar ConfigManager de toml_config en su lugar.
    """
    
    def __init__(self, config_file="cpcready.toml"):
        """Inicializa el gestor de configuración."""
        self.drive_manager = DriveManager(config_file)
    
    def get_current_config(self):
        """
        Obtiene toda la configuración actual.
        
        Returns:
            dict: Diccionario con toda la configuración
        """
        return {
            'drive_a': self.drive_manager.read_drive_a(),
            'drive_b': self.drive_manager.read_drive_b(),
            'default_drive': self.drive_manager.read_drive_select(),
            'emulator': self.drive_manager.read_emulator(),
            'm4board_ip': self.drive_manager.read_m4board_ip()
        }
    
    def save_config(self, drive_a=None, drive_b=None, default_drive=None, 
                   emulator=None, m4board_ip=None, silent=True):
        """
        Guarda la configuración completa.
        
        Args:
            drive_a (str, optional): Ruta del disco A
            drive_b (str, optional): Ruta del disco B
            default_drive (str, optional): Drive por defecto ('a' o 'b')
            emulator (str, optional): Emulador seleccionado
            m4board_ip (str, optional): IP del M4Board
            silent (bool, optional): Si es True, no muestra mensajes de consola
            
        Returns:
            bool: True si se guardó correctamente
        """
        from pathlib import Path
        
        success = True
        
        # Guardar drives
        if drive_a is not None:
            if drive_a:
                # Verificar que el mismo disc no esté en drive B
                current_b = self.drive_manager.config.get("drive", "drive_b", "")
                if current_b == drive_a and drive_a != "":
                    self.drive_manager.config.set("drive", "drive_b", "")
                self.drive_manager.config.set("drive", "drive_a", drive_a)
            else:
                self.drive_manager.config.set("drive", "drive_a", "")
        
        if drive_b is not None:
            if drive_b:
                # Verificar que el mismo disc no esté en drive A
                current_a = self.drive_manager.config.get("drive", "drive_a", "")
                if current_a == drive_b and drive_b != "":
                    self.drive_manager.config.set("drive", "drive_a", "")
                self.drive_manager.config.set("drive", "drive_b", drive_b)
            else:
                self.drive_manager.config.set("drive", "drive_b", "")
        
        # Guardar drive por defecto
        if default_drive:
            self.drive_manager.config.set("drive", "selected_drive", default_drive)
        
        # Guardar emulador
        if emulator:
            valid_emulators = ["RetroVirtualMachine", "CPCEmu", "M4Board"]
            if emulator in valid_emulators:
                self.drive_manager.config.set("emulator", "default", emulator)
            else:
                success = False
        
        # Guardar IP M4Board
        if m4board_ip is not None:
            self.drive_manager.config.set("emulator", "m4board_ip", m4board_ip)
        
        return success
