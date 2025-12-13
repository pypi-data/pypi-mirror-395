#!/usr/bin/env python3
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
Ejemplo 2: Listar archivos de imágenes DSK
===========================================


Este ejemplo muestra cómo listar el contenido de imágenes DSK,
obtener información de archivos, y trabajar con el directorio AMSDOS.
"""

import sys
from pathlib import Path

# Añadir PyDSK al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pydsk import DSK, DSKError


def ejemplo_listado_basico():
    """Listar archivos en formato tabla (con Rich si está disponible)"""
    print("=" * 70)
    print("EJEMPLO 1: Listado básico (formato tabla con Rich)")
    print("=" * 70)
    
    # Buscar un DSK de ejemplo
    dsk_file = "../../demo_8bp_v41_004.dsk"
    
    if not Path(dsk_file).exists():
        print("\n⚠️  DSK de ejemplo no encontrado")
        print(f"   Buscando: {dsk_file}")
        print("   Por favor, ejecuta desde la carpeta correcta")
        return
    
    # Cargar DSK
    dsk = DSK(dsk_file)
    
    # Listar en formato tabla con Rich (si está disponible)
    print(f"\nContenido de: {dsk_file}")
    print()
    # use_rich=True es el comportamiento por defecto
    # Si Rich está instalado, muestra tabla con bordes redondeados y colores
    # Si no, usa formato ASCII tradicional
    dsk.list_files(simple=False, use_rich=True)
    print()


def ejemplo_listado_simple():
    """Listar archivos en formato simple (columnas)"""
    print("=" * 70)
    print("EJEMPLO 2: Listado simple (formato columnas)")
    print("=" * 70)
    
    dsk_file = "../../demo_8bp_v41_004.dsk"
    
    if not Path(dsk_file).exists():
        print("\n⚠️  DSK de ejemplo no encontrado")
        return
    
    dsk = DSK(dsk_file)
    
    print(f"\nContenido de: {dsk_file}")
    print()
    # El formato simple no usa Rich, siempre imprime columnas
    print(dsk.list_files(simple=True))
    print()


def ejemplo_listado_tradicional():
    """Listar archivos en formato ASCII tradicional (sin Rich)"""
    print("=" * 70)
    print("EJEMPLO 2b: Listado tradicional (sin Rich)")
    print("=" * 70)
    
    dsk_file = "../../demo_8bp_v41_004.dsk"
    
    if not Path(dsk_file).exists():
        print("\n⚠️  DSK de ejemplo no encontrado")
        return
    
    dsk = DSK(dsk_file)
    
    print(f"\nContenido de: {dsk_file}")
    print()
    # use_rich=False fuerza el formato ASCII tradicional
    # Útil si quieres consistencia o Rich no está disponible
    resultado = dsk.list_files(simple=False, use_rich=False)
    print(resultado)
    print()


def ejemplo_filtrar_archivos():
    """Filtrar archivos por extensión o usuario"""
    print("=" * 70)
    print("EJEMPLO 3: Filtrar archivos del directorio")
    print("=" * 70)
    
    dsk_file = "../../demo_8bp_v41_004.dsk"
    
    if not Path(dsk_file).exists():
        print("\n⚠️  DSK de ejemplo no encontrado")
        return
    
    dsk = DSK(dsk_file)
    entries = dsk.get_directory_entries()
    
    print(f"\nAnalizando: {dsk_file}")
    print()
    
    # Filtrar archivos BASIC
    print("Archivos BASIC (.BAS):")
    basic_files = [e for e in entries if not e.is_deleted and e.ext == "BAS"]
    for entry in basic_files:
        print(f"   - {entry.full_name:15s} (User {entry.user})")
    
    print()
    
    # Filtrar archivos binarios
    print("Archivos binarios (.BIN):")
    bin_files = [e for e in entries if not e.is_deleted and e.ext == "BIN"]
    for entry in bin_files:
        print(f"   - {entry.full_name:15s} (User {entry.user})")
    
    print()
    
    # Filtrar por usuario
    print("Archivos del usuario 10:")
    user10_files = [e for e in entries if not e.is_deleted and e.user == 10]
    for entry in user10_files:
        print(f"   - {entry.full_name:15s} (.{entry.ext})")
    
    print()


def ejemplo_estadisticas():
    """Mostrar estadísticas del DSK"""
    print("=" * 70)
    print("EJEMPLO 4: Estadísticas del DSK")
    print("=" * 70)
    
    dsk_file = "../../demo_8bp_v41_004.dsk"
    
    if not Path(dsk_file).exists():
        print("\n⚠️  DSK de ejemplo no encontrado")
        return
    
    dsk = DSK(dsk_file)
    entries = dsk.get_directory_entries()
    info = dsk.get_info()
    
    # Contar archivos activos
    archivos_activos = [e for e in entries if not e.is_deleted and e.num_page == 0]
    archivos_borrados = [e for e in entries if e.is_deleted]
    
    # Contar por extensión
    extensiones = {}
    for entry in archivos_activos:
        ext = entry.ext
        extensiones[ext] = extensiones.get(ext, 0) + 1
    
    # Mostrar estadísticas
    print(f"\nEstadísticas de: {dsk_file}")
    print("=" * 70)
    print(f"Formato:           {info['format']}")
    print(f"Pistas:            {info['tracks']}")
    print(f"Capacidad total:   {info['capacity_kb']} KB")
    print(f"Espacio usado:     {info['capacity_kb'] - dsk.get_free_space()} KB")
    print(f"Espacio libre:     {dsk.get_free_space()} KB")
    print()
    print(f"Archivos activos:  {len(archivos_activos)}")
    print(f"Archivos borrados: {len(archivos_borrados)}")
    print()
    print("Archivos por tipo:")
    for ext, count in sorted(extensiones.items()):
        print(f"   .{ext:3s} -> {count:2d} archivo(s)")
    print()


def ejemplo_detalles_archivo():
    """Mostrar detalles de archivos específicos"""
    print("=" * 70)
    print("EJEMPLO 5: Detalles de archivos individuales")
    print("=" * 70)
    
    dsk_file = "../../demo_8bp_v41_004.dsk"
    
    if not Path(dsk_file).exists():
        print("\n⚠️  DSK de ejemplo no encontrado")
        return
    
    dsk = DSK(dsk_file)
    entries = dsk.get_directory_entries()
    
    print(f"\nArchivos en: {dsk_file}")
    print()
    
    # Mostrar primeros 5 archivos con detalles
    archivos = [e for e in entries if not e.is_deleted and e.num_page == 0][:5]
    
    for entry in archivos:
        print(f"Archivo: {entry.full_name}")
        print(f"   Usuario:  {entry.user}")
        print(f"   Nombre:   {entry.name}")
        print(f"   Ext:      {entry.ext}")
        print(f"   Páginas:  {entry.nb_pages}")
        print(f"   Bloques:  {[b for b in entry.blocks[:4] if b != 0]}")
        
        # Intentar leer cabecera AMSDOS
        if entry.blocks[0] != 0:
            try:
                block = dsk.read_block(entry.blocks[0])
                if dsk._check_amsdos_header(block):
                    import struct
                    load_addr = struct.unpack('<H', block[0x15:0x17])[0]
                    exec_addr = struct.unpack('<H', block[0x1A:0x1C])[0]
                    print(f"   Load:     &{load_addr:04X}")
                    print(f"   Exec:     &{exec_addr:04X}")
            except:
                pass
        
        print()


def ejemplo_comparar_dsk():
    """Comparar contenido de múltiples DSK"""
    print("=" * 70)
    print("EJEMPLO 6: Comparar múltiples DSK")
    print("=" * 70)
    
    # Crear dos DSK de prueba si no existen
    dsk_files = []
    
    # Buscar DSK existente
    if Path("../../demo_8bp_v41_004.dsk").exists():
        dsk_files.append("../../demo_8bp_v41_004.dsk")
    
    # Crear uno vacío para comparar
    print("\nCreando DSK de prueba vacío...")
    dsk_vacio = DSK()
    dsk_vacio.create(nb_tracks=40, nb_sectors=9)
    dsk_vacio.save("dsk_vacio_temp.dsk")
    dsk_files.append("dsk_vacio_temp.dsk")
    
    if len(dsk_files) < 2:
        print("⚠️  No hay suficientes DSK para comparar")
        return
    
    print(f"\nComparando {len(dsk_files)} DSK:")
    print()
    
    for dsk_file in dsk_files:
        try:
            dsk = DSK(dsk_file)
            entries = dsk.get_directory_entries()
            archivos = [e for e in entries if not e.is_deleted and e.num_page == 0]
            info = dsk.get_info()
            
            print(f"{dsk_file}")
            print(f"   Formato:    {info['format']}")
            print(f"   Archivos:   {len(archivos)}")
            print(f"   Libre:      {dsk.get_free_space()} KB")
            print()
        except DSKError as e:
            print(f"   Error: {e}")
            print()
    
    # Limpiar archivo temporal
    Path("dsk_vacio_temp.dsk").unlink(missing_ok=True)


def main():
    """Ejecutar todos los ejemplos"""
    print("\n" + "=" * 70)
    print(" PyDSK - Ejemplos de listado de archivos")
    print("=" * 70 + "\n")
    
    # Ejecutar ejemplos
    ejemplo_listado_basico()
    ejemplo_listado_simple()
    ejemplo_listado_tradicional()
    ejemplo_filtrar_archivos()
    ejemplo_estadisticas()
    ejemplo_detalles_archivo()
    ejemplo_comparar_dsk()
    
    print("=" * 70)
    print("Todos los ejemplos completados")
    print("=" * 70)
    print()


if __name__ == '__main__':
    main()
