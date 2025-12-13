
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

"""
Version utilities for cpcready commands.

Provides common version functionality for all commands.
"""

import click
from functools import wraps
from cpcready import __version__, __author__, __license__
from cpcready.utils.console import message, blank_line,warn
from rich import print as rprint

def show_banner():
    """Display ASCII art banner."""
    from rich.console import Console
    console = Console()
    blank_line()
    console.print("▞▀▖▛▀▖▞▀▖▛▀▖        ▌   ", style="bold yellow")
    console.print("▌  ▙▄▘▌  ▙▄▘▞▀▖▝▀▖▞▀▌▌ ▌", style="bold yellow")
    console.print("▌ ▖▌  ▌ ▖▌▚ ▛▀ ▞▀▌▌ ▌▚▄▌", style="bold yellow")
    console.print("▝▀ ▘  ▝▀ ▘ ▘▝▀▘▝▀▘▝▀▘▗▄▘", style="bold yellow")
    console.print(f"CLI Toolchain v{__version__}", style="yellow", highlight=False)
    console.print(f"Copyright (c) 2025 {__author__}", style="yellow", highlight=False)
    console.print(f"License: {__license__}", style="yellow", highlight=False)
    console.print("Repository: https://github.com/CPCReady/cpc", style="yellow")
    console.print("Issue Tracker: https://github.com/CPCReady/cpc/issues", style="yellow")
    console.print("Docs: https://cpcready.github.io/docs", style="yellow")
    blank_line()


def show_version_info():
    """Display version information."""
    show_banner()


def version_option_handler(ctx, param, value):
    """Click callback handler for --version option."""
    if not value or ctx.resilient_parsing:
        return
    show_version_info()
    ctx.exit()


def add_version_option(f):
    """
    Decorator to add --version option to any Click command.
    
    Usage:
        @add_version_option
        @click.command()
        def my_command():
            pass
    """
    return click.option('--version', is_flag=True, expose_value=False, 
                       is_eager=True, callback=version_option_handler,
                       help='Show version and exit')(f)


def add_version_option_to_group(f):
    """
    Decorator to add --version option to Click groups.
    
    Usage:
        @add_version_option_to_group
        @click.group()
        def my_group():
            pass
    """
    return click.option('--version', is_flag=True, expose_value=False,
                       is_eager=True, callback=version_option_handler,
                       help='Show version and exit')(f)