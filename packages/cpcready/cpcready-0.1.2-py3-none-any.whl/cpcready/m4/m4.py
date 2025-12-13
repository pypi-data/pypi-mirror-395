
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


from rich.console import Console
import sys

import click
import questionary
from pathlib import Path
from cpcready.utils.click_custom import CustomCommand, CustomGroup
from cpcready.utils.console import info2, ok, error, warn, blank_line
from cpcready.utils.toml_config import ConfigManager
from cpcready.utils.m4board import M4Board

console = Console()



@click.group(cls=CustomGroup)
def m4():
    """M4Board management commands."""
    pass


@m4.command(cls=CustomCommand)
def status():
    """Check M4Board connection status."""
    blank_line(1)
    
    console.print("[bold yellow]\n⚠️ This feature is under development.\nExiting...\n[/bold yellow]")
    sys.exit(0)
    
    # Obtener configuración
    config = ConfigManager()
    ip = config.get("m4board", "ip", "")
    
    if not ip:
        error("M4Board IP not configured.")
        error("Use 'cpc m4 config' to configure the IP address.")
        blank_line(1)
        return
    
    info2(f"M4Board IP: {ip}")
    
    # Verificar conexión
    try:
        m4 = M4Board(ip)
        if m4.check_connection():
            ok("M4Board is reachable and ready.")
        else:
            error("M4Board is not reachable.")
            error("Check that:")
            error("  - M4Board is powered on")
            error("  - Network connection is working")
            error("  - IP address is correct")
    except Exception as e:
        error(f"Error: {e}")
    
    blank_line(1)


@m4.command(cls=CustomCommand)
def config():
    """Configure M4Board IP address."""
    blank_line(1)
    console.print("[bold yellow]\n⚠️ This feature is under development.\nExiting...\n[/bold yellow]")
    sys.exit(0)
    # Obtener configuración actual
    config_manager = ConfigManager()
    current_ip = config_manager.get("m4board", "ip", "")
    
    if current_ip:
        info2(f"Current IP: {current_ip}")
        blank_line(1)
    
    # Prompt para la IP
    ip = questionary.text(
        "Enter M4Board IP address:",
        default=current_ip if current_ip else "192.168.1."
    ).ask()
    
    # Si el usuario cancela
    if ip is None:
        blank_line(1)
        warn("Configuration cancelled.")
        blank_line(1)
        return
    
    blank_line(1)
    info2(f"Testing connection to {ip}...")
    
    # Verificar conexión
    try:
        m4 = M4Board(ip)
        if m4.check_connection():
            ok("Connection successful!")
            
            # Guardar configuración
            config_manager.set("m4board", "ip", ip)
            blank_line(1)
            ok(f"M4Board IP configured: {ip}")
        else:
            error("Cannot connect to M4Board at this IP.")
            error("Configuration not saved.")
    except Exception as e:
        error(f"Error: {e}")
        error("Configuration not saved.")
    
    blank_line(1)


@m4.command(cls=CustomCommand)
def reset_m4():
    """Reset M4Board."""
    blank_line(1)
    console.print("[bold yellow]\n⚠️ This feature is under development.\nExiting...\n[/bold yellow]")
    sys.exit(0)
    try:
        m4 = M4Board()
        m4.reset_m4()
    except Exception as e:
        error(f"Error: {e}")
    
    blank_line(1)


@m4.command(cls=CustomCommand)
def reset_cpc():
    """Reset CPC."""
    blank_line(1)
    console.print("[bold yellow]\n⚠️ This feature is under development.\nExiting...\n[/bold yellow]")
    sys.exit(0)
    try:
        m4 = M4Board()
        m4.reset_cpc()
    except Exception as e:
        error(f"Error: {e}")
    
    blank_line(1)


@m4.command(cls=CustomCommand)
@click.argument("file_path", type=click.Path(exists=True))
@click.option("-d", "--destination", default="/", help="Destination directory on SD card")
@click.option("-h", "--header", is_flag=True, help="Add AMSDOS header")
def push(file_path, destination, header):
    """Upload a file to M4Board SD card.
    
    FILE_PATH: Local file to upload
    """
    blank_line(1)
    console.print("[bold yellow]\n⚠️ This feature is under development.\nExiting...\n[/bold yellow]")
    sys.exit(0)
    try:
        m4 = M4Board()
        m4.upload_file(file_path, destination, with_header=header)
    except Exception as e:
        error(f"Error: {e}")
    
    blank_line(1)


@m4.command(cls=CustomCommand)
@click.argument("cpc_path")
@click.option("-o", "--output", default=None, help="Local output file path")
def pull(cpc_path, output):
    """Download a file from M4Board SD card.
    
    CPC_PATH: File path on M4Board SD card
    """
    blank_line(1)
    console.print("[bold yellow]\n⚠️ This feature is under development.\nExiting...\n[/bold yellow]")
    sys.exit(0)
    try:
        m4 = M4Board()
        m4.download_file(cpc_path, local_path=output)
    except Exception as e:
        error(f"Error: {e}")
    
    blank_line(1)


@m4.command(cls=CustomCommand)
@click.argument("cpc_file")
def exec(cpc_file):
    """Execute a file on CPC.
    
    CPC_FILE: File path on M4Board SD card to execute
    """
    blank_line(1)
    console.print("[bold yellow]\n⚠️ This feature is under development.\nExiting...\n[/bold yellow]")
    sys.exit(0)
    try:
        m4 = M4Board()
        m4.execute(cpc_file)
    except Exception as e:
        error(f"Error: {e}")
    
    blank_line(1)


@m4.command(cls=CustomCommand)
@click.argument("file_path", type=click.Path(exists=True))
@click.option("-d", "--destination", default="/tmp", help="Destination directory (default: /tmp)")
def run(file_path, destination):
    """Upload and execute a file on CPC.
    
    FILE_PATH: Local file to upload and execute
    """
    blank_line(1)
    console.print("[bold yellow]\n⚠️ This feature is under development.\nExiting...\n[/bold yellow]")
    sys.exit(0)
    try:
        m4 = M4Board()
        file_name = Path(file_path).name
        
        # Subir archivo
        if m4.upload_file(file_path, destination, with_header=False):
            # Ejecutar
            cpc_path = f"{destination}/{file_name}".replace("//", "/")
            m4.execute(cpc_path)
    except Exception as e:
        error(f"Error: {e}")
    
    blank_line(1)


@m4.command(cls=CustomCommand)
@click.argument("folder")
def mkdir(folder):
    """Create a directory on M4Board SD card.
    
    FOLDER: Directory path to create
    """
    blank_line(1)
    console.print("[bold yellow]\n⚠️ This feature is under development.\nExiting...\n[/bold yellow]")
    sys.exit(0)
    try:
        m4 = M4Board()
        m4.mkdir(folder)
    except Exception as e:
        error(f"Error: {e}")
    
    blank_line(1)


@m4.command(cls=CustomCommand)
@click.argument("folder")
def cd(folder):
    """Change current directory on CPC.
    
    FOLDER: Directory path
    """
    blank_line(1)
    console.print("[bold yellow]\n⚠️ This feature is under development.\nExiting...\n[/bold yellow]")
    sys.exit(0)
    try:
        m4 = M4Board()
        m4.cd(folder)
    except Exception as e:
        error(f"Error: {e}")
    
    blank_line(1)


@m4.command(cls=CustomCommand)
@click.argument("cpc_file")
def rm(cpc_file):
    """Remove a file or empty directory on CPC.
    
    CPC_FILE: File or directory to remove
    """
    blank_line(1)
    console.print("[bold yellow]\n⚠️ This feature is under development.\nExiting...\n[/bold yellow]")
    sys.exit(0)
    try:
        m4 = M4Board()
        m4.rm(cpc_file)
    except Exception as e:
        error(f"Error: {e}")
    
    blank_line(1)


@m4.command(cls=CustomCommand)
def pause():
    """Pause CPC execution."""
    blank_line(1)
    console.print("[bold yellow]\n⚠️ This feature is under development.\nExiting...\n[/bold yellow]")
    sys.exit(0)
    try:
        m4 = M4Board()
        m4.pause()
    except Exception as e:
        error(f"Error: {e}")
    
    blank_line(1)


@m4.command(cls=CustomCommand)
@click.argument("folder", default="")
def ls(folder):
    """List files in a directory on CPC.
    
    FOLDER: Directory to list (default: current directory)
    """
    blank_line(1)
    console.print("[bold yellow]\n⚠️ This feature is under development.\nExiting...\n[/bold yellow]")
    sys.exit(0)
    try:
        m4 = M4Board()
        listing = m4.ls(folder)
        
        if listing:
            print(listing)
    except Exception as e:
        error(f"Error: {e}")
    
    blank_line(1)
