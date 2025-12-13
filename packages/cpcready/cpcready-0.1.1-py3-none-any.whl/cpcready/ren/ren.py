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
from rich.console import Console
from cpcready.pydsk import DSK, DSKError, DSKFileNotFoundError, DSKFileExistsError
from rich.panel import Panel
console = Console()

@click.command(cls=CustomCommand)
@click.argument("file_old", required=True)
@click.argument("file_new", required=True)
@click.option("-A", "--drive-a", is_flag=True, help="Insert disc into drive A")
@click.option("-B", "--drive-b", is_flag=True, help="Insert disc into drive B")
def ren(file_old, file_new, drive_a, drive_b):
    """Rename file on virtual disc."""
    # Obtener el nombre del disco usando DriveManager
    drive_manager = DriveManager()
    
    disc_name = drive_manager.get_disc_name(drive_a, drive_b)
    
    if disc_name is None:
        error("No disc inserted in the specified drive.")
        return
    
    blank_line(1)
    
    try:
        # Cargar DSK y renombrar archivo
        dsk = DSK(disc_name)
        dsk.rename_file(file_old, file_new)
        dsk.save()
        
        ok(f"File renamed: {file_old} → {file_new}")
        
        blank_line(1)
        
        # Mostrar contenido actualizado del disco
        dsk.list_files(simple=False, use_rich=True, show_title=True)
        
    except DSKFileNotFoundError as e:
        error(f"File not found: {file_old}")
    except DSKFileExistsError as e:
        error(f"File already exists: {file_new}")
    except DSKError as e:
        error(f"Error renaming file: {e}")
    
    blank_line(1)
