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

"""
CPCReady Interactive Console with bottom toolbar
"""

import click
import subprocess
import shlex
from pathlib import Path
from typing import Tuple
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import HTML

from cpcready.utils.toml_config import ConfigManager
from cpcready.utils.click_custom import CustomCommand


def get_bottom_toolbar():
    """Get bottom toolbar with system status"""
    config = ConfigManager()
    parts = []
    
    # Logo Amstrad: ● en rojo, verde y azul (igual que los iconos de unidad)
    logo = '<style fg="ansired">●</style><style fg="ansigreen">●</style><style fg="ansiblue">●</style>'
    # Model info first
    try:
        model = config.get("system", "model", "464")
        if model == "464":
            kb="64K"
        elif model == "664":
            kb="64K"
        elif model == "6128":
            kb="128K"
        else:
            kb="N/A"
        parts.append(f"{logo} Amstrad CPC {model} {kb}")
    except:
        parts.append(f"{logo} CPC: N/A")
    
    # Drive A info
    try:
        drive_select = config.get("drive", "selected_drive", "a").upper()
        drive_a_path = config.get("drive", "drive_a", "N/A")
        disk_a_path = Path(drive_a_path)
        disk_a_name = disk_a_path.name if disk_a_path.exists() else "Empty"
        disk_a_status = "✓" if disk_a_path.exists() else "○"
        # Icon change for selected/not selected
        icon_a = '●' if drive_select == "A" else '○'
        parts.append(f"A:{icon_a} {disk_a_status} {disk_a_name}")
    except:
        parts.append("A: N/A")
    
    # Drive B info
    try:
        drive_select = config.get("drive", "selected_drive", "a").upper()
        drive_b_path = config.get("drive", "drive_b", "N/A")
        disk_b_path = Path(drive_b_path)
        disk_b_name = disk_b_path.name if disk_b_path.exists() else "Empty"
        disk_b_status = "✓" if disk_b_path.exists() else "○"
        # Icon change for selected/not selected
        icon_b = '●' if drive_select == "B" else '○'
        parts.append(f"B:{icon_b} {disk_b_status} {disk_b_name}")
    except:
        parts.append("B: N/A")
    
    # Emulator info
    try:
        emulator = config.get("emulator", "selected", "N/A")
        if emulator == "RetroVirtualMachine":
            parts.append("Emulator: RVM")
        elif emulator == "M4Board":
            m4_ip = config.get("m4board", "ip", "Not configured")
            parts.append(f"Emulator: M4 ({m4_ip})")
        else:
            parts.append(f"Emulator: {emulator}")
    except:
        parts.append("Emulator: N/A")
    
    # Video mode from [system] section
    try:
        video_mode = config.get("system", "mode", 2)
        parts.append(f"Mode: {video_mode}")
    except:
        parts.append("Mode: N/A")
    
        # Concatenar el logo al principio del HTML
    return HTML(f"<b>{' │ '.join(parts)}</b>")


class CommandParser:
    """Parse and execute commands"""
    
    CPC_COMMANDS = [
        "save", "cat", "disc", "drive", "run", "version",
        "rvm", "emu", "m4"
    ]
    
    @staticmethod
    def parse(command_line: str) -> Tuple[str, list]:
        """Parse command line"""
        if not command_line.strip():
            return ('empty', [])
        
        parts = shlex.split(command_line)
        if not parts:
            return ('empty', [])
        
        cmd = parts[0]
        
        if cmd in ('exit', 'quit', 'q'):
            return ('exit', [])
        
        if cmd in ('help', '?'):
            return ('help', parts[1:])
        
        if cmd == 'clear':
            return ('clear', [])
        
        if cmd in CommandParser.CPC_COMMANDS:
            return ('cpc', parts)
        
        return ('system', parts)
    
    @staticmethod
    def execute_cpc(args: list) -> int:
        """Execute CPC command"""
        try:
            cmd = ['poetry', 'run', 'cpc'] + args
            result = subprocess.run(
                cmd,
                cwd='/Users/destroyer/PROJECTS/CPCReady/cpc'
            )
            return result.returncode
        except Exception as e:
            print(f"Error: {e}")
            return 1
    
    @staticmethod
    def execute_cd(args: list) -> int:
        """Execute cd command"""
        try:
            import os
            if len(args) == 1:
                # cd sin argumentos va al home
                os.chdir(os.path.expanduser("~"))
            else:
                # cd con ruta
                os.chdir(os.path.expanduser(args[1]))
            return 0
        except FileNotFoundError:
            print(f"cd: no such file or directory: {args[1] if len(args) > 1 else '~'}")
            return 1
        except Exception as e:
            print(f"cd: {e}")
            return 1
    
    @staticmethod
    def execute_system(args: list) -> int:
        """Execute system command"""
        try:
            result = subprocess.run(args)
            return result.returncode
        except FileNotFoundError:
            print(f"Command not found: {args[0]}")
            return 127
        except Exception as e:
            print(f"Error: {e}")
            return 1
    
    @staticmethod
    def show_help():
        """Show help"""
        print("""
╭─────────────────────────────────────────────────────╮
│          CPCReady Interactive Console Help          │
╰─────────────────────────────────────────────────────╯

CPC Commands:
  save, cat, disc, drive, run, version, rvm, emu, m4

System Commands:
  ls, cd, pwd, cat, grep, find, echo, etc.

Special:
  help, ?          Show this help
  clear            Clear screen
  exit, quit, q    Exit console

Shortcuts:
  Ctrl+C, Ctrl+D   Exit console
""")


def get_all_completions() -> list:
    """Get all completions"""
    return (
        CommandParser.CPC_COMMANDS +
        ['exit', 'quit', 'q', 'help', 'clear', 'cd', 'ls', 'pwd']
    )


@click.command(cls=CustomCommand)
def console():
    """
    Interactive console with bottom status toolbar
    
    The console displays a bottom toolbar with real-time information about:
    - Current drives and disks (A and B)
    - Selected emulator
    - CPC model configuration
    
    Examples:
        cpc console
        
        # In console:
        > disc info
        > drive status
        > ls -la
        > help
        > exit
    """
    parser = CommandParser()
    
    # Word completer
    completer = WordCompleter(
        get_all_completions(),
        ignore_case=True,
    )
    
    # Crear historial persistente de comandos
    from prompt_toolkit.history import FileHistory
    import os
    history_path = os.path.expanduser("~/.config/cpcready/console_history.txt")
    session = PromptSession(
        completer=completer,
        complete_while_typing=True,
        bottom_toolbar=get_bottom_toolbar,
        history=FileHistory(history_path),
    )
    
    # Welcome message based on CPC model
    config = ConfigManager()
    model = config.get("system", "model", "464")
    
    # Limpiar la consola al arrancar (usando print builtin)
    import builtins
    builtins.print("\033[2J\033[H", end="")
    
    from rich import print
    from rich.panel import Panel
    from rich.console import Console
    from rich.align import Align
    
    console_rich = Console()
    
    # Panel responsive con el título centrado en 3 líneas
    content = Align.center("[bold][red]█[/red][green]█[/green][blue]█[/blue][/bold] [bold yellow]CPCReady Console[/bold yellow]")
    panel = Panel(
        content,
        expand=True,
        border_style="yellow",
        padding=(1, 0)  # 1 línea arriba y abajo, 0 a los lados
    )
    print("\n")
    console_rich.print(panel)
    
    print()
    # print("[bold][red]█[/red][green]█[/green][blue]█[/blue][/bold]")

    print("\nType 'help' for assistance, 'exit' to quit\n")
    
    # Main loop
    while True:
        try:
            # Obtener directorio currente para el prompt
            import os
            current_dir = os.getcwd()
            home = os.path.expanduser("~")
            # Reemplazar home por ~ para compactar
            if current_dir.startswith(home):
                current_dir = "~" + current_dir[len(home):]
            
            prompt_text = f'<b><style fg="yellow">\nCPCReady</style> <style fg="ansiblue">{current_dir}</style>\n</b>'
            command_line = session.prompt(HTML(prompt_text))

            cmd_type, args = parser.parse(command_line)

            # Guardar modelo antes de ejecutar
            old_model = config.get("system", "model", "464")

            if cmd_type == 'empty':
                continue

            elif cmd_type == 'exit':
                print("\nGoodbye! 👋\n")
                break

            elif cmd_type == 'help':
                parser.show_help()

            elif cmd_type == 'clear':
                print("\033[2J\033[H", end="")

            elif cmd_type == 'cpc':
                parser.execute_cpc(args)

            elif cmd_type == 'system':
                # Manejar cd de forma especial
                if args and args[0] == 'cd':
                    parser.execute_cd(args)
                else:
                    parser.execute_system(args)

        except KeyboardInterrupt:
            print("\n(Use 'exit' to quit)")
            continue
        
        except EOFError:
            print("\nGoodbye! 👋\n")
            break
        
        except Exception as e:
            print(f"Error: {e}")
            continue
