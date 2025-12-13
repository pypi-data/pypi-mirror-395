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
from cpcready.utils.console import error, warn, blank_line
from cpcready.utils.manager import DriveManager
from cpcready.utils.click_custom import CustomCommand
from cpcready.utils.version import add_version_option
from cpcready.utils.update import show_update_notification

@add_version_option
@click.command(cls=CustomCommand, show_banner=True)
@click.argument('action', type=click.Choice(['a', 'b', 'eject', 'status'], case_sensitive=False), required=False)
@click.option('-A', '--drive-a', is_flag=True, help='Eject disc from drive A (use with eject action)')
@click.option('-B', '--drive-b', is_flag=True, help='Eject disc from drive B (use with eject action)')
def drive(action, drive_a, drive_b):
    """Manage disc drives.
    
    \b
    Actions:
      a       - Select drive A as active drive
      b       - Select drive B as active drive
      eject   - Eject disc from drive (use with -A or -B)
      status  - Show drive status (default if no action specified)
    
    \b
    Examples:
      cpc drive a              # Select drive A
      cpc drive b              # Select drive B
      cpc drive eject -A       # Eject disc from drive A
      cpc drive eject -B       # Eject disc from drive B
      cpc drive status         # Show drive status
      cpc drive                # Show drive status (default)
    """
    show_update_notification()
    drive_manager = DriveManager()
    
    # Si no se especifica acción, mostrar status
    if action is None:
        action = 'status'
    
    action = action.lower()
    
    if action == 'a':
        if drive_manager.read_drive_a() == "":
            blank_line(1)
            error(f"Drive A: disc missing\n")
            drive_manager.drive_table()
            return
        blank_line(1)
        drive_manager.select_drive("a")
        blank_line(1)
        drive_manager.drive_table()
    
    elif action == 'b':
        if drive_manager.read_drive_b() == "":
            blank_line(1)
            error(f"Drive B: disc missing\n")
            drive_manager.drive_table()
            return
        blank_line(1)
        drive_manager.select_drive("b")
        blank_line(1)
        drive_manager.drive_table()
    
    elif action == 'eject':
        # Validar que solo se especifique una unidad
        if drive_a and drive_b:
            blank_line(1)
            error("Cannot specify both -A and -B options. Choose one drive.")
            return
        
        if drive_a:
            blank_line(1)
            drive_manager.eject('A')
            drive_manager.drive_table()
        elif drive_b:
            blank_line(1)
            drive_manager.eject('B')
            drive_manager.drive_table()
        else:
            blank_line(1)
            warn("Please specify a drive using -A or -B option.\n")
            return
    
    elif action == 'status':
        blank_line(1)
        drive_manager.drive_table()
