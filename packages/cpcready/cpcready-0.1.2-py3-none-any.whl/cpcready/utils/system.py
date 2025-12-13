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

import subprocess
import click
from cpcready.utils import console
from pathlib import Path

def process_dsk_name(disc_image: str):
    path = Path(disc_image)
    
    # Asegurarse de que tenga la extensión .dsk
    if path.suffix.lower() != ".dsk":
        path = path.with_suffix(".dsk")
    
    # Obtener la ruta absoluta
    if len(path.parts) == 1:
        # Solo nombre de archivo - usar directorio actual
        absolute_path = Path.cwd() / path
    else:
        # Incluye una ruta (relativa o absoluta)
        if path.is_absolute():
            absolute_path = path
        else:
            absolute_path = path.resolve()
    
    # Crear el directorio si no existe
    parent_directory = absolute_path.parent
    if not parent_directory.exists():
        parent_directory.mkdir(parents=True, exist_ok=True)
    
    return absolute_path

def run_command(cmd, show_output=True, check=True):
    """
    Ejecuta un comando del sistema y muestra su salida en tiempo real.

    Args:
        cmd (str | list): Comando a ejecutar (por ejemplo, 'ls -l' o ['ls', '-l'])
        show_output (bool): Si True, muestra la salida directamente en consola.
        check (bool): Si True, lanza excepción si el comando devuelve error.

    Returns:
        subprocess.CompletedProcess: Resultado del comando.
    """
    console.debug(f"[DEBUG] Ejecutando comando: {cmd}")

    # Si se pasa como string, usar shell=True (para pipes o redirecciones)
    use_shell = isinstance(cmd, str)

    process = subprocess.Popen(
        cmd,
        shell=use_shell,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    output_lines = []
    for line in iter(process.stdout.readline, ''):
        line = line.strip()
        if show_output:
            click.echo(line)
        output_lines.append(line)

    process.wait()

    if check and process.returncode != 0:
        console.error(f"[ERROR] Comando falló con código {process.returncode}")
        raise subprocess.CalledProcessError(process.returncode, cmd)

    console.ok(f"[OK] Comando completado con código {process.returncode}")
    return subprocess.CompletedProcess(cmd, process.returncode, "\n".join(output_lines), "")
