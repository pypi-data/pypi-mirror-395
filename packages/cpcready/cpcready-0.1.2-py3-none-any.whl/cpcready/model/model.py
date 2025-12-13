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
@click.argument("model_type", required=False, type=click.Choice(['464', '664', '6128'], case_sensitive=False))
def model(model_type):
    """Set or show current CPC model.
    
    Supported models: 464, 664, 6128
    """
    system_cpm = SystemCPM()
    
    if model_type:
        # Set new model
        try:
            system_cpm.set_model(model_type)
            blank_line(1)
            ok(f"CPC Model set to: {model_type}")
            blank_line(1)
        except Exception as e:
            error(f"Error setting model: {e}")
    else:
        # Show current model
        current_model = system_cpm.get_model()
        blank_line(1)
        info2(f"Current CPC Model: {current_model}")
        blank_line(1)
