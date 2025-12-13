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

import os
import click
from cpcready.utils.manager import SystemCPM
from cpcready.utils.click_custom import CustomCommand
from cpcready.utils.console import ok, error, blank_line
from cpcready.utils.toml_config import ConfigManager


@click.command(cls=CustomCommand)
@click.argument("user_number", type=click.IntRange(0, 15), required=False)
def user(user_number):
    """Set user number (0-15) for current session.
    
    If no user_number is provided, displays the current user number.
    """
    system_cpm = SystemCPM()
    config = ConfigManager()
    
    # Si no se pasa argumento, mostrar el valor actual
    if user_number is None:
        current_user = system_cpm.get_user_number()
        blank_line(1)
        ok(f"Current user: {current_user}")
        blank_line(1)
        return
    
    # Guardar en TOML
    try:
        config.set("system", "user", int(user_number))
    except Exception as e:
        error(f"Failed to set user: {e}")
        return

    blank_line(1)
    ok(f"User set to {user_number}")
    blank_line(1)


