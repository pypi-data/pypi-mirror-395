
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
import questionary
from cpcready.utils.click_custom import CustomCommand
from cpcready.utils.console import info2, ok, warn, blank_line
from cpcready.utils.toml_config import ConfigManager


@click.command(cls=CustomCommand)
def emu():
    """Configure the emulator to use.
    
    Select between M4Board or RetroVirtualMachine as the default emulator.
    """
    blank_line(1)
    
    # Obtener configuración actual
    config = ConfigManager()
    current_emulator = config.get("emulator", "selected", "RetroVirtualMachine")
    
    # Mostrar emulador actual
    info2(f"Current emulator: {current_emulator}")
    blank_line(1)
    
    # Opciones disponibles
    emulators = [
        "RetroVirtualMachine",
        "M4Board"
    ]
    
    # Prompt para seleccionar emulador
    selected = questionary.select(
        "Select emulator to use:",
        choices=emulators,
        default=current_emulator if current_emulator in emulators else emulators[0]
    ).ask()
    
    # Si el usuario cancela (Ctrl+C o ESC)
    if selected is None:
        blank_line(1)
        warn("Configuration cancelled.")
        blank_line(1)
        return
    
    # Guardar selección
    config.set("emulator", "selected", selected)
    
    blank_line(1)
    ok(f"Emulator set to: {selected}")
    blank_line(1)
