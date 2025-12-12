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
Estructuras de datos para el formato DSK de Amstrad CPC
Implementación Python de las estructuras C++ originales
"""

import struct
from typing import NamedTuple, List


# Constantes
SECTSIZE = 512
USER_DELETED = 0xE5
MAX_TRACKS = 84
MAX_SECTORS = 29
AMSDOS_HEADER_SIZE = 128  # Tamaño de la cabecera AMSDOS en bytes


class CPCEMUHeader(NamedTuple):
    """
    Cabecera del archivo DSK (0x100 bytes)
    Equivalente a CPCEMUEnt en C++
    """
    magic: bytes  # "MV - CPCEMU Disk-File\r\nDisk-Info\r\n"
    nb_tracks: int  # Número de pistas (típicamente 40 o 42)
    nb_heads: int  # Número de caras (1 o 2)
    data_size: int  # Tamaño de cada pista (0x1300 = 256 + 512*9)

    @classmethod
    def from_bytes(cls, data: bytes):
        """Construye la cabecera desde bytes"""
        if len(data) < 0x100:
            raise ValueError("Datos insuficientes para cabecera DSK")
        
        magic = data[0:0x30]
        nb_tracks = data[0x30]
        nb_heads = data[0x31]
        data_size = struct.unpack('<H', data[0x32:0x34])[0]
        
        return cls(magic, nb_tracks, nb_heads, data_size)
    
    def to_bytes(self) -> bytes:
        """Convierte la cabecera a bytes"""
        result = bytearray(0x100)
        result[0:0x30] = self.magic.ljust(0x30, b'\x00')
        result[0x30] = self.nb_tracks
        result[0x31] = self.nb_heads
        struct.pack_into('<H', result, 0x32, self.data_size)
        return bytes(result)


class CPCEMUSector(NamedTuple):
    """
    Información de un sector
    Equivalente a CPCEMUSect en C++
    """
    C: int  # Track
    H: int  # Head
    R: int  # Sector ID
    N: int  # Sector size (2 = 512 bytes)
    size_bytes: int  # Tamaño real en bytes

    @classmethod
    def from_bytes(cls, data: bytes, offset: int = 0):
        """Construye información de sector desde bytes"""
        C = data[offset]
        H = data[offset + 1]
        R = data[offset + 2]
        N = data[offset + 3]
        # Offset +4 y +5 son unused (Un1)
        size_bytes = struct.unpack('<H', data[offset + 6:offset + 8])[0]
        return cls(C, H, R, N, size_bytes)
    
    def to_bytes(self) -> bytes:
        """Convierte información de sector a bytes"""
        result = bytearray(8)
        result[0] = self.C
        result[1] = self.H
        result[2] = self.R
        result[3] = self.N
        struct.pack_into('<H', result, 6, self.size_bytes)
        return bytes(result)


class CPCEMUTrack(NamedTuple):
    """
    Información de una pista
    Equivalente a CPCEMUTrack en C++
    """
    track: int
    head: int
    sect_size: int  # Tamaño de sector (2 = 512 bytes)
    nb_sect: int  # Número de sectores
    gap3: int  # Gap 3 (típicamente 0x4E)
    filler: int  # Byte de relleno (típicamente 0xE5)
    sectors: List[CPCEMUSector]

    @classmethod
    def from_bytes(cls, data: bytes, offset: int = 0):
        """Construye información de pista desde bytes"""
        # "Track-Info\r\n" (0x10 bytes)
        track = data[offset + 0x10]
        head = data[offset + 0x11]
        # +0x12 y +0x13 son unused
        sect_size = data[offset + 0x14]
        nb_sect = data[offset + 0x15]
        gap3 = data[offset + 0x16]
        filler = data[offset + 0x17]
        
        # Leer información de sectores (máximo 29)
        sectors = []
        for i in range(nb_sect):
            sect_offset = offset + 0x18 + (i * 8)
            sector = CPCEMUSector.from_bytes(data, sect_offset)
            sectors.append(sector)
        
        return cls(track, head, sect_size, nb_sect, gap3, filler, sectors)
    
    def to_bytes(self) -> bytes:
        """Convierte información de pista a bytes (256 bytes)"""
        result = bytearray(0x100)
        result[0:0x10] = b'Track-Info\r\n\x00\x00\x00\x00'
        result[0x10] = self.track
        result[0x11] = self.head
        result[0x14] = self.sect_size
        result[0x15] = self.nb_sect
        result[0x16] = self.gap3
        result[0x17] = self.filler
        
        # Escribir información de sectores
        for i, sector in enumerate(self.sectors):
            offset = 0x18 + (i * 8)
            result[offset:offset + 8] = sector.to_bytes()
        
        return bytes(result)


class DirEntry(NamedTuple):
    """
    Entrada de directorio AMSDOS
    Equivalente a StDirEntry en C++
    """
    user: int  # Número de usuario (0-15, 0xE5=borrado)
    name: str  # Nombre del archivo (8 caracteres)
    ext: str  # Extensión (3 caracteres)
    num_page: int  # Número de página/extent
    nb_pages: int  # Número de páginas usadas
    blocks: List[int]  # Lista de bloques ocupados (máximo 16)

    @classmethod
    def from_bytes(cls, data: bytes, offset: int = 0):
        """Construye entrada de directorio desde bytes"""
        user = data[offset]
        name = data[offset + 1:offset + 9].decode('ascii', errors='ignore').rstrip()
        ext = data[offset + 9:offset + 12].decode('ascii', errors='ignore').rstrip()
        num_page = data[offset + 12]
        nb_pages = data[offset + 15]
        blocks = list(data[offset + 16:offset + 32])
        
        return cls(user, name, ext, num_page, nb_pages, blocks)
    
    def to_bytes(self) -> bytes:
        """Convierte entrada de directorio a bytes (32 bytes)"""
        result = bytearray(32)
        result[0] = self.user
        result[1:9] = self.name.ljust(8, ' ').encode('ascii')
        result[9:12] = self.ext.ljust(3, ' ').encode('ascii')
        result[12] = self.num_page
        result[15] = self.nb_pages
        for i, block in enumerate(self.blocks[:16]):
            result[16 + i] = block
        
        return bytes(result)
    
    @property
    def is_deleted(self) -> bool:
        """Verifica si la entrada está marcada como borrada"""
        return self.user == USER_DELETED
    
    @property
    def full_name(self) -> str:
        """Retorna el nombre completo del archivo"""
        if self.ext:
            return f"{self.name}.{self.ext}"
        return self.name
