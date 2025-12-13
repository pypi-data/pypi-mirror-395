
# Copyright (C) 2025 David CH.F (destroyer)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import click
from pathlib import Path
import shutil
import tempfile
from cpcready.utils import console, system, DriveManager, discManager, SystemCPM
from cpcready.utils.click_custom import CustomCommand, CustomGroup
from cpcready.utils.console import info2, ok, debug, warn, error, message,blank_line,banner
from cpcready.utils.version import add_version_option_to_group
from rich.console import Console
from rich.panel import Panel
from cpcready.pydsk.dsk import DSK

console = Console()

def convert_to_dos(file_path):
    """Convert file from Unix (LF) to DOS (CRLF) format."""
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # Convertir LF a CRLF (Unix to DOS)
        # Primero eliminar cualquier CR existente para evitar duplicados
        content = content.replace(b'\r\n', b'\n')
        content = content.replace(b'\r', b'\n')
        # Luego convertir todos los LF a CRLF
        content = content.replace(b'\n', b'\r\n')
        
        # Crear archivo temporal con el contenido convertido
        tmp = tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.tmp')
        tmp.write(content)
        tmp.close()
        
        return tmp.name
    except Exception as e:
        debug(f"Error converting to DOS format: {e}")
        return None

def is_header(ruta):
    with open(ruta, "rb") as f:
        cabecera = f.read(128)
        if len(cabecera) < 128:
            return None, None
        
        # El byte 0 debe estar en el rango válido de tipos AMSDOS (0-2 normalmente)
        if cabecera[0] > 2:
            return None, None
        
        # Verificar que nombre y extensión sean ASCII válidos (letras/números)
        try:
            nombre_str = cabecera[1:9].decode("ascii").strip()
            ext_str = cabecera[9:12].decode("ascii").strip()
            # Debe tener al menos un carácter válido en el nombre
            if not nombre_str or not nombre_str.replace(" ", "").isalnum():
                return None, None
        except:
            return None, None
        
        # Load address: bytes 21-22 (little endian)
        load_addr = cabecera[21] + (cabecera[22] << 8)
        
        # Exec address: bytes 26-27 (little endian)
        exec_addr = cabecera[26] + (cabecera[27] << 8)
        
        return load_addr, exec_addr

@click.command(cls=CustomCommand)
@click.argument("file_name", required=True)
@click.argument("type_file", required=False, type=click.Choice(["a", "b", "p"], case_sensitive=True))
@click.argument("load_addr", required=False)
@click.argument("exec_addr", required=False)
@click.option("-A", "--drive-a", is_flag=True, help="Insert disc into drive A")
@click.option("-B", "--drive-b", is_flag=True, help="Insert disc into drive B")
def save(file_name, type_file, load_addr, exec_addr, drive_a, drive_b):
    """Save file to virtual disc.
    
    Type options:
      - a: ASCII/Data file (no AMSDOS header)
      - b: Binary file with AMSDOS header (requires load_addr and optional exec_addr)
      - p: Program file with AMSDOS header (preserves existing header if present)
    """
    
    debug(f"file={file_name}, type={type_file}, load={load_addr}, exec={exec_addr}")
    
    # Verificar que el archivo existe
    if not Path(file_name).exists():
        blank_line(1)
        error(f"File '{file_name}' not found.")
        blank_line(1)
        return
    
    # Obtener el nombre del disco usando DriveManager
    drive_manager = DriveManager()
    system_cpm = SystemCPM()
    
    disc_name = drive_manager.get_disc_name(drive_a, drive_b)
    
    if disc_name is None:
        error("No disc inserted in the specified drive.")
        return
    
    # Obtener el user number (por defecto 0)
    user_number = str(system_cpm.get_user_number())

    # Convertir archivo a formato DOS (CRLF)
    info2("Converting file to DOS format (CRLF)...")
    dos_file = convert_to_dos(file_name)
    
    if dos_file is None:
        warn("Could not convert to DOS format, using original file")
        dos_file = file_name
        cleanup_temp = False
    else:
        debug(f"Converted to DOS format: {dos_file}")
        cleanup_temp = True
    
    try:
        # Verificar si el archivo tiene cabecera AMSDOS
        header_load_addr, header_exec_addr = is_header(dos_file)
    
        if header_load_addr is not None:
            blank_line(1)
            info2(f"File '{file_name}' has AMSDOS header.")
            console.print(f"  [blue]Load address:[/blue] [yellow]&{header_load_addr:04X}[/yellow]")
            console.print(f"  [blue]Exec address:[/blue] [yellow]&{header_exec_addr:04X}[/yellow]")
            # Si el archivo tiene cabecera y no se especificó tipo, preservarla
            # NO forzamos type_file aquí, dejamos que el usuario o el auto-detect decidan
        else:
            blank_line(1)
            info2(f"File '{file_name}' has no AMSDOS header.")
        
        if type_file is None:
            # Sin tipo especificado: detectar automáticamente
            try:
                dsk = DSK(disc_name)
                
                # Obtener nombre del archivo sin path
                file_base_name = Path(file_name).name.upper()
                
                # Si tiene cabecera AMSDOS, preservarla usando file_type=0 (binario)
                # El método write_file detectará la cabecera existente y la preservará
                if header_load_addr is not None:
                    debug(f"File has AMSDOS header (load=&{header_load_addr:04X}, exec=&{header_exec_addr:04X}), preserving it")
                    dsk.write_file(dos_file, dsk_filename=file_base_name, file_type=0, 
                                 user=int(user_number), force=True)
                # Detectar tipo según extensión para archivos sin cabecera
                elif file_base_name.endswith('.BAS'):
                    # BASIC ASCII (sin cabecera AMSDOS - guardar como RAW)
                    debug("Auto-detected as BASIC ASCII file (.BAS)")
                    dsk.write_file(dos_file, dsk_filename=file_base_name, file_type=-1, user=int(user_number), force=True)
                elif file_base_name.endswith('.BIN'):
                    # Binario sin cabecera - añadir cabecera AMSDOS
                    debug("Auto-detected as BINARY file (.BIN)")
                    dsk.write_file(dos_file, dsk_filename=file_base_name, file_type=2, 
                                 load_addr=0x4000, exec_addr=0x4000, 
                                 user=int(user_number), force=True)
                else:
                    # Por defecto: ASCII sin cabecera (RAW)
                    debug("Plain file without header, saving as RAW")
                    dsk.write_file(dos_file, dsk_filename=file_base_name, file_type=-1, 
                                 user=int(user_number), force=True)
                
                dsk.save()
                ok(f"File '{file_name}' saved successfully.")
                 
                # Mostrar listado actualizado
                blank_line(1)
                dsk.list_files(simple=False, use_rich=True)
            except Exception as e:
                error(f"Failed to save file: {e}")
                return

        elif type_file == "a":
            # ASCII/Data file sin cabecera AMSDOS
            debug("Saved as type 'a' (ASCII/data) by user request.")
            try:
                dsk = DSK(disc_name)
                file_base_name = Path(file_name).name.upper()
                
                # Modo -1 = RAW (sin cabecera AMSDOS)
                dsk.write_file(dos_file, dsk_filename=file_base_name, file_type=-1, 
                             user=int(user_number), force=True)
                dsk.save()
                
                ok(f"File '{file_name}' saved successfully.")
                blank_line(1)
                dsk.list_files(simple=False, use_rich=True)
            except Exception as e:
                error(f"Failed to save file: {e}")
                return
                
        elif type_file == "p":
            # Program file con cabecera AMSDOS
            print("Saved as type 'p' (program) by user request.")
            try:
                dsk = DSK(disc_name)
                file_base_name = Path(file_name).name.upper()
                
                # Modo 0 = Binario con cabecera AMSDOS
                dsk.write_file(dos_file, dsk_filename=file_base_name, file_type=0, 
                             load_addr=header_load_addr or 0, exec_addr=header_exec_addr or 0,
                             user=int(user_number), force=True, read_only=True)
                dsk.save()
                
                ok(f"File '{file_name}' saved successfully.")
                blank_line(1)
                dsk.list_files(simple=False, use_rich=True)
            except Exception as e:
                error(f"Failed to save file: {e}")
                return
                
        elif type_file == "b":
            # Binary file con direcciones específicas
            info2("Saved as type 'b' (binary) by user request.")
            
            # Validar que se proporcionaron las direcciones
            if load_addr is None:
                error("Binary type 'b' requires load address. Usage: save file.bin b 0x4000 [0x4000]")
                return
            
            try:
                dsk = DSK(disc_name)
                file_base_name = Path(file_name).name.upper()
                
                # Convertir direcciones hexadecimales
                if isinstance(load_addr, str):
                    if load_addr.startswith(('0x', '0X')):
                        load_address = int(load_addr, 16)
                    elif load_addr.startswith('&'):
                        load_address = int(load_addr[1:], 16)
                    else:
                        load_address = int(load_addr)
                else:
                    load_address = int(load_addr)
                
                # Exec address: usar load_address si no se especifica
                if exec_addr is None:
                    exec_address = load_address
                elif isinstance(exec_addr, str):
                    if exec_addr.startswith(('0x', '0X')):
                        exec_address = int(exec_addr, 16)
                    elif exec_addr.startswith('&'):
                        exec_address = int(exec_addr[1:], 16)
                    else:
                        exec_address = int(exec_addr)
                else:
                    exec_address = int(exec_addr)
                
                debug(f"Load address: 0x{load_address:04X}, Exec address: 0x{exec_address:04X}")
                
                # Modo 2 = Binario con cabecera AMSDOS
                dsk.write_file(dos_file, dsk_filename=file_base_name, file_type=2, 
                             load_addr=load_address, exec_addr=exec_address,
                             user=int(user_number), force=True)
                dsk.save()
                ok(f"File '{file_name}' saved successfully.")
                blank_line(1)
                dsk.list_files(simple=False, use_rich=True)
            except Exception as e:
                error(f"Failed to save file: {e}")
                import traceback
                traceback.print_exc()
                return
    finally:
        # Limpiar archivo temporal si se creó
        if cleanup_temp and dos_file and dos_file != file_name:
            import os
            try:
                os.unlink(dos_file)
                debug(f"Temporary DOS file deleted: {dos_file}")
            except Exception:
                pass  # Ignorar errores al eliminar archivo temporal

