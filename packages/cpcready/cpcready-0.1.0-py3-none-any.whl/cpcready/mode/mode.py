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
from cpcready.utils import SystemCPM
from cpcready.utils.click_custom import CustomCommand
from cpcready.utils.console import ok, error, info2, blank_line

@click.command(cls=CustomCommand)
@click.argument("screen_mode", required=False, type=click.Choice(['0', '1', '2'], case_sensitive=False))
def mode(screen_mode):
    """Set or show current CPC screen mode.
    
    Supported modes: 0, 1, 2
    """
    system_cpm = SystemCPM()
    
    if screen_mode:
        # Set new mode
        try:
            system_cpm.set_mode(screen_mode)
            blank_line(1)
            ok(f"CPC Screen Mode set to: {screen_mode}")
            blank_line(1)
        except Exception as e:
            error(f"Error setting mode: {e}")
    else:
        # Show current mode
        current_mode = system_cpm.get_mode()
        blank_line(1)
        info2(f"Current CPC Screen Mode: {current_mode}")
        blank_line(1)
