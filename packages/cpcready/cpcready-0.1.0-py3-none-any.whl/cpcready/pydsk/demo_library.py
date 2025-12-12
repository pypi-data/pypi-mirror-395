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
Script de demostración: Usando PyDSK como librería
Este es un ejemplo de cómo usar PyDSK desde tus propios scripts
"""

import sys
from pathlib import Path

# Añadir pydsk al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pydsk import DSK, DSKError


def crear_disco_para_juego(nombre_juego: str, output: str) -> bool:
    """
    Crea un disco formateado listo para un juego
    
    Args:
        nombre_juego: Nombre del juego
        output: Ruta del archivo DSK a crear
    
    Returns:
        True si fue exitoso
    """
    try:
        print(f"📀 Creando disco para: {nombre_juego}")
        
        # Crear imagen DSK
        dsk = DSK()
        dsk.create(
            nb_tracks=40,
            nb_sectors=9,
            format_type=DSK.FORMAT_DATA
        )
        
        # Guardar
        dsk.save(output)
        
        # Mostrar información
        info = dsk.get_info()
        print(f"✅ Disco creado: {output}")
        print(f"   Capacidad: {info['capacity_kb']} KB")
        print(f"   Formato: {info['format']}")
        
        return True
        
    except DSKError as e:
        print(f"❌ Error: {e}")
        return False


def crear_coleccion_discos(base_name: str, cantidad: int = 5):
    """
    Crea una colección de discos numerados
    
    Args:
        base_name: Nombre base para los discos
        cantidad: Número de discos a crear
    """
    print(f"\n📀 Creando colección de {cantidad} discos...")
    print("=" * 50)
    
    for i in range(1, cantidad + 1):
        filename = f"{base_name}_{i:02d}.dsk"
        
        dsk = DSK()
        dsk.create(nb_tracks=40, nb_sectors=9)
        dsk.save(filename)
        
        print(f"✅ Disco {i:2d}/{cantidad}: {filename}")
    
    print("=" * 50)
    print(f"✅ Colección completada: {cantidad} discos creados")


def crear_discos_diferentes_tamaños():
    """
    Crea discos con diferentes capacidades
    """
    print("\n📀 Creando discos de diferentes tamaños...")
    print("=" * 50)
    
    configuraciones = [
        ("small.dsk", 35, "Pequeño (35 pistas)"),
        ("standard.dsk", 40, "Estándar (40 pistas)"),
        ("large.dsk", 42, "Grande (42 pistas)"),
        ("xlarge.dsk", 80, "Extra grande (80 pistas)"),
    ]
    
    for filename, tracks, descripcion in configuraciones:
        dsk = DSK()
        dsk.create(nb_tracks=tracks, nb_sectors=9)
        dsk.save(filename)
        
        info = dsk.get_info()
        print(f"✅ {descripcion:25s} -> {info['capacity_kb']:3d} KB")
    
    print("=" * 50)


def analizar_disco_existente(filename: str):
    """
    Analiza y muestra información de un disco existente
    
    Args:
        filename: Ruta al archivo DSK
    """
    try:
        print(f"\n🔍 Analizando: {filename}")
        print("=" * 50)
        
        dsk = DSK(filename)
        info = dsk.get_info()
        
        print(f"Archivo:      {info['filename']}")
        print(f"Formato:      {info['format']}")
        print(f"Pistas:       {info['tracks']}")
        print(f"Caras:        {info['heads']}")
        print(f"Tam. pista:   {info['track_size']:,} bytes")
        print(f"Tam. total:   {info['total_size']:,} bytes")
        print(f"Capacidad:    {info['capacity_kb']} KB")
        
        # Info adicional
        min_sector = dsk.get_min_sector()
        print(f"Primer sect:  0x{min_sector:02X}")
        
        print("=" * 50)
        
    except DSKError as e:
        print(f"❌ Error: {e}")


def ejemplo_uso_en_pipeline():
    """
    Ejemplo de uso en un pipeline de procesamiento
    """
    print("\n🔄 Ejemplo de pipeline de procesamiento")
    print("=" * 50)
    
    # Paso 1: Crear disco base
    print("1. Creando disco base...")
    dsk = DSK()
    dsk.create(nb_tracks=40, nb_sectors=9)
    dsk.save("pipeline_base.dsk")
    print("   ✅ Disco base creado")
    
    # Paso 2: Cargar y verificar
    print("2. Cargando y verificando...")
    dsk2 = DSK("pipeline_base.dsk")
    info = dsk2.get_info()
    print(f"   ✅ Verificado: {info['capacity_kb']} KB disponibles")
    
    # Paso 3: Aquí irían operaciones adicionales (importar archivos, etc.)
    print("3. [Aquí irían más operaciones...]")
    
    # Paso 4: Guardar versión final
    print("4. Guardando versión final...")
    dsk2.save("pipeline_final.dsk")
    print("   ✅ Pipeline completado")
    
    print("=" * 50)


def main():
    """Función principal con ejemplos"""
    print("\n" + "=" * 60)
    print(" PyDSK - Ejemplos de uso como librería")
    print("=" * 60)
    
    # Ejemplo 1: Crear disco para un juego específico
    crear_disco_para_juego("Super Adventure", "adventure_disk.dsk")
    
    # Ejemplo 2: Crear colección
    crear_coleccion_discos("backup", 5)
    
    # Ejemplo 3: Diferentes tamaños
    crear_discos_diferentes_tamaños()
    
    # Ejemplo 4: Analizar disco existente
    analizar_disco_existente("adventure_disk.dsk")
    
    # Ejemplo 5: Pipeline
    ejemplo_uso_en_pipeline()
    
    print("\n" + "=" * 60)
    print("✅ Todos los ejemplos completados")
    print("=" * 60)
    
    # Limpiar archivos de ejemplo
    cleanup_files = [
        "adventure_disk.dsk",
        "backup_01.dsk", "backup_02.dsk", "backup_03.dsk", 
        "backup_04.dsk", "backup_05.dsk",
        "small.dsk", "standard.dsk", "large.dsk", "xlarge.dsk",
        "pipeline_base.dsk", "pipeline_final.dsk"
    ]
    
    print("\n🧹 Limpiando archivos de ejemplo...")
    for f in cleanup_files:
        try:
            Path(f).unlink()
        except:
            pass
    print("✅ Limpieza completada")


if __name__ == '__main__':
    main()
