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
Ejemplo 1: Crear nuevas imágenes DSK
=====================================

Este ejemplo muestra cómo crear imágenes DSK con diferentes configuraciones
usando la librería PyDSK.
"""

import sys
from pathlib import Path

# Añadir PyDSK al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pydsk import DSK


def ejemplo_basico():
    """Crear un DSK con configuración por defecto"""
    print("=" * 70)
    print("EJEMPLO 1: Crear DSK básico (40 pistas, 9 sectores, formato DATA)")
    print("=" * 70)
    
    # Crear instancia de DSK
    dsk = DSK()
    
    # Crear con configuración por defecto
    dsk.create(
        nb_tracks=40,              # 40 pistas
        nb_sectors=9,              # 9 sectores por pista
        format_type=DSK.FORMAT_DATA  # Formato DATA (0xC1)
    )
    
    # Guardar
    dsk.save("mi_primer_disco.dsk")
    
    # Mostrar información
    info = dsk.get_info()
    print(f"\n✅ DSK creado exitosamente!")
    print(f"   Archivo: mi_primer_disco.dsk")
    print(f"   Formato: {info['format']}")
    print(f"   Capacidad: {info['capacity_kb']} KB")
    print(f"   Espacio libre: {dsk.get_free_space()} KB")
    print()


def ejemplo_formato_system():
    """Crear un DSK con formato SYSTEM"""
    print("=" * 70)
    print("EJEMPLO 2: Crear DSK formato SYSTEM (para discos de arranque)")
    print("=" * 70)
    
    dsk = DSK()
    
    # Formato SYSTEM reserva las primeras 2 pistas para el sistema
    dsk.create(
        nb_tracks=40,
        nb_sectors=9,
        format_type=DSK.FORMAT_SYSTEM  # Formato SYSTEM (0x41)
    )
    
    dsk.save("disco_sistema.dsk")
    
    print(f"\n✅ DSK SYSTEM creado!")
    print(f"   Archivo: disco_sistema.dsk")
    print(f"   Formato: {dsk.get_format_type()}")
    print(f"   Primer sector: 0x{dsk.get_min_sector():02X}")
    print()


def ejemplo_disco_grande():
    """Crear un DSK de alta capacidad"""
    print("=" * 70)
    print("EJEMPLO 3: Crear DSK de alta capacidad (80 pistas)")
    print("=" * 70)
    
    dsk = DSK()
    
    # Disco de doble capacidad
    dsk.create(
        nb_tracks=80,  # Doble de pistas
        nb_sectors=9,
        format_type=DSK.FORMAT_DATA
    )
    
    dsk.save("disco_grande.dsk")
    
    info = dsk.get_info()
    print(f"\n✅ DSK de alta capacidad creado!")
    print(f"   Archivo: disco_grande.dsk")
    print(f"   Pistas: {info['tracks']}")
    print(f"   Capacidad: {info['capacity_kb']} KB")
    print(f"   Tamaño archivo: {info['total_size']:,} bytes")
    print()


def ejemplo_coleccion():
    """Crear una colección de discos numerados"""
    print("=" * 70)
    print("EJEMPLO 4: Crear colección de discos (5 unidades)")
    print("=" * 70)
    
    base_name = "coleccion"
    cantidad = 5
    
    print(f"\n📀 Creando {cantidad} discos...")
    print()
    
    for i in range(1, cantidad + 1):
        # Crear DSK
        dsk = DSK()
        dsk.create(nb_tracks=40, nb_sectors=9)
        
        # Nombre con número de serie
        filename = f"{base_name}_{i:03d}.dsk"
        dsk.save(filename)
        
        info = dsk.get_info()
        print(f"   ✅ Disco {i}/{cantidad}: {filename} ({info['capacity_kb']} KB)")
    
    print(f"\n✅ Colección de {cantidad} discos creada!")
    print()


def ejemplo_diferentes_tamaños():
    """Crear discos con diferentes capacidades"""
    print("=" * 70)
    print("EJEMPLO 5: Crear discos de diferentes tamaños")
    print("=" * 70)
    
    configuraciones = [
        ("compacto.dsk", 35, "Disco compacto"),
        ("estandar.dsk", 40, "Disco estándar"),
        ("extendido.dsk", 42, "Disco extendido"),
        ("doble.dsk", 80, "Disco doble densidad"),
    ]
    
    print()
    for filename, pistas, descripcion in configuraciones:
        dsk = DSK()
        dsk.create(nb_tracks=pistas, nb_sectors=9)
        dsk.save(filename)
        
        info = dsk.get_info()
        print(f"   ✅ {descripcion:25s} -> {filename:20s} ({info['capacity_kb']:3d} KB)")
    
    print()


def ejemplo_con_verificacion():
    """Crear un DSK y verificar que fue creado correctamente"""
    print("=" * 70)
    print("EJEMPLO 6: Crear DSK con verificación")
    print("=" * 70)
    
    filename = "verificado.dsk"
    
    # Crear DSK
    print("\n📝 Paso 1: Creando DSK...")
    dsk1 = DSK()
    dsk1.create(nb_tracks=40, nb_sectors=9)
    dsk1.save(filename)
    print(f"   ✅ DSK guardado: {filename}")
    
    # Verificar cargándolo de nuevo
    print("\n🔍 Paso 2: Verificando DSK...")
    dsk2 = DSK(filename)
    info = dsk2.get_info()
    
    print(f"   ✅ DSK cargado correctamente")
    print(f"   📊 Información:")
    print(f"      - Formato: {info['format']}")
    print(f"      - Pistas: {info['tracks']}")
    print(f"      - Capacidad: {info['capacity_kb']} KB")
    print(f"      - Espacio libre: {dsk2.get_free_space()} KB")
    
    # Verificar que está vacío
    entries = dsk2.get_directory_entries()
    archivos = [e for e in entries if not e.is_deleted]
    
    print(f"\n✅ Verificación completada!")
    print(f"   Archivos en el disco: {len(archivos)}")
    print()


def main():
    """Ejecutar todos los ejemplos"""
    print("\n" + "=" * 70)
    print(" PyDSK - Ejemplos de creación de imágenes DSK")
    print("=" * 70 + "\n")
    
    # Ejecutar ejemplos
    ejemplo_basico()
    ejemplo_formato_system()
    ejemplo_disco_grande()
    ejemplo_coleccion()
    ejemplo_diferentes_tamaños()
    ejemplo_con_verificacion()
    
    print("=" * 70)
    print("✅ Todos los ejemplos completados")
    print("=" * 70)
    print("\nArchivos creados en el directorio actual:")
    print("  - mi_primer_disco.dsk")
    print("  - disco_sistema.dsk")
    print("  - disco_grande.dsk")
    print("  - coleccion_001.dsk ... coleccion_005.dsk")
    print("  - compacto.dsk, estandar.dsk, extendido.dsk, doble.dsk")
    print("  - verificado.dsk")
    print()


if __name__ == '__main__':
    main()
