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
import sys
import io

class FormattedStderr:
    """Wrapper for stderr that adds formatting to Click error messages"""
    def __init__(self, original_stderr):
        self.original_stderr = original_stderr
        self.buffer = []
        self.in_error_sequence = False
    
    def write(self, text):
        if isinstance(text, str):
            # Detectar inicio de secuencia de error
            if text.startswith('Usage:') and not self.in_error_sequence:
                self.in_error_sequence = True
                self.original_stderr.write('\n')  # Línea en blanco antes
                self.original_stderr.write(text)
                return len(text)
            elif 'Error:' in text and self.in_error_sequence:
                self.original_stderr.write(text)
                self.original_stderr.write('\n')  # Línea en blanco después
                self.in_error_sequence = False
                return len(text)
            else:
                self.original_stderr.write(text)
                return len(text)
        else:
            return self.original_stderr.write(text)
    
    def flush(self):
        return self.original_stderr.flush()
    
    def __getattr__(self, name):
        return getattr(self.original_stderr, name)

# Aplicar el wrapper solo cuando se inicializa el módulo
if not hasattr(sys.stderr, '_cpcready_wrapped'):
    sys.stderr = FormattedStderr(sys.stderr)
    sys.stderr._cpcready_wrapped = True

class CustomCommand(click.Command):
    def __init__(self, *args, **kwargs):
        self.show_banner = kwargs.pop('show_banner', False)
        super().__init__(*args, **kwargs)
    
    def get_help(self, ctx):
        help_text = super().get_help(ctx)
        if self.show_banner:
            try:
                from cpcready.utils.version import show_banner
                show_banner()  # Imprime el banner con Rich en color
            except ImportError:
                pass
        return f"\n{help_text}\n"

class CustomGroup(click.Group):
    def __init__(self, *args, **kwargs):
        self.show_banner = kwargs.pop('show_banner', False)
        super().__init__(*args, **kwargs)
    
    def get_help(self, ctx):
        help_text = super().get_help(ctx)
        if self.show_banner:
            try:
                from cpcready.utils.version import show_banner
                show_banner()  # Imprime el banner con Rich en color
            except ImportError:
                pass
        return f"\n{help_text}\n"
    
    def command(self, *args, **kwargs):
        """Override command to use CustomCommand by default"""
        kwargs.setdefault('cls', CustomCommand)
        return super().command(*args, **kwargs)
