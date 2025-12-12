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

import sys
from rich.console import Console
from rich.panel import Panel

# Crear consolas separadas para stdout y stderr
console = Console()
error_console = Console(stderr=True)

LEVELS = {"quiet": 0, "normal": 1, "verbose": 2, "debug": 3}
_current_level = LEVELS["normal"]

def set_level(level_name):
    global _current_level
    _current_level = LEVELS.get(level_name, 1)

def _should_show(required_level):
    return _current_level >= required_level

def info2(msg, level="normal"):
    if _should_show(LEVELS[level]):
        console.print(f"[cyan]◉[/cyan] {msg}")

def ok(msg, level="normal"):
    if _should_show(LEVELS[level]):
        console.print(f"[green]◉[/green] {msg}")

def warn(msg, level="normal"):
    if _should_show(LEVELS[level]):
        console.print(f"[yellow]◉[/yellow] {msg}")

def error(msg):
    # Usar la consola de error de Rich
    error_console.print(f"[red]◉[/red] {msg}")

def debug(msg):
    if _should_show(LEVELS["debug"]):
        console.print(f"[magenta][DEBUG][/magenta]  {msg}")

def banner(msg):
    console.print(Panel.fit(f"[bold green]▶ [/bold green][bold white]{msg}[/bold white]", border_style="white"))

def message(msg):
    if _should_show(LEVELS["normal"]):
        console.print(msg)

def blank_line(lines=1):
    for _ in range(lines):
        console.print("")