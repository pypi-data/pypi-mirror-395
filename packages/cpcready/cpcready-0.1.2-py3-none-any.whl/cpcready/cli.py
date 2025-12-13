
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
from cpcready.drive import drive
from cpcready.disc import disc
from cpcready.save import save
from cpcready.era import era
from cpcready.list import list
from cpcready.filextr.filextr import filextr
from cpcready.cat.cat import cat
from cpcready.user.user import user
from cpcready.ren.ren import ren
from cpcready.model.model import model
from cpcready.mode.mode import mode
from cpcready.run import run
from cpcready.rvm.rvm import rvm_group
from cpcready.emu.emu import emu
# from cpcready.m4.m4 import m4 as m4_group
# from cpcready.header import header
from cpcready.utils.click_custom import CustomGroup, CustomCommand
from cpcready.utils.console import message, blank_line
from cpcready import __version__
from cpcready.utils.version import add_version_option_to_group, show_version_info
from cpcready.utils.update import show_update_notification

@add_version_option_to_group
@click.group(cls=CustomGroup, invoke_without_command=True, show_banner=True)
@click.pass_context
def cli(ctx):
    """Toolchain CLI for Amstrad CPC."""
    # # Mostrar notificación de actualización si la hay
    # show_update_notification()
    
    # Si no hay comando, mostrar ayuda
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

@cli.command(cls=CustomCommand)
def version():
    """Show version information."""
    show_version_info()

# Añadir comandos al CLI principal
cli.add_command(drive, name='drive')
cli.add_command(disc)
cli.add_command(cat)
cli.add_command(save)
cli.add_command(era)
cli.add_command(user)
cli.add_command(list)
cli.add_command(ren)
cli.add_command(filextr)
cli.add_command(model)
cli.add_command(mode)
cli.add_command(run)
cli.add_command(emu)
cli.add_command(rvm_group)
# cli.add_command(m4_group)
# cli.add_command(header)

if __name__ == "__main__":
    import sys
    import os
    
    # Detectar el nombre con el que fue invocado el script
    invoked_name = os.path.basename(sys.argv[0])
    
    # Mapeo de nombres de comando a funciones
    command_map = {
        'cpc': cli,
        'disc': disc,
        'drive': drive,
        'catcpc': cat,
        'user': user,
        'save': save,
        'era': era,
        'list': list,
        'model': model,
        'mode': mode,
    }
    
    # Si fue invocado con un alias, ejecutar el comando directamente
    if invoked_name in command_map:
        command_map[invoked_name]()
    else:
        # Por defecto, ejecutar el CLI principal
        cli()

