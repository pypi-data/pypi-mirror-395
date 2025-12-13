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
Excepciones personalizadas para PyDSK
"""


class DSKError(Exception):
    """Excepción base para todos los errores de DSK"""
    pass


class DSKFormatError(DSKError):
    """Error en el formato del archivo DSK"""
    pass


class DSKFileNotFoundError(DSKError):
    """Archivo no encontrado en la imagen DSK"""
    pass


class DSKNoSpaceError(DSKError):
    """No hay espacio suficiente en la imagen DSK"""
    pass


class DSKFileExistsError(DSKError):
    """El archivo ya existe en la imagen DSK"""
    pass
