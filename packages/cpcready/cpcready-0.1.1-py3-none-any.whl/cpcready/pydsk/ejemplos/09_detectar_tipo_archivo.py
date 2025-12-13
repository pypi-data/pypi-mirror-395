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
Ejemplo 09: Detectar tipo de archivo
====================================

Este ejemplo demuestra cómo detectar el tipo de archivos en un DSK:
- BASIC-TOKENIZED: Programas BASIC tokenizados
- BASIC-ASCII: Programas BASIC en formato texto
- BINARY: Archivos binarios ejecutables
- ASCII: Archivos de texto
- RAW: Archivos sin formato reconocible
- DELETED: Archivos marcados como eliminados

Compatible con el comando -y/--filetype de iDSK
"""

import sys
import os
import tempfile

# Añadir el directorio padre al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from pydsk.dsk import DSK
from pydsk.basic_viewer import detect_basic_format
from pydsk.exceptions import DSKError


def detect_file_type(dsk, filename, user=0):
    """
    Detecta el tipo de un archivo en el DSK
    
    Returns:
        str: Tipo de archivo (BASIC-TOKENIZED, BASIC-ASCII, BINARY, ASCII, RAW, DELETED)
    """
    # Normalizar nombre para búsqueda
    amsdos_name = dsk._get_amsdos_filename(filename)
    
    # Verificar si el archivo existe y si está eliminado
    entries = dsk.get_directory_entries()
    file_found = False
    is_deleted = False
    
    # Primero buscar archivo no eliminado
    for entry in entries:
        if (entry.full_name == amsdos_name and 
            entry.user == user and
            not entry.is_deleted and
            entry.num_page == 0):
            file_found = True
            break
    
    # Si no se encuentra no eliminado, buscar eliminado
    if not file_found:
        for entry in entries:
            if (entry.full_name == amsdos_name and 
                entry.is_deleted and
                entry.num_page == 0):
                is_deleted = True
                break
    
    if is_deleted:
        return "DELETED"
    
    # Leer archivo (sin cabecera AMSDOS)
    data = dsk.read_file(filename, user, keep_header=False)
    
    # Determinar tipo de archivo
    file_type = "RAW"  # Default
    
    # Verificar si es BASIC
    is_tokenized, fmt = detect_basic_format(data)
    
    if fmt == "BASIC tokenizado":
        file_type = "BASIC-TOKENIZED"
    elif fmt == "BASIC ASCII":
        file_type = "BASIC-ASCII"
    else:
        # Verificar si parece ASCII o BINARY
        # Buscar el último byte no-cero para ignorar padding
        last_nonzero = len(data) - 1
        while last_nonzero > 0 and data[last_nonzero] == 0:
            last_nonzero -= 1
        
        content = data[:last_nonzero + 1]
        if len(content) > 0:
            # Verificar líneas numeradas (BASIC ASCII)
            try:
                text = content[:min(200, len(content))].decode('ascii', errors='ignore')
                lines = text.split('\n')
                valid_lines = 0
                for line in lines[:5]:
                    line = line.strip()
                    if line and line[0].isdigit():
                        parts = line.split(None, 1)
                        if parts and parts[0].isdigit():
                            valid_lines += 1
                
                if valid_lines > 0:
                    file_type = "BASIC-ASCII"
                else:
                    # Verificar si es mayormente texto ASCII
                    printable = sum(1 for b in content[:min(100, len(content))] 
                                  if (b >= 0x20 and b < 0x7F) or b in (0x09, 0x0A, 0x0D))
                    total = min(100, len(content))
                    if printable >= total * 0.8:  # 80% o más imprimible = ASCII
                        file_type = "ASCII"
                    else:
                        file_type = "BINARY"
            except:
                file_type = "BINARY"
    
    return file_type


# ============================================================================
# Ejemplo 1: Detectar tipo de archivos individuales
# ============================================================================
def ejemplo1_detectar_tipos_individuales():
    """Detectar el tipo de archivos uno por uno"""
    print("=" * 70)
    print("Ejemplo 1: Detectar tipo de archivos individuales")
    print("=" * 70)
    
    try:
        dsk = DSK("../../demo_8bp_v41_004.dsk")
        
        archivos = ["DEMO1.BAS", "DEMO10.BAS", "8BP.BIN", "CICLO.BIN"]
        
        print("\nDetección de tipos de archivo:")
        print("-" * 40)
        for filename in archivos:
            try:
                file_type = detect_file_type(dsk, filename)
                print(f"{filename:15} -> {file_type}")
            except DSKError as e:
                print(f"{filename:15} -> ERROR: {e}")
        
        print("\n✅ Ejemplo completado\n")
        
    except FileNotFoundError:
        print("\n⚠️  Archivo demo_8bp_v41_004.dsk no encontrado")
        print("   Este ejemplo requiere el archivo de demostración\n")


# ============================================================================
# Ejemplo 2: Escanear todos los archivos BASIC
# ============================================================================
def ejemplo2_escanear_archivos_basic():
    """Escanear y clasificar todos los archivos BASIC"""
    print("=" * 70)
    print("Ejemplo 2: Escanear y clasificar archivos BASIC")
    print("=" * 70)
    
    try:
        dsk = DSK("../../demo_8bp_v41_004.dsk")
        
        # Obtener todos los archivos
        entries = dsk.get_directory_entries()
        
        tokenized = []
        ascii_files = []
        
        print("\nEscaneando archivos .BAS y .BAK...")
        print("-" * 40)
        
        for entry in entries:
            if entry.is_deleted or entry.num_page != 0:
                continue
            
            filename = entry.full_name
            if filename.endswith('.BAS') or filename.endswith('.BAK'):
                try:
                    file_type = detect_file_type(dsk, filename)
                    if file_type == "BASIC-TOKENIZED":
                        tokenized.append(filename)
                    elif file_type == "BASIC-ASCII":
                        ascii_files.append(filename)
                except:
                    pass
        
        print(f"\n📦 Archivos BASIC tokenizados: {len(tokenized)}")
        for f in tokenized:
            print(f"   - {f}")
        
        print(f"\n📄 Archivos BASIC ASCII: {len(ascii_files)}")
        for f in ascii_files:
            print(f"   - {f}")
        
        print("\n✅ Ejemplo completado\n")
        
    except FileNotFoundError:
        print("\n⚠️  Archivo demo_8bp_v41_004.dsk no encontrado\n")


# ============================================================================
# Ejemplo 3: Clasificar todos los archivos por tipo
# ============================================================================
def ejemplo3_clasificar_todos_archivos():
    """Clasificar todos los archivos del DSK por tipo"""
    print("=" * 70)
    print("Ejemplo 3: Clasificar todos los archivos por tipo")
    print("=" * 70)
    
    try:
        dsk = DSK("../../demo_8bp_v41_004.dsk")
        
        # Diccionario para clasificar
        tipos = {
            "BASIC-TOKENIZED": [],
            "BASIC-ASCII": [],
            "BINARY": [],
            "ASCII": [],
            "RAW": [],
            "DELETED": []
        }
        
        # Obtener todos los archivos
        entries = dsk.get_directory_entries()
        
        print("\nClasificando archivos...")
        print("-" * 40)
        
        for entry in entries:
            if entry.num_page != 0:  # Solo primera página
                continue
            
            filename = entry.full_name
            if not filename or filename.strip() == "":
                continue
            
            try:
                file_type = detect_file_type(dsk, filename)
                tipos[file_type].append(filename)
            except:
                pass
        
        # Mostrar resultados
        print("\n📊 Clasificación de archivos:")
        print("=" * 40)
        
        for tipo, archivos in tipos.items():
            if archivos:
                print(f"\n{tipo}: {len(archivos)} archivo(s)")
                for f in archivos[:5]:  # Mostrar hasta 5
                    print(f"   - {f}")
                if len(archivos) > 5:
                    print(f"   ... y {len(archivos) - 5} más")
        
        print("\n✅ Ejemplo completado\n")
        
    except FileNotFoundError:
        print("\n⚠️  Archivo demo_8bp_v41_004.dsk no encontrado\n")


# ============================================================================
# Ejemplo 4: Crear DSK de prueba con diferentes tipos
# ============================================================================
def ejemplo4_crear_dsk_con_diferentes_tipos():
    """Crear un DSK con diferentes tipos de archivos"""
    print("=" * 70)
    print("Ejemplo 4: Crear DSK con diferentes tipos de archivos")
    print("=" * 70)
    
    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(suffix='.dsk', delete=False) as f:
        temp_dsk = f.name
    
    try:
        # Crear DSK
        print("\n1. Creando DSK vacío...")
        dsk = DSK()
        dsk.create(nb_tracks=40, nb_sectors=9, format_type=DSK.FORMAT_DATA)
        dsk.save(temp_dsk)
        dsk = DSK(temp_dsk)
        
        # Crear archivos temporales
        with tempfile.NamedTemporaryFile(mode='w', suffix='.bas', delete=False) as f:
            f.write('10 PRINT "HELLO"\n20 END\n')
            temp_ascii = f.name
        
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.bin', delete=False) as f:
            f.write(b'\xC3\x00\x40' + bytes(100))  # Código binario
            temp_bin = f.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write('Este es un archivo de texto plano.\nCon varias líneas.\n')
            temp_txt = f.name
        
        # Importar archivos
        print("2. Importando BASIC ASCII...")
        dsk.write_file(temp_ascii, dsk_filename="ASCII.BAS", file_type=2, user=0)
        
        print("3. Importando archivo binario...")
        dsk.write_file(temp_bin, dsk_filename="CODE.BIN", file_type=2, user=0)
        
        print("4. Importando archivo de texto...")
        dsk.write_file(temp_txt, dsk_filename="README.TXT", file_type=2, user=0)
        
        # Detectar tipos
        print("\n5. Detectando tipos de archivo:")
        print("-" * 40)
        for filename in ["ASCII.BAS", "CODE.BIN", "README.TXT"]:
            file_type = detect_file_type(dsk, filename)
            print(f"{filename:15} -> {file_type}")
        
        print(f"\n✅ DSK de prueba creado: {temp_dsk}\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
    finally:
        # Limpiar archivos temporales
        try:
            os.unlink(temp_dsk)
            os.unlink(temp_ascii)
            os.unlink(temp_bin)
            os.unlink(temp_txt)
        except:
            pass


# ============================================================================
# Ejemplo 5: Detectar archivos eliminados
# ============================================================================
def ejemplo5_detectar_archivos_eliminados():
    """Detectar archivos marcados como eliminados"""
    print("=" * 70)
    print("Ejemplo 5: Detectar archivos eliminados")
    print("=" * 70)
    
    try:
        dsk = DSK("../../demo_8bp_v41_004.dsk")
        
        # Obtener todos los archivos (incluyendo eliminados)
        entries = dsk.get_directory_entries()
        
        print("\nBuscando archivos eliminados...")
        print("-" * 40)
        
        deleted_count = 0
        for entry in entries:
            if entry.is_deleted and entry.num_page == 0:
                filename = entry.full_name
                if filename and filename.strip() != "":
                    print(f"🗑️  {filename} (usuario {entry.user if entry.user != 229 else '0xE5'})")
                    deleted_count += 1
        
        if deleted_count == 0:
            print("No se encontraron archivos eliminados")
        else:
            print(f"\n📊 Total: {deleted_count} archivo(s) eliminado(s)")
        
        print("\n✅ Ejemplo completado\n")
        
    except FileNotFoundError:
        print("\n⚠️  Archivo demo_8bp_v41_004.dsk no encontrado\n")


# ============================================================================
# Ejemplo 6: Comparar con comando CLI
# ============================================================================
def ejemplo6_usar_desde_cli():
    """Mostrar cómo usar el comando desde CLI"""
    print("=" * 70)
    print("Ejemplo 6: Usar comando filetype desde CLI")
    print("=" * 70)
    
    print("\nEl comando 'filetype' está disponible desde la línea de comandos:")
    print("-" * 70)
    
    print("\n# Detectar tipo de un archivo:")
    print("python3 -m pydsk.cli filetype ../../demo_8bp_v41_004.dsk \"DEMO1.BAS\"")
    
    print("\n# Detectar múltiples archivos:")
    print("python3 -m pydsk.cli filetype ../../demo_8bp_v41_004.dsk \"DEMO1.BAS\" \"8BP.BIN\"")
    
    print("\n# Con usuario específico:")
    print("python3 -m pydsk.cli filetype mydisk.dsk \"FILE.BAS\" --user 10")
    
    print("\n# Tipos detectados:")
    print("  - BASIC-TOKENIZED  : Programa BASIC tokenizado")
    print("  - BASIC-ASCII      : Programa BASIC en texto")
    print("  - BINARY           : Archivo binario ejecutable")
    print("  - ASCII            : Archivo de texto plano")
    print("  - RAW              : Formato desconocido")
    print("  - DELETED          : Archivo eliminado")
    
    print("\n" + "=" * 70)
    print("Compatible con iDSK: idsk20 floppy.dsk -y program.bas")
    print("=" * 70 + "\n")


# ============================================================================
# Menú principal
# ============================================================================
def main():
    """Ejecutar todos los ejemplos"""
    print("\n" + "=" * 70)
    print("  EJEMPLOS DE DETECCIÓN DE TIPO DE ARCHIVO")
    print("=" * 70 + "\n")
    
    while True:
        print("Seleccione un ejemplo:")
        print("  1. Detectar tipos individuales")
        print("  2. Escanear archivos BASIC")
        print("  3. Clasificar todos los archivos")
        print("  4. Crear DSK con diferentes tipos")
        print("  5. Detectar archivos eliminados")
        print("  6. Usar desde CLI")
        print("  7. Ejecutar todos los ejemplos")
        print("  0. Salir")
        
        opcion = input("\nOpción: ").strip()
        print()
        
        if opcion == "1":
            ejemplo1_detectar_tipos_individuales()
        elif opcion == "2":
            ejemplo2_escanear_archivos_basic()
        elif opcion == "3":
            ejemplo3_clasificar_todos_archivos()
        elif opcion == "4":
            ejemplo4_crear_dsk_con_diferentes_tipos()
        elif opcion == "5":
            ejemplo5_detectar_archivos_eliminados()
        elif opcion == "6":
            ejemplo6_usar_desde_cli()
        elif opcion == "7":
            ejemplo1_detectar_tipos_individuales()
            ejemplo2_escanear_archivos_basic()
            ejemplo3_clasificar_todos_archivos()
            ejemplo4_crear_dsk_con_diferentes_tipos()
            ejemplo5_detectar_archivos_eliminados()
            ejemplo6_usar_desde_cli()
            break
        elif opcion == "0":
            print("¡Hasta luego!\n")
            break
        else:
            print("❌ Opción inválida\n")


if __name__ == "__main__":
    main()
