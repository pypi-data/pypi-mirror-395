
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
from pathlib import Path
from cpcready.utils.click_custom import CustomCommand, CustomGroup
from cpcready.utils.console import info2, ok, error, warn, blank_line
from cpcready.utils.toml_config import ConfigManager
from cpcready.utils.retrovirtualmachine import RVM


# Crear grupo principal de comandos rvm
@click.group(cls=CustomGroup, name='rvm')
def rvm_group():
    """RetroVirtualMachine emulator management."""
    pass


@rvm_group.command(cls=CustomCommand, name='status')
def status():
    """Check RetroVirtualMachine installation and version.
    
    Verifies:
    - RVM path is configured
    - RVM executable exists at the configured path
    - RVM version matches the required version
    """
    blank_line(1)
    
    # Cargar configuración
    config = ConfigManager()
    ruta_rvm = config.get("emulator", "retro_virtual_machine_path", "")
    
    # Verificar que está configurado
    if not ruta_rvm:
        error("RetroVirtualMachine path not configured.")
        error("Configure the emulator using the configuration file.")
        blank_line(1)
        return
    
    info2(f"Configured path: {ruta_rvm}")
    
    # Verificar que existe
    if not Path(ruta_rvm).exists():
        error(f"RetroVirtualMachine not found at: {ruta_rvm}")
        error("Check the path in configuration file.")
        blank_line(1)
        return
    
    ok("Executable found at configured path.")
    
    # Verificar versión
    rvm = RVM(ruta_rvm)
    is_valid, version_info = rvm.check_version()
    
    blank_line(1)
    
    if is_valid:
        ok("RetroVirtualMachine is properly configured and ready to use.")
        blank_line(1)
    else:
        error("RetroVirtualMachine version check failed.")
        error(version_info)
        error("")
        error("Required version:")
        error(f"  {RVM.REQUIRED_VERSION}")
        error(f"  MacOs x64 Build: 6783 - (Tue Jul  9 18:18:12 2019 UTC)")
        blank_line(1)


@rvm_group.command(cls=CustomCommand, name='config')
def config():
    """Configure RetroVirtualMachine executable path.
    
    Interactive prompt to set the path to RetroVirtualMachine.
    
    Validates that:
    - The path exists
    - The executable is accessible
    - The version matches the required version
    """
    blank_line(1)
    
    # Obtener configuración actual
    config_manager = ConfigManager()
    current_path = config_manager.get("emulator", "retro_virtual_machine_path", "")
    
    # Mostrar path actual si existe
    if current_path:
        info2(f"Current path: {current_path}")
        blank_line(1)
    
    # Prompt para la ruta
    path = questionary.path(
        "Enter the path to RetroVirtualMachine (.app or executable):",
        default=current_path if current_path else "/Applications/",
        only_directories=False
    ).ask()
    
    # Si el usuario cancela (Ctrl+C o ESC)
    if path is None:
        blank_line(1)
        warn("Configuration cancelled.")
        blank_line(1)
        return
    
    rvm_path = Path(path).resolve()
    
    # Verificar que existe
    if not rvm_path.exists():
        blank_line(1)
        error(f"Path does not exist: {rvm_path}")
        blank_line(1)
        return
    
    blank_line(1)
    info2(f"Validating: {rvm_path}")
    
    # Crear instancia de RVM y verificar versión
    rvm = RVM(str(rvm_path))
    is_valid, version_info = rvm.check_version()
    
    if not is_valid:
        blank_line(1)
        error("Version validation failed.")
        error(version_info)
        error("")
        error("Required version:")
        error(f"  {RVM.REQUIRED_VERSION}")
        error(f"  MacOs x64 Build: 6783 - (Tue Jul  9 18:18:12 2019 UTC)")
        blank_line(1)
        return
    
    # Si la validación es correcta, guardar en configuración
    config_manager.set("emulator", "retro_virtual_machine_path", str(rvm_path))
    
    blank_line(1)
    ok("RetroVirtualMachine path configured successfully.")
    ok(f"Path: {rvm_path}")
    blank_line(1)
