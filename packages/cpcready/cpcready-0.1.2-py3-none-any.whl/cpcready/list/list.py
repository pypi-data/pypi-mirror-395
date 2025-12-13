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
from cpcready.utils import console, system, DriveManager, discManager, SystemCPM
from cpcready.utils.click_custom import CustomCommand, CustomGroup
from cpcready.utils.console import info2, ok, debug, warn, error, message,blank_line,banner
from cpcready.utils.version import add_version_option_to_group
from cpcready.pydsk import DSK
from cpcready.pydsk.basic_viewer import view_basic, detect_basic_format, view_basic_ascii, detokenize_basic
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
console = Console()

@click.command(cls=CustomCommand)
@click.argument("file_name", required=True)
@click.option("-A", "--drive-a", is_flag=True, help="Insert disc into drive A")
@click.option("-B", "--drive-b", is_flag=True, help="Insert disc into drive B")
def list(file_name, drive_a, drive_b):
    """List BASIC file from virtual disc."""
    # Obtener el nombre del disco usando DriveManager
    drive_manager = DriveManager()
    system_cpm = SystemCPM()
    
    disc_name = drive_manager.get_disc_name(drive_a, drive_b)
    
    if disc_name is None:
        error("No disc inserted in the specified drive.")
        return
    
    # Obtener el user number actual
    user_number = system_cpm.get_user_number()
    
    blank_line(1)
    
    try:
        dsk = DSK(disc_name)
        
        # Leer archivo con cabecera para verificar el tipo
        data_with_header = dsk.read_file(file_name, keep_header=True, user=user_number)
        
        # Verificar si tiene cabecera AMSDOS válida
        if len(data_with_header) >= 128 and dsk._check_amsdos_header(data_with_header):
            file_type = data_with_header[0x12]  # Byte de tipo de archivo
            
            # Tipo 2 = BINARY
            if file_type == 2:
                error(f"Cannot list binary file: {file_name}")
                blank_line(1)
                return
            
            # Tipo 22 = SCREEN$
            if file_type == 22:
                error(f"Cannot list screen file: {file_name}")
                blank_line(1)
                return
        
        # Leer archivo sin cabecera para procesarlo
        data = dsk.read_file(file_name, keep_header=False, user=user_number)
        
        # Intentar visualizar como BASIC - auto detectar formato
        listing = view_basic(data, auto_detect=True)
        
        # Si el listing está vacío, no es BASIC
        if not listing or not listing.strip():
            error(f"File does not appear to be a valid BASIC program: {file_name}")
            blank_line(1)
            return
        
        # Mostrar el listado directamente sin más validaciones
        syntax = Syntax(listing, "basic", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title=f"Listing '{file_name}'", border_style="bright_blue"))
        
    except Exception as e:
        error(f"Error listing file: {e}")
    
    blank_line(1)

