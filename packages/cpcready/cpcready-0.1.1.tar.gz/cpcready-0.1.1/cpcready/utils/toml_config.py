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
ConfigManager: Gestión de configuración usando TOML.

Reemplaza el uso de shelve por archivos TOML legibles y versionables.
"""

import os
from pathlib import Path
from typing import Any, Dict

# Python 3.11+ tiene tomllib incluido, versiones anteriores necesitan tomli
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

import tomli_w


class ConfigManager:
    """Gestor de configuración basado en TOML."""
    
    def __init__(self, config_file: str = "cpcready.toml"):
        """
        Inicializa el gestor de configuración.
        
        Args:
            config_file: Nombre del archivo de configuración
        """
        # Crear directorio ~/.config/cpcready/
        self.config_dir = Path.home() / ".config" / "cpcready"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Ruta completa del fichero
        self.config_path = self.config_dir / config_file
        
        # Asegurar que existe con estructura inicial
        self._ensure_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Retorna la configuración por defecto."""
        return {
            "drive": {
                "drive_a": "",
                "drive_b": "",
                "selected_drive": "A"
            },
            "emulator": {
                "default": "RetroVirtualMachine",
                "retro_virtual_machine_path": "",
                "m4board_ip": ""
            },
            "system": {
                "user": 0,
                "model": "6128",
                "mode": 1
            }
        }
    
    def _ensure_config(self):
        """
        Crea el archivo de configuración si no existe, o valida que tenga todas las claves y tipos.
        Si faltan claves o tipos, se añaden los valores por defecto.
        """
        default = self._default_config()
        updated = False
        if not self.config_path.exists():
            self._write(default)
            return
        # Leer config actual
        try:
            config = self._read()
        except Exception:
            self._write(default)
            return
        # Validar y completar claves y tipos
        def validate_section(section, default_section):
            if section not in config or not isinstance(config[section], dict):
                config[section] = default_section.copy()
                return True
            for key, value in default_section.items():
                if key not in config[section] or not isinstance(config[section][key], type(value)):
                    config[section][key] = value
                    return True
            return False
        for section, default_section in default.items():
            if validate_section(section, default_section):
                updated = True
        if updated:
            self._write(config)
    
    def _read(self) -> Dict[str, Any]:
        """Lee y retorna el contenido del archivo TOML."""
        if not self.config_path.exists():
            return self._default_config()
        
        with open(self.config_path, "rb") as f:
            return tomllib.load(f)
    
    def _write(self, data: Dict[str, Any]):
        """Escribe datos al archivo TOML."""
        with open(self.config_path, "wb") as f:
            tomli_w.dump(data, f)
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor de la configuración.
        
        Args:
            section: Sección del TOML (ej: "drive", "emulator")
            key: Clave dentro de la sección
            default: Valor por defecto si no existe
            
        Returns:
            El valor configurado o el default
        """
        config = self._read()
        return config.get(section, {}).get(key, default)
    
    def set(self, section: str, key: str, value: Any):
        """
        Establece un valor en la configuración.
        
        Args:
            section: Sección del TOML (ej: "drive", "emulator")
            key: Clave dentro de la sección
            value: Valor a establecer
        """
        config = self._read()
        
        # Asegurar que la sección existe
        if section not in config:
            config[section] = {}
        
        config[section][key] = value
        self._write(config)
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Obtiene una sección completa de la configuración.
        
        Args:
            section: Nombre de la sección
            
        Returns:
            Diccionario con los valores de la sección
        """
        config = self._read()
        return config.get(section, {})
    
    def set_section(self, section: str, data: Dict[str, Any]):
        """
        Reemplaza una sección completa de la configuración.
        
        Args:
            section: Nombre de la sección
            data: Diccionario con los nuevos valores
        """
        config = self._read()
        config[section] = data
        self._write(config)
    
    def reset(self):
        """Resetea la configuración a valores por defecto."""
        self._write(self._default_config())
    
    def get_all(self) -> Dict[str, Any]:
        """Retorna toda la configuración."""
        return self._read()
