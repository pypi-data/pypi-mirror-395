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
Ejemplo 3: Obtener información detallada de DSK
================================================

Este ejemplo muestra cómo obtener y mostrar información técnica
de imágenes DSK.
"""

import sys
from pathlib import Path

# Añadir PyDSK al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pydsk import DSK, DSKError


def ejemplo_info_basica():
    """Obtener información básica del DSK"""
    print("=" * 70)
    print("EJEMPLO 1: Información básica")
    print("=" * 70)
    
    dsk_file = "../../demo_8bp_v41_004.dsk"
    
    if not Path(dsk_file).exists():
        print("\n⚠️  DSK de ejemplo no encontrado")
        return
    
    dsk = DSK(dsk_file)
    info = dsk.get_info()
    
    print(f"\n📀 Información de: {dsk_file}")
    print("=" * 70)
    for key, value in info.items():
        print(f"{key:15s}: {value}")
    print()


def ejemplo_info_formato():
    """Analizar formato y estructura del DSK"""
    print("=" * 70)
    print("EJEMPLO 2: Información de formato")
    print("=" * 70)
    
    dsk_file = "../../demo_8bp_v41_004.dsk"
    
    if not Path(dsk_file).exists():
        print("\n⚠️  DSK de ejemplo no encontrado")
        return
    
    dsk = DSK(dsk_file)
    
    formato = dsk.get_format_type()
    min_sector = dsk.get_min_sector()
    
    # Descripción del formato
    formato_desc = {
        'DATA': 'Formato estándar para datos (sectores desde 0xC1)',
        'SYSTEM': 'Formato sistema con pistas reservadas (sectores desde 0x41)',
        'VENDOR': 'Formato de fabricante (sectores desde 0x01)',
        'UNKNOWN': 'Formato desconocido'
    }
    
    print(f"\n📊 Análisis de formato:")
    print("=" * 70)
    print(f"Tipo de formato:    {formato}")
    print(f"Descripción:        {formato_desc.get(formato, 'N/A')}")
    print(f"Primer sector ID:   0x{min_sector:02X}")
    print(f"Representación:     {dsk}")
    print()


def ejemplo_analisis_completo():
    """Análisis completo de la estructura del DSK"""
    print("=" * 70)
    print("EJEMPLO 3: Análisis completo de estructura")
    print("=" * 70)
    
    dsk_file = "../../demo_8bp_v41_004.dsk"
    
    if not Path(dsk_file).exists():
        print("\n⚠️  DSK de ejemplo no encontrado")
        return
    
    dsk = DSK(dsk_file)
    info = dsk.get_info()
    entries = dsk.get_directory_entries()
    
    # Calcular estadísticas
    archivos_activos = [e for e in entries if not e.is_deleted and e.num_page == 0]
    archivos_borrados = [e for e in entries if e.is_deleted]
    
    # Bloques usados
    bloques_usados = set()
    for entry in entries:
        if not entry.is_deleted:
            for block in entry.blocks:
                if block != 0:
                    bloques_usados.add(block)
    
    espacio_usado = len(bloques_usados)
    espacio_libre = dsk.get_free_space()
    porcentaje_usado = (espacio_usado / (espacio_usado + espacio_libre)) * 100 if (espacio_usado + espacio_libre) > 0 else 0
    
    print(f"\n📊 Análisis completo: {dsk_file}")
    print("=" * 70)
    print()
    print("ESTRUCTURA FÍSICA:")
    print(f"  Pistas:                {info['tracks']}")
    print(f"  Caras:                 {info['heads']}")
    print(f"  Tamaño por pista:      {info['track_size']:,} bytes")
    print(f"  Tamaño total archivo:  {info['total_size']:,} bytes")
    print()
    print("FORMATO:")
    print(f"  Tipo:                  {info['format']}")
    print(f"  Primer sector:         0x{dsk.get_min_sector():02X}")
    print()
    print("CAPACIDAD:")
    print(f"  Capacidad total:       {info['capacity_kb']} KB")
    print(f"  Espacio usado:         {espacio_usado} KB ({porcentaje_usado:.1f}%)")
    print(f"  Espacio libre:         {espacio_libre} KB ({100-porcentaje_usado:.1f}%)")
    print()
    print("DIRECTORIO:")
    print(f"  Entradas totales:      64")
    print(f"  Archivos activos:      {len(archivos_activos)}")
    print(f"  Archivos borrados:     {len(archivos_borrados)}")
    print(f"  Entradas libres:       {64 - len(archivos_activos) - len(archivos_borrados)}")
    print()
    print("BLOQUES:")
    print(f"  Bloques usados:        {len(bloques_usados)}")
    print(f"  Primeros bloques:      {sorted(list(bloques_usados))[:10]}")
    print()


def ejemplo_multiple_dsk():
    """Analizar múltiples DSK y crear tabla comparativa"""
    print("=" * 70)
    print("EJEMPLO 4: Comparación de múltiples DSK")
    print("=" * 70)
    
    # Lista de DSK a analizar
    dsk_files = []
    
    # Buscar DSK existente
    if Path("../../demo_8bp_v41_004.dsk").exists():
        dsk_files.append("../../demo_8bp_v41_004.dsk")
    
    # Crear algunos de prueba
    print("\n📝 Creando DSK de prueba...")
    
    test_dsks = [
        ("test_35.dsk", 35, DSK.FORMAT_DATA),
        ("test_40.dsk", 40, DSK.FORMAT_DATA),
        ("test_42.dsk", 42, DSK.FORMAT_SYSTEM),
    ]
    
    for filename, tracks, fmt in test_dsks:
        dsk = DSK()
        dsk.create(nb_tracks=tracks, nb_sectors=9, format_type=fmt)
        dsk.save(filename)
        dsk_files.append(filename)
    
    # Tabla comparativa
    print(f"\n📊 Comparación de {len(dsk_files)} imágenes DSK:")
    print()
    print("┌─────────────────────────┬────────┬────────┬──────────┬───────────┐")
    print("│         Archivo         │ Pistas │ Format │ Archivos │   Libre   │")
    print("├─────────────────────────┼────────┼────────┼──────────┼───────────┤")
    
    for dsk_file in dsk_files:
        try:
            dsk = DSK(dsk_file)
            info = dsk.get_info()
            entries = dsk.get_directory_entries()
            archivos = [e for e in entries if not e.is_deleted and e.num_page == 0]
            
            filename_short = Path(dsk_file).name[:23]
            pistas = str(info['tracks'])
            formato = info['format'][:6]
            num_arch = str(len(archivos))
            libre = f"{dsk.get_free_space()} KB"
            
            print(f"│ {filename_short:23s} │ {pistas:>6s} │ {formato:6s} │ {num_arch:>8s} │ {libre:>9s} │")
        except Exception as e:
            print(f"│ {Path(dsk_file).name:23s} │   ERROR reading file: {str(e)[:30]:30s} │")
    
    print("└─────────────────────────┴────────┴────────┴──────────┴───────────┘")
    print()
    
    # Limpiar archivos de prueba
    for filename, _, _ in test_dsks:
        Path(filename).unlink(missing_ok=True)


def main():
    """Ejecutar todos los ejemplos"""
    print("\n" + "=" * 70)
    print(" PyDSK - Ejemplos de información de DSK")
    print("=" * 70 + "\n")
    
    ejemplo_info_basica()
    ejemplo_info_formato()
    ejemplo_analisis_completo()
    ejemplo_multiple_dsk()
    
    print("=" * 70)
    print("✅ Todos los ejemplos completados")
    print("=" * 70)
    print()


if __name__ == '__main__':
    main()
