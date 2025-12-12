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
Ejemplos de uso de PyDSK desde Python
"""

import sys
from pathlib import Path

# Añadir el directorio padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pydsk import DSK


def ejemplo_crear_dsk():
    """Ejemplo 1: Crear una nueva imagen DSK"""
    print("=" * 60)
    print("Ejemplo 1: Crear nueva imagen DSK")
    print("=" * 60)
    
    # Crear DSK vacío
    dsk = DSK()
    
    # Formatear con 40 pistas, 9 sectores por pista, formato DATA
    dsk.create(nb_tracks=40, nb_sectors=9, format_type=DSK.FORMAT_DATA)
    
    # Guardar
    output_file = "test_output.dsk"
    dsk.save(output_file)
    
    print(f"✅ DSK creado: {output_file}")
    print(f"   {dsk}")
    print()


def ejemplo_cargar_dsk():
    """Ejemplo 2: Cargar y analizar un DSK existente"""
    print("=" * 60)
    print("Ejemplo 2: Cargar DSK existente")
    print("=" * 60)
    
    # Primero crear uno para el ejemplo
    dsk = DSK()
    dsk.create(nb_tracks=42, nb_sectors=9)
    dsk.save("ejemplo_load.dsk")
    
    # Ahora cargarlo
    dsk2 = DSK("ejemplo_load.dsk")
    
    print(f"✅ DSK cargado: {dsk2}")
    print()
    
    # Obtener información detallada
    info = dsk2.get_info()
    print("📋 Información detallada:")
    for key, value in info.items():
        print(f"   {key:15s}: {value}")
    print()


def ejemplo_diferentes_formatos():
    """Ejemplo 3: Crear DSKs con diferentes formatos"""
    print("=" * 60)
    print("Ejemplo 3: Diferentes formatos de DSK")
    print("=" * 60)
    
    formatos = [
        ('DATA', DSK.FORMAT_DATA, "formato_data.dsk"),
        ('SYSTEM', DSK.FORMAT_SYSTEM, "formato_system.dsk"),
        ('VENDOR', DSK.FORMAT_VENDOR, "formato_vendor.dsk"),
    ]
    
    for nombre, formato, archivo in formatos:
        dsk = DSK()
        dsk.create(nb_tracks=40, nb_sectors=9, format_type=formato)
        dsk.save(archivo)
        
        info = dsk.get_info()
        print(f"✅ {nombre:10s} -> {archivo:25s} ({info['capacity_kb']} KB)")
    
    print()


def ejemplo_listar_archivos():
    """Ejemplo 4: Listar archivos de un DSK"""
    print("=" * 60)
    print("Ejemplo 4: Listar archivos")
    print("=" * 60)
    
    # Primero necesitamos un DSK con archivos
    # Usaremos el DSK de demo si existe
    import os
    dsk_file = "../../demo_8bp_v41_004.dsk"
    
    if not os.path.exists(dsk_file):
        print("⚠️  DSK de demo no encontrado, creando uno vacío...")
        dsk = DSK()
        dsk.create(nb_tracks=40, nb_sectors=9)
        dsk.save("ejemplo_vacio.dsk")
        dsk_file = "ejemplo_vacio.dsk"
    
    # Cargar DSK
    dsk = DSK(dsk_file)
    
    # Listar en formato tabla
    print("\n📋 Formato tabla:")
    print(dsk.list_files(simple=False))
    
    # Listar en formato simple
    print("\n📋 Formato simple:")
    print(dsk.list_files(simple=True))
    
    print()


def ejemplo_uso_clase():
    """Ejemplo 5: Uso de la clase DSK desde otro script"""
    print("=" * 60)
    print("Ejemplo 5: Uso de la clase DSK")
    print("=" * 60)
    
    # Crear instancia
    dsk = DSK()
    
    # Configurar y crear
    dsk.create(
        nb_tracks=40,      # 40 pistas
        nb_sectors=9,      # 9 sectores por pista
        format_type=DSK.FORMAT_DATA  # Formato DATA
    )
    
    # Obtener información
    formato = dsk.get_format_type()
    min_sector = dsk.get_min_sector()
    
    print(f"Formato detectado: {formato}")
    print(f"Primer sector ID: 0x{min_sector:02X}")
    print(f"Representación: {dsk}")
    
    # Guardar
    dsk.save("mi_disco.dsk")
    print(f"✅ Guardado como: mi_disco.dsk")
    print()


def ejemplo_manejo_errores():
    """Ejemplo 6: Manejo de errores"""
    print("=" * 60)
    print("Ejemplo 6: Manejo de errores")
    print("=" * 60)
    
    from pydsk import DSKError, DSKFormatError
    
    # Intentar crear con parámetros inválidos
    try:
        dsk = DSK()
        dsk.create(nb_tracks=100, nb_sectors=9)  # Demasiadas pistas
    except DSKError as e:
        print(f"✅ Error capturado correctamente: {e}")
    
    # Intentar cargar archivo inexistente
    try:
        dsk = DSK("archivo_inexistente.dsk")
    except DSKError as e:
        print(f"✅ Error capturado correctamente: {e}")
    
    print()


def main():
    """Ejecuta todos los ejemplos"""
    print("\n" + "=" * 60)
    print(" PyDSK - Ejemplos de uso")
    print("=" * 60 + "\n")
    
    ejemplo_crear_dsk()
    ejemplo_cargar_dsk()
    ejemplo_diferentes_formatos()
    ejemplo_listar_archivos()
    ejemplo_uso_clase()
    ejemplo_manejo_errores()
    
    print("=" * 60)
    print("✅ Todos los ejemplos completados")
    print("=" * 60)


if __name__ == '__main__':
    main()
