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

import click
from pathlib import Path
import shutil
import fnmatch
from cpcready.utils import console, system, DriveManager, discManager, SystemCPM
from cpcready.utils.click_custom import CustomCommand, CustomGroup
from cpcready.utils.console import info2, ok, debug, warn, error, message,blank_line,banner
from cpcready.utils.version import add_version_option_to_group
from rich.console import Console
from rich.panel import Panel
from cpcready.pydsk import DSK, DSKError, DSKFileNotFoundError
console = Console()
import os

@click.command(cls=CustomCommand)
@click.argument("files", nargs=-1, required=True)
@click.option("-A", "--drive-a", is_flag=True, help="Use drive A")
@click.option("-B", "--drive-b", is_flag=True, help="Use drive B")
def filextr(files, drive_a, drive_b):
    """Extract files from virtual disc to current directory.
    
    Supports multiple files and wildcards.
    
    Examples:
        filextr file.bin
        filextr file1.bin file2.bas
        filextr "*.bin"
        filextr "GAME.*"
    """
    # Obtener el nombre del disco usando DriveManager
    drive_manager = DriveManager()
    disc_manager = discManager("idsk20")
    
    disc_name = drive_manager.get_disc_name(drive_a, drive_b)
    
    if disc_name is None:
        error("No disc inserted in the specified drive.")
        return
    
    blank_line(1)
    dsk = DSK(disc_name)
    
    # Obtener lista de archivos en el DSK
    entries = dsk.get_directory_entries()
    available_files = []
    for entry in entries:
        if not entry.is_deleted and entry.num_page == 0:
            available_files.append(entry.full_name.strip())
    
    # Procesar cada patrón de archivo
    files_to_extract = set()
    for pattern in files:
        pattern_upper = pattern.upper()
        
        # Verificar si es un wildcard
        if '*' in pattern or '?' in pattern:
            # Buscar archivos que coincidan con el patrón
            matches = fnmatch.filter(available_files, pattern_upper)
            if matches:
                files_to_extract.update(matches)
            else:
                warn(f"No files match pattern: {pattern}")
        else:
            # Archivo específico
            # Normalizar el nombre (añadir espacios si es necesario para AMSDOS)
            files_to_extract.add(pattern_upper)
    
    # Extraer archivos
    extracted_count = 0
    failed_count = 0
    info2(f"Extracting with header: True")
    for filename in sorted(files_to_extract):
        try:
            output_file = filename.strip().replace(' ', '')
            dsk.export_file(filename, output_file, keep_header=True)
            ok(f"Extracted: {output_file} ({os.path.getsize(output_file)} bytes)")
            extracted_count += 1
        except DSKFileNotFoundError:
            error(f"File not found: {filename}")
            failed_count += 1
        except Exception as e:
            error(f"Error extracting {filename}: {e}")
            failed_count += 1
    
    blank_line(1)
    if extracted_count > 0:
        info2(f"{extracted_count} file(s) extracted successfully")
        blank_line(1)
    if failed_count > 0:
        error(f"❌ {failed_count} file(s) failed")
        blank_line(1)
