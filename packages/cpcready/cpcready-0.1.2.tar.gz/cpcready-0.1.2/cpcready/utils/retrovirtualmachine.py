
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

import psutil
import subprocess
import sys
import time
import re
from pathlib import Path
from cpcready.utils.console import info2, ok, debug, error, warn  # Eliminar si no se usa ninguna función


class RVM:
    """RetroVirtualMachine emulator manager."""
    
    # Nombres posibles del ejecutable RVM
    NOMBRES_RVM = [
        "Retro Virtual Machine",
        "retrovirtualmachine",
        "RetroVirtualMachine.exe",
        "retrovirtualmachine.exe"
    ]
    
    # Versión requerida
    REQUIRED_VERSION = "Retro Virtual Machine v2.0 BETA-1 r7"
    REQUIRED_BUILD_PATTERN = r"MacOs x64 Build: 6783 - \(Tue Jul\s+9 18:18:12 2019 UTC\)"
    
    def __init__(self, ruta_ejecutable=None):
        """
        Initialize RVM manager.
        
        Args:
            ruta_ejecutable: Path to RetroVirtualMachine executable or .app
        """
        self.ruta_ejecutable = ruta_ejecutable
    
    def kill_all_instances(self):
        """Kill all previous RetroVirtualMachine instances."""
        debug("Searching for previous RetroVirtualMachine instances...")
        
        count = 0
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
            try:
                nombre = proc.info["name"] or ""
                ruta = proc.info["exe"] or ""
                cmd = " ".join(proc.info["cmdline"] or [])

                if any(t.lower() in nombre.lower() for t in self.NOMBRES_RVM) or \
                   any(t.lower() in ruta.lower() for t in self.NOMBRES_RVM) or \
                   any(t.lower() in cmd.lower() for t in self.NOMBRES_RVM):

                    debug(f"Closing: PID {proc.pid} ({nombre})")
                    proc.kill()
                    proc.wait()
                    count += 1

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if count > 0:
            info2(f"Closed {count} RetroVirtualMachine instance(s).")
        
        return count
    
    def check_version(self):
        """
        Check if RetroVirtualMachine version is the required one.
        
        Returns:
            tuple: (bool, str) - (is_valid, version_info)
                is_valid: True if version matches requirements
                version_info: Version information string or error message
        """
        if not self.ruta_ejecutable:
            return False, "RetroVirtualMachine path not configured."
        
        # Verificar que existe
        if not Path(self.ruta_ejecutable).exists():
            return False, f"RetroVirtualMachine not found at: {self.ruta_ejecutable}"
        
        try:
            # Construir comando según plataforma
            if sys.platform == "darwin" and self.ruta_ejecutable.endswith(".app"):
                # macOS con .app: buscar el binario dentro del bundle
                app_path = Path(self.ruta_ejecutable)
                macos_dir = app_path / "Contents" / "MacOS"
                
                if not macos_dir.exists():
                    return False, "Cannot find Contents/MacOS directory in .app bundle"
                
                # Buscar cualquier archivo ejecutable
                possible_binaries = [f for f in macos_dir.iterdir() if f.is_file() and not f.name.startswith('.')]
                
                if not possible_binaries:
                    return False, "Cannot find RVM binary inside .app bundle"
                
                # Usar el primer ejecutable encontrado
                comando = [str(possible_binaries[0]), "-nocolor", "--help"]
            else:
                comando = [self.ruta_ejecutable, "-nocolor", "--help"]
            
            debug(f"Checking version: {' '.join(comando)}")
            
            # Ejecutar comando y capturar salida
            result = subprocess.run(
                comando,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # La salida puede estar en stdout o stderr
            output = result.stdout + result.stderr
            
            debug(f"RVM output:\n{output[:300]}")
            
            # Verificar versión exacta
            version_found = self.REQUIRED_VERSION in output
            build_found = re.search(self.REQUIRED_BUILD_PATTERN, output) is not None
            
            if version_found and build_found:
                ok(f"Version verified: {self.REQUIRED_VERSION}")
                return True, self.REQUIRED_VERSION
            else:
                # Intentar extraer la versión que se encontró
                version_match = re.search(r"Retro Virtual Machine v[\d\.]+ BETA-\d+ r\d+", output)
                found_version = version_match.group(0) if version_match else "Unknown version"
                
                warn(f"Version mismatch!")
                warn(f"Required: {self.REQUIRED_VERSION}")
                warn(f"Found: {found_version}")
                
                return False, f"Version mismatch. Required: {self.REQUIRED_VERSION}, Found: {found_version}"
        
        except subprocess.TimeoutExpired:
            return False, "Timeout checking RVM version"
        except FileNotFoundError:
            return False, f"Executable not found: {self.ruta_ejecutable}"
        except Exception as e:
            return False, f"Error checking version: {e}"
    
    def launch(self, modelo, archivo_dsk=None, archivo_ejecutar=None, wait_after_kill=0.5):
        """
        Launch RetroVirtualMachine with the specified parameters.
        
        Args:
            modelo: CPC model (464, 664, 6128)
            archivo_dsk: DSK file to load (optional)
            archivo_ejecutar: File to execute automatically from disk (optional)
            wait_after_kill: Seconds to wait after killing previous instances
            
        Returns:
            bool: True if launched successfully, False otherwise
        """
        if not self.ruta_ejecutable:
            error("RetroVirtualMachine path not configured.")
            return False
        
        # Verificar que existe
        if not Path(self.ruta_ejecutable).exists():
            error(f"RetroVirtualMachine not found at: {self.ruta_ejecutable}")
            error("Check the path in configuration file.")
            return False
        
        # Matar instancias previas
        self.kill_all_instances()
        if wait_after_kill > 0:
            time.sleep(wait_after_kill)
        
        # Construir parámetros
        parametros = [f"-b=cpc{modelo}"]
        
        if archivo_dsk:
            parametros.extend(["-i", archivo_dsk])
        
        if archivo_ejecutar:
            # Comando para ejecutar el archivo: run"archivo"\n
            parametros.append(f'-c=run"{archivo_ejecutar}"\\n')
        
        debug(f"Parámetros: {' '.join(parametros)}")
        
        # Detectar si es macOS y la ruta es .app
        if sys.platform == "darwin" and self.ruta_ejecutable.endswith(".app"):
            # En macOS, usar 'open -a' para aplicaciones .app
            comando = ["open", "-a", self.ruta_ejecutable, "--args"] + parametros
        else:
            # Windows/Linux o ruta directa al binario
            comando = [self.ruta_ejecutable] + parametros
            info2(f"Launching: {' '.join(comando)}")
        
        try:
            if sys.platform.startswith("win"):
                # Windows: usar DETACHED_PROCESS para desconectar completamente
                DETACHED_PROCESS = 0x00000008
                subprocess.Popen(
                    comando, 
                    creationflags=DETACHED_PROCESS,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL
                )
            else:
                # Unix/Linux/macOS: usar start_new_session
                subprocess.Popen(
                    comando,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True
                )
            
            ok("RetroVirtualMachine launched successfully.")
            return True
            
        except FileNotFoundError:
            error(f"Executable not found: {self.ruta_ejecutable}")
            error("Check the path in configuration file.")
            return False
        except Exception as e:
            error(f"Error launching RetroVirtualMachine: {e}")
            return False
