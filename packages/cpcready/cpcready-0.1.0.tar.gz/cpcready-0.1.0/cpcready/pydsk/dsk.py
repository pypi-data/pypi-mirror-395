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
Clase principal DSK para gestión de imágenes de disco Amstrad CPC
"""

import os
import struct
from typing import Optional, List, Tuple
from pathlib import Path

from .structures import (
    CPCEMUHeader, CPCEMUTrack, CPCEMUSector, DirEntry,
    SECTSIZE, USER_DELETED, MAX_TRACKS, AMSDOS_HEADER_SIZE
)
from .exceptions import (
    DSKError, DSKFormatError, DSKFileNotFoundError,
    DSKNoSpaceError, DSKFileExistsError
)


class DSK:
    """
    Clase para manipular imágenes DSK de Amstrad CPC
    Compatible con formato CPCEMU (estándar y extendido)
    
    Attributes:
        filename: Ruta al archivo DSK
        data: Bytes de la imagen DSK completa
        header: Cabecera CPCEMU parseada
    """
    
    # Constantes para tipos de formato
    FORMAT_DATA = 0xC1  # Formato DATA (sectores comienzan en 0xC1)
    FORMAT_SYSTEM = 0x41  # Formato SYSTEM (sectores comienzan en 0x41)
    FORMAT_VENDOR = 0x01  # Formato VENDOR (sectores comienzan en 0x01)
    
    def __init__(self, filename: Optional[str] = None):
        """
        Inicializa una imagen DSK
        
        Args:
            filename: Ruta al archivo DSK a cargar (opcional)
            
        Raises:
            DSKFileNotFoundError: Si el archivo especificado no existe
        """
        self.filename = filename
        self.data = bytearray()
        self.header: Optional[CPCEMUHeader] = None
        
        if filename:
            if not os.path.exists(filename):
                raise DSKFileNotFoundError(f"DSK file not found: {filename}")
            self.load(filename)
    
    def create(self, nb_tracks: int = 40, nb_sectors: int = 9, 
               format_type: int = FORMAT_DATA) -> None:
        """
        Crea una nueva imagen DSK vacía formateada
        
        Args:
            nb_tracks: Número de pistas (típicamente 40 o 42)
            nb_sectors: Número de sectores por pista (típicamente 9)
            format_type: Tipo de formato (FORMAT_DATA, FORMAT_SYSTEM, FORMAT_VENDOR)
        
        Raises:
            DSKError: Si los parámetros son inválidos
        
        Example:
            >>> dsk = DSK()
            >>> dsk.create(nb_tracks=40, nb_sectors=9)
            >>> dsk.save("mydisk.dsk")
        """
        if nb_tracks < 1 or nb_tracks > MAX_TRACKS:
            raise DSKError(f"Número de pistas inválido: {nb_tracks} (debe ser 1-{MAX_TRACKS})")
        
        if nb_sectors < 1 or nb_sectors > 10:
            raise DSKError(f"Número de sectores inválido: {nb_sectors} (debe ser 1-10)")
        
        if format_type not in (self.FORMAT_DATA, self.FORMAT_SYSTEM, self.FORMAT_VENDOR):
            raise DSKError(f"Tipo de formato inválido: 0x{format_type:02X}")
        
        # Calcular tamaño de cada pista: 256 bytes de header + (512 * nb_sectors) de datos
        data_size = 0x100 + (SECTSIZE * nb_sectors)
        
        # Crear cabecera
        magic = b'MV - CPCEMU Disk-File\r\nDisk-Info\r\n'
        self.header = CPCEMUHeader(
            magic=magic,
            nb_tracks=nb_tracks,
            nb_heads=1,  # Siempre 1 cara por defecto
            data_size=data_size
        )
        
        # Calcular tamaño total de la imagen
        total_size = 0x100 + (nb_tracks * data_size)
        self.data = bytearray(total_size)
        
        # Escribir cabecera
        self.data[0:0x100] = self.header.to_bytes()
        
        # Formatear cada pista
        for track in range(nb_tracks):
            self._format_track(track, format_type, nb_sectors)
    
    def _format_track(self, track_num: int, min_sect: int, nb_sectors: int) -> None:
        """
        Formatea una pista con el esquema de sectores entrelazados
        
        Args:
            track_num: Número de pista (0-based)
            min_sect: ID del primer sector (0x41, 0xC1, o 0x01)
            nb_sectors: Número de sectores en la pista
        """
        # Calcular offset de esta pista
        track_offset = 0x100 + (track_num * self.header.data_size)
        
        # Crear información de pista
        sectors = []
        sector_counter = 0
        
        # Sectores entrelazados idéntico a C++: 0, 5, 1, 6, 2, 7, 3, 8, 4
        s = 0
        while s < nb_sectors:
            # Sector par
            sector = CPCEMUSector(
                C=track_num,
                H=0,
                R=sector_counter + min_sect,
                N=2,  # 2 = 512 bytes
                size_bytes=SECTSIZE
            )
            sectors.append(sector)
            sector_counter += 1
            s += 1
            
            # Sector impar (si hay más sectores)
            if s < nb_sectors:
                sector = CPCEMUSector(
                    C=track_num,
                    H=0,
                    R=sector_counter + min_sect + 4,
                    N=2,  # 2 = 512 bytes
                    size_bytes=SECTSIZE
                )
                sectors.append(sector)
                s += 1
        
        track_info = CPCEMUTrack(
            track=track_num,
            head=0,
            sect_size=2,  # 2 = 512 bytes (128 << 2)
            nb_sect=nb_sectors,
            gap3=0x4E,
            filler=0xE5,
            sectors=sectors
        )
        
        # Escribir información de pista
        self.data[track_offset:track_offset + 0x100] = track_info.to_bytes()
        
        # Rellenar datos de sectores con 0xE5
        data_offset = track_offset + 0x100
        data_size = SECTSIZE * nb_sectors
        self.data[data_offset:data_offset + data_size] = bytes([0xE5] * data_size)
    
    def load(self, filename: str) -> None:
        """
        Carga una imagen DSK desde archivo
        
        Args:
            filename: Ruta al archivo DSK
        
        Raises:
            DSKError: Si el archivo no existe
            DSKFormatError: Si el formato del DSK es inválido
        """
        if not os.path.exists(filename):
            raise DSKError(f"Archivo no encontrado: {filename}")
        
        with open(filename, 'rb') as f:
            self.data = bytearray(f.read())
        
        # Parsear cabecera
        try:
            self.header = CPCEMUHeader.from_bytes(self.data)
        except Exception as e:
            raise DSKFormatError(f"Error al leer cabecera DSK: {e}")
        
        # Verificar magic string
        if not (self.header.magic.startswith(b'MV -') or 
                self.header.magic.startswith(b'EXTENDED CPC DSK')):
            raise DSKFormatError("Archivo DSK con formato inválido (magic string incorrecto)")
        
        self.filename = filename
    
    def save(self, filename: Optional[str] = None) -> None:
        """
        Guarda la imagen DSK a archivo
        
        Args:
            filename: Ruta donde guardar (usa self.filename si no se especifica)
        
        Raises:
            DSKError: Si no se especifica filename y no hay uno guardado
        """
        if filename:
            self.filename = filename
        
        if not self.filename:
            raise DSKError("No se especificó nombre de archivo para guardar")
        
        # Crear directorio si no existe
        Path(self.filename).parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.filename, 'wb') as f:
            f.write(self.data)
    
    def get_min_sector(self) -> int:
        """
        Obtiene el ID del primer sector de la pista 0
        
        Returns:
            ID del primer sector (0x41, 0xC1, o 0x01)
        """
        if not self.data or len(self.data) < 0x100 + 0x100:
            return 0xC1  # Default
        
        # Leer primera pista
        track = CPCEMUTrack.from_bytes(self.data, 0x100)
        
        if track.nb_sect == 0:
            return 0xC1
        
        # Encontrar el sector con ID más bajo
        min_sect = min(sector.R for sector in track.sectors)
        return min_sect
    
    def get_format_type(self) -> str:
        """
        Determina el tipo de formato del DSK
        
        Returns:
            'DATA', 'SYSTEM', 'VENDOR', o 'UNKNOWN'
        """
        min_sect = self.get_min_sector()
        
        if min_sect == self.FORMAT_DATA:
            return 'DATA'
        elif min_sect == self.FORMAT_SYSTEM:
            return 'SYSTEM'
        elif min_sect == self.FORMAT_VENDOR:
            return 'VENDOR'
        else:
            return 'UNKNOWN'
    
    def get_info(self) -> dict:
        """
        Obtiene información detallada del DSK
        
        Returns:
            Diccionario con información del DSK
        """
        if not self.header:
            return {}
        
        # Mostrar solo el nombre del archivo, no el path completo
        display_name = os.path.basename(self.filename) if self.filename else 'Sin nombre'
        
        return {
            'filename': display_name,
            'format': self.get_format_type(),
            'tracks': self.header.nb_tracks,
            'heads': self.header.nb_heads,
            'track_size': self.header.data_size,
            'total_size': len(self.data),
            'capacity_kb': (self.header.nb_tracks * 
                           (self.header.data_size - 0x100)) // 1024
        }
    
    def read_block(self, block_num: int) -> bytes:
        """
        Lee un bloque AMSDOS (2 sectores = 1024 bytes)
        
        Args:
            block_num: Número de bloque (0-based)
        
        Returns:
            1024 bytes del bloque
        """
        # Calcular track y sector
        track = (block_num << 1) // 9
        sect = (block_num << 1) % 9
        
        min_sect = self.get_min_sector()
        
        # Ajustar track según el formato
        if min_sect == 0x41:  # SYSTEM
            track += 2
        elif min_sect == 0x01:  # VENDOR
            track += 1
        
        # Leer primer sector
        pos1 = self._get_sector_position(track, sect + min_sect, physical=True)
        data1 = self.data[pos1:pos1 + SECTSIZE]
        
        # Leer segundo sector
        sect += 1
        if sect > 8:
            track += 1
            sect = 0
        
        pos2 = self._get_sector_position(track, sect + min_sect, physical=True)
        data2 = self.data[pos2:pos2 + SECTSIZE]
        
        return bytes(data1 + data2)
    
    def _get_sector_position(self, track: int, sector_id: int, physical: bool = True) -> int:
        """
        Obtiene la posición de un sector en los datos del DSK
        
        Args:
            track: Número de pista
            sector_id: ID del sector
            physical: Si True, busca por ID físico; si False, por índice
        
        Returns:
            Posición en bytes del inicio del sector
        """
        # Posición del header de la pista
        track_pos = 0x100 + (track * self.header.data_size)
        
        # Leer información de la pista
        from .structures import CPCEMUTrack
        track_info = CPCEMUTrack.from_bytes(self.data, track_pos)
        
        # Buscar el sector
        data_pos = track_pos + 0x100  # Después del header de pista
        
        for i, sector in enumerate(track_info.sectors):
            if (physical and sector.R == sector_id) or (not physical and i == sector_id):
                return data_pos
            data_pos += sector.size_bytes
        
        return data_pos
    
    def get_directory_entries(self) -> List[DirEntry]:
        """
        Obtiene todas las entradas del directorio AMSDOS
        
        Returns:
            Lista de entradas de directorio (máximo 64)
        """
        entries = []
        min_sect = self.get_min_sector()
        
        # Determinar track inicial según formato
        if min_sect == 0x41:  # SYSTEM
            track = 2
        elif min_sect == 0x01:  # VENDOR
            track = 1
        else:  # DATA
            track = 0
        
        # Leer 64 entradas (4 sectores × 16 entradas por sector)
        for dir_num in range(64):
            sector = (dir_num >> 4) + min_sect  # Cada 16 entradas cambia de sector
            entry_in_sector = dir_num & 15       # Posición dentro del sector (0-15)
            
            # Obtener posición del sector
            pos = self._get_sector_position(track, sector, physical=True)
            
            # Cada entrada ocupa 32 bytes
            entry_pos = pos + (entry_in_sector << 5)
            
            # Parsear entrada
            entry = DirEntry.from_bytes(self.data, entry_pos)
            entries.append(entry)
        
        return entries
    
    def get_free_space(self) -> int:
        """
        Calcula el espacio libre en el DSK en KB
        
        Returns:
            Espacio libre en kilobytes
        """
        entries = self.get_directory_entries()
        
        # Contar bloques usados
        used_blocks = set()
        for entry in entries:
            if not entry.is_deleted and entry.nb_pages > 0:
                for block in entry.blocks:
                    if block != 0:
                        used_blocks.add(block)
        
        # Capacidad estándar: 178 KB
        # Cada bloque = 1 KB
        used_kb = len(used_blocks)
        total_capacity = 178
        
        return total_capacity - used_kb
    
    def list_files(self, simple: bool = False, use_rich: bool = True, show_title: bool = True) -> str:
        """
        Lista los archivos del directorio AMSDOS
        
        Args:
            simple: Si True, formato compacto; si False, tabla detallada
            use_rich: Si True y Rich está disponible, usa formato Rich con colores
            show_title: Si True, muestra el título con el nombre del archivo; si False, no muestra título
        
        Returns:
            String con el listado formateado o None si usa Rich (imprime directamente)
        """
        entries = self.get_directory_entries()
        
        # Intentar usar Rich si está disponible y solicitado
        if use_rich and not simple:
            try:
                from rich.console import Console
                from rich.table import Table
                from rich.panel import Panel
                from rich import box
                
                console = Console()
                
                # Crear tabla con box.ROUNDED
                # Mostrar solo el nombre del archivo, no el path completo
                display_name = os.path.basename(self.filename) if self.filename else 'Sin nombre'
                
                # Configurar título según show_title
                display_name = display_name.upper()
                table_title = f"[bold cyan]{display_name}[/bold cyan]" if show_title else None
                
                table = Table(
                    title=table_title,
                    title_justify="left",
                    show_header=True,
                    header_style="bold magenta",
                    border_style="bright_blue",
                    title_style="bold cyan",
                    box=box.ROUNDED
                )
                
                # Definir columnas
                table.add_column("File", style="cyan", no_wrap=True, width=14)
                table.add_column("Size", justify="right", style="green", width=8)
                table.add_column("Load", justify="center", style="yellow", width=10)
                table.add_column("Exec", justify="center", style="yellow", width=10)
                table.add_column("User", justify="center", style="magenta", width=6)
                table.add_column("Type", style="dim", width=12)
                
                # Procesar archivos
                for i, entry in enumerate(entries):
                    if entry.is_deleted or entry.num_page != 0:
                        continue
                    
                    # Calcular tamaño total
                    total_pages = 0
                    p = 0
                    while (i + p) < 64 and entries[i + p].num_page >= p:
                        if entries[i + p].user == entry.user:
                            total_pages += entries[i + p].nb_pages
                        p += 1
                    
                    size_kb = (total_pages + 7) >> 3
                    size_str = f"{size_kb}K"
                    
                    # Leer cabecera AMSDOS
                    load_addr = "-"
                    exec_addr = "-"
                    file_type = "[dim]ASCII[/dim]"
                    
                    if entry.blocks[0] != 0:
                        try:
                            block_data = self.read_block(entry.blocks[0])
                            if self._check_amsdos_header(block_data):
                                load_addr = f"&{struct.unpack('<H', block_data[0x15:0x17])[0]:04X}"
                                exec_addr = f"&{struct.unpack('<H', block_data[0x1A:0x1C])[0]:04X}"
                                
                                ftype = block_data[0x12]
                                if ftype == 0:
                                    file_type = "[cyan]BASIC[/cyan]"
                                elif ftype == 1:
                                    file_type = "[bright_yellow]BASIC+[/bright_yellow]"
                                elif ftype == 2:
                                    file_type = "[blue]BINARY[/blue]"
                                elif ftype == 22:
                                    file_type = "[magenta]SCREEN$[/magenta]"
                                else:
                                    file_type = f"[dim]Type {ftype}[/dim]"
                        except:
                            pass
                    
                    # Estilo según extensión
                    filename = entry.full_name
                    if filename.endswith('.BAS'):
                        filename_style = "[bold cyan]" + filename + "[/bold cyan]"
                    elif filename.endswith('.BIN'):
                        filename_style = "[bold yellow]" + filename + "[/bold yellow]"
                    elif filename.endswith('.BAK'):
                        filename_style = "[dim]" + filename + "[/dim]"
                    else:
                        filename_style = filename
                    
                    table.add_row(
                        filename_style,
                        size_str,
                        load_addr,
                        exec_addr,
                        str(entry.user),
                        file_type
                    )
                
                # Mostrar tabla
                console.print(table)
                
                # Mostrar espacio libre
                free_space = self.get_free_space()
                free_text = f"[bold green]{free_space}K[/bold green] free"
                console.print(Panel(free_text, style="bright_blue", expand=False))
                console.print()
                
                return None  # Rich imprime directamente
                
            except ImportError:
                # Si Rich no está disponible, usar formato tradicional
                pass
        
        if simple:
            return self._list_files_simple(entries)
        else:
            return self._list_files_table(entries)
    
    def _list_files_table(self, entries: List[DirEntry]) -> str:
        """Genera listado en formato tabla profesional"""
        output = []
        
        # Header
        output.append("┌──────────────┬────────┬──────────┬──────────┬────────┐")
        output.append("│     File     │  Size  │   Load   │   Exec   │  User  │")
        output.append("├──────────────┼────────┼──────────┼──────────┼────────┤")
        
        # Procesar archivos
        for i, entry in enumerate(entries):
            # Solo mostrar archivos no borrados y primera página (extent 0)
            if entry.is_deleted or entry.num_page != 0:
                continue
            
            # Calcular tamaño total (sumar todas las páginas/extends)
            total_pages = 0
            p = 0
            while (i + p) < 64 and entries[i + p].num_page >= p:
                if entries[i + p].user == entry.user:
                    total_pages += entries[i + p].nb_pages
                p += 1
            
            # Tamaño en KB
            size_kb = (total_pages + 7) >> 3
            size_str = f"{size_kb}K"
            
            # Intentar leer cabecera AMSDOS
            load_addr = "-"
            exec_addr = "-"
            
            if entry.blocks[0] != 0:
                try:
                    block_data = self.read_block(entry.blocks[0])
                    if self._check_amsdos_header(block_data):
                        load_addr = f"&{struct.unpack('<H', block_data[0x15:0x17])[0]:04X}"
                        exec_addr = f"&{struct.unpack('<H', block_data[0x1A:0x1C])[0]:04X}"
                except:
                    pass
            
            # Formatear línea
            filename = entry.full_name.ljust(12)[:12]
            size_col = size_str.rjust(6)
            load_col = load_addr.center(8)
            exec_col = exec_addr.center(8)
            user_col = str(entry.user).center(6)
            
            output.append(f"│ {filename} │ {size_col} │ {load_col} │ {exec_col} │ {user_col} │")
        
        # Footer con espacio libre
        output.append("├──────────────────────────────────────────────────────┤")
        free_space = self.get_free_space()
        free_text = f"{free_space}K free".center(54)
        output.append(f"│{free_text}│")
        output.append("└──────────────────────────────────────────────────────┘")
        
        return "\n".join(output)
    
    def _list_files_simple(self, entries: List[DirEntry]) -> str:
        """Genera listado en formato simple (columnas)"""
        output = []
        
        # Procesar archivos
        for i, entry in enumerate(entries):
            # Solo mostrar archivos no borrados y primera página
            if entry.is_deleted or entry.num_page != 0:
                continue
            
            # Calcular tamaño total
            total_pages = 0
            p = 0
            while (i + p) < 64 and entries[i + p].num_page >= p:
                if entries[i + p].user == entry.user:
                    total_pages += entries[i + p].nb_pages
                p += 1
            
            # Tamaño en KB
            size_kb = (total_pages + 7) >> 3
            size_str = f"{size_kb}K"
            
            # Intentar leer cabecera AMSDOS
            load_addr = "-"
            exec_addr = "-"
            
            if entry.blocks[0] != 0:
                try:
                    block_data = self.read_block(entry.blocks[0])
                    if self._check_amsdos_header(block_data):
                        load_addr = f"&{struct.unpack('<H', block_data[0x15:0x17])[0]:04X}"
                        exec_addr = f"&{struct.unpack('<H', block_data[0x1A:0x1C])[0]:04X}"
                except:
                    pass
            
            # Formatear línea simple
            filename = entry.full_name.ljust(12)
            line = f"{filename} {size_str:>6}  {load_addr:<8} {exec_addr:<8} User {entry.user}"
            output.append(line)
        
        # Espacio libre
        free_space = self.get_free_space()
        output.append(f"\n{free_space}K free")
        
        return "\n".join(output)
    
    def _check_amsdos_header(self, data: bytes) -> bool:
        """
        Verifica si los datos tienen una cabecera AMSDOS válida
        
        Args:
            data: Primeros bytes del archivo
        
        Returns:
            True si la cabecera es válida
        """
        if len(data) < 128:
            return False
        
        # Calcular checksum
        checksum = sum(data[0:67]) & 0xFFFF
        stored_checksum = struct.unpack('<H', data[0x43:0x45])[0]
        
        return checksum == stored_checksum and checksum != 0
    
    def write_file(self, host_filename: str, dsk_filename: Optional[str] = None,
                   file_type: int = 0, load_addr: int = 0, exec_addr: int = 0,
                   user: int = 0, system: bool = False, read_only: bool = False,
                   force: bool = False) -> None:
        """
        Importa un archivo desde el sistema al DSK
        
        Args:
            host_filename: Ruta del archivo en el sistema host
            dsk_filename: Nombre del archivo en el DSK (si None, usa el nombre del archivo host)
            file_type: Tipo de archivo:
                       0 = BASIC tokenizado (con cabecera AMSDOS)
                       1 = BASIC protegido (con cabecera)
                       2 = Binario (con cabecera AMSDOS)
                       3 = Binario protegido (con cabecera)
                       -1 = RAW (sin cabecera, sin procesamiento)
            load_addr: Dirección de carga (solo para binarios)
            exec_addr: Dirección de ejecución (solo para binarios)
            user: Número de usuario (0-15)
            system: Marcar como archivo de sistema
            read_only: Marcar como solo lectura
            force: Sobrescribir si existe
        
        Raises:
            DSKFileNotFoundError: Si el archivo no existe
            DSKFileExistsError: Si el archivo ya existe en el DSK y force=False
            DSKNoSpaceError: Si no hay espacio suficiente
        """
        # Leer archivo del sistema
        if not os.path.exists(host_filename):
            raise DSKFileNotFoundError(f"Archivo no encontrado: {host_filename}")
        
        with open(host_filename, 'rb') as f:
            file_data = bytearray(f.read())
        
        # Determinar nombre AMSDOS
        if dsk_filename is None:
            dsk_filename = os.path.basename(host_filename)
        
        amsdos_name = self._get_amsdos_filename(dsk_filename)
        
        # Verificar si el archivo ya existe
        entries = self.get_directory_entries()
        for i, entry in enumerate(entries):
            if not entry.is_deleted and entry.full_name == amsdos_name:
                if not force:
                    raise DSKFileExistsError(f"El archivo {amsdos_name} ya existe en el DSK")
                # Eliminar archivo existente
                self._remove_file_by_index(i)
                break
        
        # Procesar archivo según tipo
        has_header = self._check_amsdos_header(file_data)
        
        # Si se especifica load o exec address, forzar modo binario
        if load_addr != 0 or exec_addr != 0:
            file_type = 2  # Binario con cabecera
        
        if file_type == 0 or file_type == 1 or file_type == 2 or file_type == 3:  # Archivos con cabecera AMSDOS
            if not has_header:
                # Crear cabecera AMSDOS
                file_data = self._create_amsdos_header(amsdos_name, file_data, 
                                                       load_addr, exec_addr, file_type)
            else:
                # Actualizar direcciones si se especificaron
                if load_addr != 0:
                    struct.pack_into('<H', file_data, 0x15, load_addr)
                if exec_addr != 0:
                    struct.pack_into('<H', file_data, 0x1A, exec_addr)
                # Recalcular checksum
                checksum = sum(file_data[0:67]) & 0xFFFF
                struct.pack_into('<H', file_data, 0x43, checksum)
        
        # file_type == -1 (RAW) no hace nada, usa los datos tal cual
        
        # Copiar archivo al DSK
        self._copy_file_to_dsk(file_data, amsdos_name, user, system, read_only)
    
    def _get_amsdos_filename(self, filename: str) -> str:
        """
        Convierte un nombre de archivo a formato AMSDOS (8.3)
        
        Args:
            filename: Nombre de archivo original
        
        Returns:
            Nombre en formato AMSDOS (sin espacios padding)
        """
        # Separar nombre y extensión
        name = os.path.splitext(os.path.basename(filename))[0].upper()
        ext = os.path.splitext(filename)[1][1:].upper() if '.' in filename else ''
        
        # Truncar a límites AMSDOS (sin padding)
        name = name[:8]
        ext = ext[:3]
        
        # Retornar sin espacios (el directorio ya tiene el padding)
        return f"{name}.{ext}" if ext else name
    
    def _create_amsdos_header(self, filename: str, data: bytearray,
                             load_addr: int, exec_addr: int, file_type: int) -> bytearray:
        """
        Crea una cabecera AMSDOS para un archivo
        
        Args:
            filename: Nombre del archivo (formato AMSDOS)
            data: Datos del archivo
            load_addr: Dirección de carga
            exec_addr: Dirección de ejecución
            file_type: Tipo de archivo
        
        Returns:
            Datos con cabecera AMSDOS prepended
        """
        header = bytearray(AMSDOS_HEADER_SIZE)
        
        # Separar nombre y extensión
        parts = filename.split('.')
        name = parts[0][:8].ljust(8).encode('ascii')
        ext = parts[1][:3].ljust(3).encode('ascii') if len(parts) > 1 else b'   '
        
        # Tipo de archivo en la cabecera AMSDOS
        # file_type parameter (interno):
        #   0 = BASIC tokenizado    -> byte 0 = 0x00
        #   1 = BASIC protegido     -> byte 0 = 0x00 (protección en dir)
        #   2 = Binario             -> byte 0 = 0x16
        #   3 = Binario protegido   -> byte 0 = 0x16 (protección en dir)
        
        if file_type in (0, 1):  # BASIC (tokenizado o protegido)
            header[0] = 0x00  # Tipo BASIC
        else:  # Binario (tipo 2 o 3)
            header[0] = 0x16  # Tipo binario
        
        # Nombre del archivo (8 bytes)
        header[1:9] = name
        
        # Extensión (3 bytes)
        header[9:12] = ext
        
        # Número de bloque (0x00)
        header[12] = 0x00
        
        # Último bloque (0x00)
        header[13] = 0x00
        
        # Tipo de archivo (repetido)
        header[14] = header[0]
        
        # Tipo de archivo en posición 0x12 (usado por list_files)
        # 0 = BASIC, 1 = BASIC protegido, 2 = Binario, 22 = SCREEN$
        if file_type in (0, 1):
            header[0x12] = file_type  # 0 o 1 para BASIC
        else:
            header[0x12] = 2  # 2 para binario
        
        # Longitud del archivo
        file_length = len(data)
        struct.pack_into('<H', header, 0x18, file_length)
        
        # Dirección de carga
        if load_addr == 0:
            # BASIC (tipo 0 y 1) usa 0x0170, binarios (tipo 2 y 3) usan 0x4000
            load_addr = 0x0170 if file_type in (0, 1) else 0x4000
        struct.pack_into('<H', header, 0x15, load_addr)
        
        # Primera dirección libre (no usada)
        header[0x17] = 0x00
        
        # Dirección de ejecución
        if exec_addr == 0:
            # BASIC tokenizado (tipo 0) usa 0x0000, otros tipos usan load_addr
            if file_type == 0:
                exec_addr = 0x0000
            else:
                exec_addr = load_addr
        struct.pack_into('<H', header, 0x1A, exec_addr)
        
        # Longitud lógica del archivo (igual a la longitud real)
        struct.pack_into('<H', header, 0x40, file_length)
        
        # Calcular checksum (suma de los primeros 67 bytes)
        checksum = sum(header[0:67]) & 0xFFFF
        struct.pack_into('<H', header, 0x43, checksum)
        
        # Prepend header a los datos
        return header + data
    
    def _copy_file_to_dsk(self, file_data: bytearray, filename: str,
                         user: int, system: bool, read_only: bool) -> None:
        """
        Copia datos de archivo al DSK
        
        Args:
            file_data: Datos del archivo (con cabecera si aplica)
            filename: Nombre AMSDOS del archivo
            user: Número de usuario
            system: Marcar como sistema
            read_only: Marcar como solo lectura
        
        Raises:
            DSKNoSpaceError: Si no hay espacio suficiente
        """
        # Calcular bloques necesarios
        file_size = len(file_data)
        blocks_needed = (file_size + 1023) // 1024  # Redondear hacia arriba
        
        # Verificar espacio disponible
        free_blocks = self._count_free_blocks()
        if free_blocks < blocks_needed:
            raise DSKNoSpaceError(f"No hay espacio suficiente ({free_blocks} bloques libres, {blocks_needed} necesarios)")
        
        # Separar nombre y extensión
        parts = filename.split('.')
        name = parts[0][:8].ljust(8)
        ext = parts[1][:3].ljust(3) if len(parts) > 1 else '   '
        
        # Marcar atributos en extensión
        ext_bytes = bytearray(ext.encode('ascii'))
        if read_only:
            ext_bytes[0] |= 0x80
        if system:
            ext_bytes[1] |= 0x80
        
        # Escribir archivo en páginas (cada página = hasta 16KB = 128 records de 128 bytes)
        pos_file = 0
        page_num = 0
        used_blocks = set()  # Tracking de bloques ya asignados en esta operación
        
        while pos_file < file_size:
            # Buscar entrada libre en directorio
            dir_pos = self._find_free_directory_entry()
            if dir_pos == -1:
                raise DSKNoSpaceError("No hay entradas libres en el directorio")
            
            # Calcular tamaño de esta página en records de 128 bytes
            remaining = file_size - pos_file
            records_this_page = (remaining + 127) // 128
            if records_this_page > 128:
                records_this_page = 128
            
            # Calcular bloques para esta página
            blocks_this_page = (records_this_page + 7) // 8
            
            # Asignar bloques
            block_list = []
            for _ in range(blocks_this_page):
                # Buscar bloque libre que no hayamos usado ya
                block_num = self._find_free_block_excluding(used_blocks)
                if block_num == -1:
                    raise DSKNoSpaceError("No hay bloques libres")
                block_list.append(block_num)
                used_blocks.add(block_num)  # Marcar como usado
                
                # Escribir datos en el bloque
                block_data = file_data[pos_file:pos_file + 1024]
                if len(block_data) < 1024:
                    block_data += bytes(1024 - len(block_data))  # Padding
                self._write_block(block_num, block_data)
                pos_file += 1024
            
            # Crear entrada de directorio
            self._write_directory_entry(dir_pos, name, ext_bytes, user, page_num,
                                       records_this_page, block_list)
            
            page_num += 1
    
    def _count_free_blocks(self) -> int:
        """Cuenta bloques libres en el DSK"""
        bitmap = self._create_bitmap()
        return sum(1 for used in bitmap if not used)
    
    def _create_bitmap(self) -> List[bool]:
        """Crea bitmap de bloques usados"""
        # Total de bloques (pistas * 9 sectores / 2 sectores por bloque)
        total_blocks = self.header.nb_tracks * 9 // 2
        bitmap = [False] * total_blocks
        
        # Los primeros bloques están reservados para el directorio
        # Track 0, 1 = directorio (2 pistas = 18 sectores = 9 bloques)
        for i in range(2):
            bitmap[i] = True
        
        # Marcar bloques usados por archivos
        entries = self.get_directory_entries()
        for entry in entries:
            if not entry.is_deleted:
                for block_num in entry.blocks:
                    if block_num < len(bitmap) and block_num > 0:
                        bitmap[block_num] = True
        
        return bitmap
    
    def _find_free_block(self) -> int:
        """Encuentra un bloque libre"""
        bitmap = self._create_bitmap()
        for i, used in enumerate(bitmap):
            if not used:
                return i
        return -1
    
    def _find_free_block_excluding(self, exclude_set: set) -> int:
        """
        Encuentra un bloque libre excluyendo los que están en exclude_set
        
        Args:
            exclude_set: Set de números de bloque a excluir
        
        Returns:
            Número de bloque libre, o -1 si no hay
        """
        bitmap = self._create_bitmap()
        for i, used in enumerate(bitmap):
            if not used and i not in exclude_set:
                return i
        return -1
    
    def _find_free_directory_entry(self) -> int:
        """Encuentra una entrada libre en el directorio"""
        entries = self.get_directory_entries()
        for i, entry in enumerate(entries):
            if entry.user == USER_DELETED:
                return i
        return -1
    
    def _write_block(self, block_num: int, data: bytes) -> None:
        """
        Escribe datos en un bloque (1KB = 2 sectores)
        
        Args:
            block_num: Número de bloque (0-based)
            data: Datos a escribir (1024 bytes)
        """
        # Calcular track y sector (igual que read_block)
        track = (block_num << 1) // 9
        sect = (block_num << 1) % 9
        
        min_sect = self.get_min_sector()
        
        # Ajustar track según el formato
        if min_sect == 0x41:  # SYSTEM
            track += 2
        elif min_sect == 0x01:  # VENDOR
            track += 1
        
        # Escribir primer sector
        pos1 = self._get_sector_position(track, sect + min_sect, physical=True)
        self.data[pos1:pos1 + 512] = data[0:512]
        
        # Escribir segundo sector
        sect += 1
        if sect > 8:
            track += 1
            sect = 0
        
        pos2 = self._get_sector_position(track, sect + min_sect, physical=True)
        self.data[pos2:pos2 + 512] = data[512:1024]
    
    def _write_directory_entry(self, entry_num: int, name: str, ext: bytearray,
                              user: int, page_num: int, nb_records: int,
                              blocks: List[int]) -> None:
        """
        Escribe una entrada en el directorio
        
        Args:
            entry_num: Número de entrada (0-63)
            name: Nombre del archivo (8 chars)
            ext: Extensión con atributos (3 bytes)
            user: Número de usuario
            page_num: Número de página
            nb_records: Número de records de 128 bytes
            blocks: Lista de bloques asignados
        """
        # Calcular posición en el directorio siguiendo la lógica C++
        # NumDir >> 4 = sector dentro del directorio (0-3)
        # NumDir & 15 = entrada dentro del sector (0-15)
        min_sect = self.get_min_sector()
        
        # Sector ID (siguiendo el formato del DSK)
        sector_id = (entry_num >> 4) + min_sect
        
        # Track del directorio
        if min_sect == self.FORMAT_SYSTEM:  # 0x41
            track = 2
        elif min_sect == self.FORMAT_VENDOR:  # 0x01
            track = 1
        else:  # FORMAT_DATA 0xC1
            track = 0
        
        # Entrada dentro del sector (0-15)
        entry_in_sector = entry_num & 15
        
        # Obtener posición física del sector usando el ID físico
        pos = self._get_sector_position(track, sector_id, physical=True)
        pos += entry_in_sector * 32  # Cada entrada son 32 bytes
        
        # Construir entrada
        entry = bytearray(32)
        entry[0] = user  # User number
        entry[1:9] = name.encode('ascii')  # Nombre
        entry[9:12] = ext  # Extensión con atributos
        entry[12] = page_num  # Número de página (extent)
        entry[13] = 0  # Reservado
        entry[14] = 0  # Extent high
        entry[15] = nb_records  # Número de records de 128 bytes
        
        # Bloques (16 bytes)
        for i, block_num in enumerate(blocks):
            if i < 16:
                entry[16 + i] = block_num
        
        # Escribir entrada
        self.data[pos:pos + 32] = entry
    
    def _remove_file_by_index(self, index: int) -> None:
        """
        Elimina un archivo por su índice en el directorio
        
        Args:
            index: Índice de la entrada (0-63)
        """
        entries = self.get_directory_entries()
        entry = entries[index]
        
        # Marcar todas las páginas del archivo como borradas
        for i in range(64):
            e = entries[i]
            if not e.is_deleted and e.full_name == entry.full_name and e.user == entry.user:
                # Marcar como borrado (user = 0xE5)
                min_sect = self.get_min_sector()
                
                # Determinar track inicial según formato
                if min_sect == 0x41:  # SYSTEM
                    track = 2
                elif min_sect == 0x01:  # VENDOR
                    track = 1
                else:  # DATA
                    track = 0
                
                # Calcular sector y posición dentro del sector
                sector = (i >> 4) + min_sect  # Cada 16 entradas cambia de sector
                entry_in_sector = i & 15       # Posición dentro del sector (0-15)
                
                # Obtener posición del sector
                pos = self._get_sector_position(track, sector, physical=True)
                
                # Cada entrada ocupa 32 bytes
                entry_pos = pos + (entry_in_sector << 5)
                
                # Marcar como eliminada (byte 0 = 0xE5)
                self.data[entry_pos] = USER_DELETED
    
    def read_file(self, dsk_filename: str, user: int = 0, 
                  keep_header: bool = True) -> Optional[bytes]:
        """
        Lee un archivo del DSK
        
        Args:
            dsk_filename: Nombre del archivo en el DSK
            user: Número de usuario (0-15)
            keep_header: Si True, mantiene la cabecera AMSDOS; si False, la quita
        
        Returns:
            Bytes del archivo, o None si no se encuentra
        
        Raises:
            DSKFileNotFoundError: Si el archivo no existe
        """
        # Normalizar nombre AMSDOS
        amsdos_name = self._get_amsdos_filename(dsk_filename)
        
        # Buscar archivo
        entries = self.get_directory_entries()
        file_entry_index = -1
        
        for i, entry in enumerate(entries):
            if (not entry.is_deleted and 
                entry.full_name == amsdos_name and 
                entry.user == user and
                entry.num_page == 0):  # Primera página
                file_entry_index = i
                break
        
        if file_entry_index == -1:
            raise DSKFileNotFoundError(f"Archivo {dsk_filename} no encontrado (usuario {user})")
        
        # Leer todas las páginas del archivo
        file_data = bytearray()
        current_entry = entries[file_entry_index]
        current_name = current_entry.full_name
        i = file_entry_index
        
        # Iterar por todas las páginas (extents) del archivo
        while i < 64:
            entry = entries[i]
            
            # Verificar si es la misma archivo
            if (entry.is_deleted or 
                entry.full_name != current_name or 
                entry.user != user):
                break
            
            # Leer bloques de esta página
            num_blocks = (entry.nb_pages + 7) >> 3  # Bloques = páginas / 8 (redondeado)
            
            for j in range(num_blocks):
                block_num = entry.blocks[j]
                if block_num > 0:
                    block_data = self.read_block(block_num)
                    file_data.extend(block_data)
            
            i += 1
        
        # Procesar cabecera AMSDOS si existe
        if not keep_header and len(file_data) >= AMSDOS_HEADER_SIZE:
            if self._check_amsdos_header(file_data):
                # Obtener tamaño real del archivo desde la cabecera
                file_length = struct.unpack('<H', file_data[0x18:0x1A])[0]
                # Retornar solo los datos sin cabecera
                return bytes(file_data[AMSDOS_HEADER_SIZE:AMSDOS_HEADER_SIZE + file_length])
        
        return bytes(file_data)
    
    def export_file(self, dsk_filename: str, host_filename: str, 
                   user: int = 0, keep_header: bool = True) -> None:
        """
        Exporta un archivo del DSK al sistema de archivos
        
        Args:
            dsk_filename: Nombre del archivo en el DSK
            host_filename: Ruta donde guardar el archivo
            user: Número de usuario (0-15)
            keep_header: Si True, mantiene cabecera AMSDOS; si False, la quita
        
        Raises:
            DSKFileNotFoundError: Si el archivo no existe
        """
        # Leer archivo
        file_data = self.read_file(dsk_filename, user, keep_header)
        
        # Guardar en el sistema
        with open(host_filename, 'wb') as f:
            f.write(file_data)
    
    def export_all(self, output_dir: str, keep_header: bool = True) -> List[str]:
        """
        Exporta todos los archivos del DSK a un directorio
        
        Args:
            output_dir: Directorio donde guardar los archivos
            keep_header: Si True, mantiene cabeceras AMSDOS
        
        Returns:
            Lista de archivos exportados
        """
        import os
        
        # Crear directorio si no existe
        os.makedirs(output_dir, exist_ok=True)
        
        exported = []
        entries = self.get_directory_entries()
        
        # Exportar solo la primera página de cada archivo
        for i, entry in enumerate(entries):
            if not entry.is_deleted and entry.num_page == 0:
                try:
                    # Nombre de salida
                    filename = entry.full_name.replace(' ', '').strip()
                    output_path = os.path.join(output_dir, filename)
                    
                    # Exportar
                    self.export_file(entry.full_name, output_path, entry.user, keep_header)
                    exported.append(filename)
                except Exception as e:
                    print(f"⚠️  Error exportando {entry.full_name}: {e}")
        
        return exported
    
    def rename_file(self, old_name: str, new_name: str, user: int = 0) -> None:
        """
        Renombra un archivo en el DSK.
        
        Args:
            old_name: Nombre actual del archivo
            new_name: Nuevo nombre para el archivo
            user: Área de usuario (0-15, default: 0)
            
        Raises:
            DSKFileNotFoundError: Si el archivo no existe
            DSKFileExistsError: Si el nuevo nombre ya existe
            DSKError: Si el nuevo nombre no es válido
        """
        if not self.header:
            raise DSKError("DSK no cargado")
        
        # Buscar archivo actual
        old_name_amsdos = old_name.upper()
        new_name_amsdos = new_name.upper()
        
        # Obtener entradas del directorio
        entries = self.get_directory_entries()
        
        # Validar que el archivo actual existe
        first_entry_idx = None
        for idx, entry in enumerate(entries):
            if entry.user == user and not entry.is_deleted:
                filename = entry.full_name.replace(' ', '').strip()
                if filename == old_name_amsdos:
                    first_entry_idx = idx
                    break
        
        if first_entry_idx is None:
            raise DSKFileNotFoundError(f"Archivo {old_name} no encontrado (usuario {user})")
        
        # Validar que el nuevo nombre no existe
        for entry in entries:
            if entry.user == user and not entry.is_deleted:
                filename = entry.full_name.replace(' ', '').strip()
                if filename == new_name_amsdos:
                    raise DSKFileExistsError(f"Ya existe un archivo llamado {new_name}")
        
        # Parsear nuevo nombre (formato 8.3)
        new_name_parts = new_name_amsdos.split('.')
        if len(new_name_parts) == 1:
            new_filename = new_name_parts[0][:8].ljust(8).encode('ascii')
            new_extension = b'   '
        elif len(new_name_parts) == 2:
            new_filename = new_name_parts[0][:8].ljust(8).encode('ascii')
            new_extension = new_name_parts[1][:3].ljust(3).encode('ascii')
        else:
            raise DSKError(f"Nombre de archivo inválido: {new_name}")
        
        # Guardar nombre/extensión original para comparar
        old_name_stored = entries[first_entry_idx].name
        old_ext_stored = entries[first_entry_idx].ext
        
        # Actualizar todas las entradas del archivo (múltiples extents)
        for idx, entry in enumerate(entries):
            # Verificar si es la misma entrada (mismo nombre, extensión y usuario)
            if (entry.user == user and 
                entry.name == old_name_stored and 
                entry.ext == old_ext_stored and
                not entry.is_deleted):
                
                # Actualizar directamente en la estructura de datos del DSK
                self._update_directory_entry_name(idx, new_filename, new_extension)
    
    def _update_directory_entry_name(self, entry_num: int, filename: bytes, extension: bytes) -> None:
        """
        Actualiza el nombre y extensión de una entrada de directorio.
        
        Args:
            entry_num: Número de entrada (0-63)
            filename: Nuevo nombre (8 bytes)
            extension: Nueva extensión (3 bytes)
        """
        min_sect = self.get_min_sector()
        
        # Determinar track inicial según formato
        if min_sect == 0x41:  # SYSTEM
            track = 2
        elif min_sect == 0x01:  # VENDOR
            track = 1
        else:  # DATA
            track = 0
        
        # Calcular sector y posición dentro del sector
        sector = (entry_num >> 4) + min_sect  # Cada 16 entradas cambia de sector
        entry_in_sector = entry_num & 15       # Posición dentro del sector (0-15)
        
        # Obtener posición del sector
        pos = self._get_sector_position(track, sector, physical=True)
        
        # Cada entrada ocupa 32 bytes
        entry_pos = pos + (entry_in_sector << 5)
        
        # Actualizar nombre (bytes 1-8)
        self.data[entry_pos + 1:entry_pos + 9] = filename
        
        # Actualizar extensión (bytes 9-11)
        self.data[entry_pos + 9:entry_pos + 12] = extension
    
    def delete_file(self, filename: str, user: int = 0) -> int:
        """
        Elimina un archivo del DSK marcando sus entradas como borradas.
        
        Args:
            filename: Nombre del archivo a eliminar
            user: Área de usuario (0-15, default: 0)
            
        Returns:
            Número de extents eliminados
            
        Raises:
            DSKFileNotFoundError: Si el archivo no existe
        """
        if not self.header:
            raise DSKError("DSK no cargado")
        
        # Buscar archivo
        filename_amsdos = filename.upper()
        
        # Obtener entradas del directorio
        entries = self.get_directory_entries()
        
        # Validar que el archivo existe
        first_entry_idx = None
        for idx, entry in enumerate(entries):
            if entry.user == user and not entry.is_deleted:
                file_in_dir = entry.full_name.replace(' ', '').strip()
                if file_in_dir == filename_amsdos:
                    first_entry_idx = idx
                    break
        
        if first_entry_idx is None:
            raise DSKFileNotFoundError(f"Archivo {filename} no encontrado (usuario {user})")
        
        # Guardar nombre/extensión para comparar
        target_name = entries[first_entry_idx].name
        target_ext = entries[first_entry_idx].ext
        
        # Marcar como eliminadas todas las entradas del archivo (múltiples extents)
        deleted_count = 0
        for idx, entry in enumerate(entries):
            # Verificar si es la misma entrada (mismo nombre, extensión y usuario)
            if (entry.user == user and 
                entry.name == target_name and 
                entry.ext == target_ext and
                not entry.is_deleted):
                
                # Marcar como eliminada (user = 0xE5)
                self._mark_entry_as_deleted(idx)
                deleted_count += 1
        
        return deleted_count
    
    def _mark_entry_as_deleted(self, entry_num: int) -> None:
        """
        Marca una entrada de directorio como eliminada.
        
        Args:
            entry_num: Número de entrada (0-63)
        """
        min_sect = self.get_min_sector()
        
        # Determinar track inicial según formato
        if min_sect == 0x41:  # SYSTEM
            track = 2
        elif min_sect == 0x01:  # VENDOR
            track = 1
        else:  # DATA
            track = 0
        
        # Calcular sector y posición dentro del sector
        sector = (entry_num >> 4) + min_sect  # Cada 16 entradas cambia de sector
        entry_in_sector = entry_num & 15       # Posición dentro del sector (0-15)
        
        # Obtener posición del sector
        pos = self._get_sector_position(track, sector, physical=True)
        
        # Cada entrada ocupa 32 bytes
        entry_pos = pos + (entry_in_sector << 5)
        
        # Marcar como eliminada (byte 0 = 0xE5)
        self.data[entry_pos] = USER_DELETED
    
    def __repr__(self) -> str:
        """Representación string del objeto DSK"""
        if not self.header:
            return "DSK(sin datos)"
        
        info = self.get_info()
        return (f"DSK(filename='{info['filename']}', "
                f"format={info['format']}, "
                f"tracks={info['tracks']}, "
                f"capacity={info['capacity_kb']}KB)")
    
    @staticmethod
    def add_amsdos_header(input_file: str, output_file: str,
                         load_addr: int = 0, exec_addr: int = 0,
                         file_type: int = 0, force: bool = False) -> None:
        """
        Añade una cabecera AMSDOS a un archivo externo (fuera del DSK)
        
        Args:
            input_file: Ruta del archivo de entrada (sin cabecera)
            output_file: Ruta del archivo de salida (con cabecera)
            load_addr: Dirección de carga (0 = auto: 0x0170 para BASIC, 0x4000 para binario)
            exec_addr: Dirección de ejecución (0 = igual que load_addr)
            file_type: Tipo de archivo (0=binario, 1=BASIC protegido, 2=BASIC ASCII, 3=binario protegido)
            force: Si True, sobrescribe el archivo de salida si existe
        
        Raises:
            FileNotFoundError: Si el archivo de entrada no existe
            FileExistsError: Si el archivo de salida existe y force=False
            DSKError: Si el archivo ya tiene cabecera AMSDOS
        """
        import os
        from pathlib import Path
        
        # Verificar que el archivo de entrada existe
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Archivo de entrada no encontrado: {input_file}")
        
        # Verificar si el archivo de salida existe
        if os.path.exists(output_file) and not force:
            raise FileExistsError(f"El archivo de salida ya existe: {output_file}. Usa force=True para sobrescribir")
        
        # Leer archivo de entrada
        with open(input_file, 'rb') as f:
            file_data = bytearray(f.read())
        
        # Verificar que no tenga ya cabecera AMSDOS
        if len(file_data) >= AMSDOS_HEADER_SIZE:
            # Comprobar checksum
            if file_data[0] in (0x00, 0x16):  # Tipos válidos
                checksum_stored = struct.unpack('<H', file_data[0x43:0x45])[0]
                checksum_calc = sum(file_data[0:67]) & 0xFFFF
                if checksum_stored == checksum_calc:
                    raise DSKError("El archivo ya tiene una cabecera AMSDOS válida")
        
        # Obtener nombre del archivo sin ruta
        filename = Path(input_file).stem[:8] + Path(input_file).suffix[:4]
        
        # Crear instancia temporal de DSK solo para usar _create_amsdos_header
        temp_dsk = DSK()
        
        # Crear cabecera AMSDOS
        file_with_header = temp_dsk._create_amsdos_header(
            filename, file_data, load_addr, exec_addr, file_type
        )
        
        # Guardar archivo con cabecera
        with open(output_file, 'wb') as f:
            f.write(file_with_header)
    
    @staticmethod
    def remove_amsdos_header(input_file: str, output_file: str, force: bool = False) -> None:
        """
        Elimina la cabecera AMSDOS de un archivo externo (fuera del DSK)
        
        Args:
            input_file: Ruta del archivo de entrada (con cabecera)
            output_file: Ruta del archivo de salida (sin cabecera)
            force: Si True, sobrescribe el archivo de salida si existe
        
        Raises:
            FileNotFoundError: Si el archivo de entrada no existe
            FileExistsError: Si el archivo de salida existe y force=False
            DSKError: Si el archivo no tiene cabecera AMSDOS
        """
        import os
        
        # Verificar que el archivo de entrada existe
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Archivo de entrada no encontrado: {input_file}")
        
        # Verificar si el archivo de salida existe
        if os.path.exists(output_file) and not force:
            raise FileExistsError(f"El archivo de salida ya existe: {output_file}. Usa force=True para sobrescribir")
        
        # Leer archivo de entrada
        with open(input_file, 'rb') as f:
            file_data = f.read()
        
        # Verificar que tenga cabecera AMSDOS
        if len(file_data) < AMSDOS_HEADER_SIZE:
            raise DSKError("El archivo es demasiado pequeño para tener cabecera AMSDOS")
        
        # Verificar checksum
        if file_data[0] not in (0x00, 0x16):
            raise DSKError("El archivo no tiene una cabecera AMSDOS válida (tipo incorrecto)")
        
        checksum_stored = struct.unpack('<H', file_data[0x43:0x45])[0]
        checksum_calc = sum(file_data[0:67]) & 0xFFFF
        
        if checksum_stored != checksum_calc:
            raise DSKError("El archivo no tiene una cabecera AMSDOS válida (checksum incorrecto)")
        
        # Obtener tamaño real del archivo desde la cabecera
        file_length = struct.unpack('<H', file_data[0x18:0x1A])[0]
        
        # Extraer datos sin cabecera
        file_data_no_header = file_data[AMSDOS_HEADER_SIZE:AMSDOS_HEADER_SIZE + file_length]
        
        # Guardar archivo sin cabecera
        with open(output_file, 'wb') as f:
            f.write(file_data_no_header)
