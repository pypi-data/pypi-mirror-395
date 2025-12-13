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
Ejemplo 10: Gestión de cabeceras AMSDOS en archivos externos
=============================================================

Este ejemplo muestra cómo añadir y eliminar cabeceras AMSDOS
en archivos externos (fuera de imágenes DSK).

La cabecera AMSDOS contiene información importante como:
- Dirección de carga (load address)
- Dirección de ejecución (exec address)
- Tipo de archivo (binario, BASIC, etc.)
- Tamaño del archivo
- Checksum de verificación
"""

import sys
import tempfile
import os
from pathlib import Path

# Añadir PyDSK al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pydsk import DSK, DSKError


def print_header(title: str):
    """Imprime un encabezado decorativo"""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70 + "\n")


def ejemplo_add_header_binario():
    """Ejemplo 1: Añadir cabecera AMSDOS a un archivo binario"""
    print_header("EJEMPLO 1: Añadir cabecera a archivo binario")
    
    try:
        # Crear archivo binario de prueba (código Z80 simple)
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.bin', delete=False) as f:
            # NOP, NOP, RET (código Z80 simple)
            binary_data = bytes([0x00, 0x00, 0xC9] * 100)
            f.write(binary_data)
            temp_file = f.name
        
        output_file = "codigo_con_header.bin"
        
        # Añadir cabecera AMSDOS
        DSK.add_amsdos_header(
            temp_file,
            output_file,
            load_addr=0x4000,  # Cargar en &4000
            exec_addr=0x4000,  # Ejecutar desde &4000
            file_type=0,       # Binario
            force=True
        )
        
        print(f"Archivo binario creado: {output_file}")
        
        # Verificar tamaños
        original_size = os.path.getsize(temp_file)
        with_header_size = os.path.getsize(output_file)
        
        print(f"  Tamaño original:     {original_size} bytes")
        print(f"  Con cabecera:        {with_header_size} bytes")
        print(f"  Cabecera añadida:    {with_header_size - original_size} bytes")
        print(f"  Dirección de carga:  &4000")
        print(f"  Dirección ejecución: &4000")
        
        # Limpiar
        os.unlink(temp_file)
        
    except DSKError as e:
        print(f"Error: {e}")


def ejemplo_add_header_basic():
    """Ejemplo 2: Añadir cabecera a archivo BASIC ASCII"""
    print_header("EJEMPLO 2: Añadir cabecera a archivo BASIC ASCII")
    
    try:
        # Crear archivo BASIC ASCII de prueba
        with tempfile.NamedTemporaryFile(mode='w', suffix='.bas', delete=False) as f:
            f.write("10 REM Programa de ejemplo\n")
            f.write("20 PRINT \"Hola desde BASIC\"\n")
            f.write("30 FOR I=1 TO 10\n")
            f.write("40 PRINT I\n")
            f.write("50 NEXT I\n")
            temp_file = f.name
        
        output_file = "programa_con_header.bas"
        
        # Añadir cabecera AMSDOS (tipo 2 = BASIC ASCII)
        DSK.add_amsdos_header(
            temp_file,
            output_file,
            load_addr=0,      # AUTO (0x0170 para BASIC)
            exec_addr=0,      # AUTO (igual que load)
            file_type=2,      # BASIC ASCII
            force=True
        )
        
        print(f"Archivo BASIC creado: {output_file}")
        
        original_size = os.path.getsize(temp_file)
        with_header_size = os.path.getsize(output_file)
        
        print(f"  Tamaño original:     {original_size} bytes")
        print(f"  Con cabecera:        {with_header_size} bytes")
        print(f"  Dirección de carga:  AUTO (0x0170)")
        print(f"  Tipo:                BASIC ASCII")
        
        # Limpiar
        os.unlink(temp_file)
        
    except DSKError as e:
        print(f"Error: {e}")


def ejemplo_remove_header():
    """Ejemplo 3: Eliminar cabecera AMSDOS"""
    print_header("EJEMPLO 3: Eliminar cabecera AMSDOS")
    
    try:
        # Primero crear un archivo con cabecera
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.bin', delete=False) as f:
            binary_data = bytes([0xFF, 0xAA, 0x55] * 50)
            f.write(binary_data)
            temp_file = f.name
        
        file_with_header = "temporal_con_header.bin"
        file_without_header = "temporal_sin_header.bin"
        
        # Añadir cabecera
        DSK.add_amsdos_header(
            temp_file,
            file_with_header,
            load_addr=0x8000,
            exec_addr=0x8000,
            file_type=0,
            force=True
        )
        
        print("Paso 1: Archivo con cabecera creado")
        size_with = os.path.getsize(file_with_header)
        print(f"  Tamaño: {size_with} bytes")
        
        # Eliminar cabecera
        DSK.remove_amsdos_header(
            file_with_header,
            file_without_header,
            force=True
        )
        
        print("\nPaso 2: Cabecera eliminada")
        size_without = os.path.getsize(file_without_header)
        print(f"  Tamaño: {size_without} bytes")
        print(f"  Cabecera eliminada: {size_with - size_without} bytes")
        
        # Verificar que el contenido es idéntico al original
        with open(temp_file, 'rb') as f1, open(file_without_header, 'rb') as f2:
            original = f1.read()
            extracted = f2.read()
            if original == extracted:
                print("\nVerificación: Contenido idéntico al original")
            else:
                print("\nAdvertencia: El contenido difiere del original")
        
        # Limpiar
        os.unlink(temp_file)
        os.unlink(file_with_header)
        os.unlink(file_without_header)
        
    except DSKError as e:
        print(f"Error: {e}")


def ejemplo_ciclo_completo():
    """Ejemplo 4: Ciclo completo con importación a DSK"""
    print_header("EJEMPLO 4: Ciclo completo - archivo externo -> DSK -> extracción")
    
    try:
        # 1. Crear archivo original
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.bin', delete=False) as f:
            original_data = bytes([0x01, 0x02, 0x03, 0x04, 0x05] * 50)
            f.write(original_data)
            original_file = f.name
        
        print("Paso 1: Archivo original creado")
        print(f"  Tamaño: {os.path.getsize(original_file)} bytes")
        
        # 2. Añadir cabecera AMSDOS
        file_with_header = "temp_with_header.bin"
        DSK.add_amsdos_header(
            original_file,
            file_with_header,
            load_addr=0x6000,
            exec_addr=0x6000,
            file_type=0,
            force=True
        )
        
        print("\nPaso 2: Cabecera AMSDOS añadida")
        print(f"  Tamaño: {os.path.getsize(file_with_header)} bytes")
        
        # 3. Importar a DSK
        dsk = DSK()
        dsk.create(40, 9)
        
        # Importar directamente el archivo con cabecera
        # write_file detecta automáticamente la cabecera
        dsk.write_file(file_with_header, 'CODIGO.BIN', user=0)
        
        dsk.save("temp_ciclo.dsk")
        
        print("\nPaso 3: Archivo importado a DSK")
        print("  DSK: temp_ciclo.dsk")
        print("  Archivo: CODIGO.BIN")
        
        # 4. Listar contenido
        print("\nPaso 4: Contenido del DSK:")
        dsk.list_files()
        
        # 5. Extraer del DSK
        extracted_file = "temp_extracted.bin"
        dsk.export_file('CODIGO.BIN', extracted_file, user=0, keep_header=True)
        
        print("\nPaso 5: Archivo extraído del DSK")
        print(f"  Tamaño: {os.path.getsize(extracted_file)} bytes")
        
        # 6. Eliminar cabecera del extraído
        final_file = "temp_final.bin"
        DSK.remove_amsdos_header(extracted_file, final_file, force=True)
        
        print("\nPaso 6: Cabecera eliminada del archivo extraído")
        print(f"  Tamaño: {os.path.getsize(final_file)} bytes")
        
        # Verificar que el contenido final es idéntico al original
        with open(original_file, 'rb') as f1, open(final_file, 'rb') as f2:
            original = f1.read()
            final = f2.read()
            if original == final:
                print("\nVerificación: Ciclo completo exitoso")
                print("  El archivo final es idéntico al original")
            else:
                print("\nAdvertencia: El archivo final difiere del original")
        
        # Limpiar
        os.unlink(original_file)
        os.unlink(file_with_header)
        os.unlink(extracted_file)
        os.unlink(final_file)
        os.unlink("temp_ciclo.dsk")
        
    except DSKError as e:
        print(f"Error: {e}")


def ejemplo_informacion_cabecera():
    """Ejemplo 5: Leer información de cabecera AMSDOS"""
    print_header("EJEMPLO 5: Leer información de cabecera AMSDOS")
    
    try:
        # Crear archivo con cabecera
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            test_data = bytes([0xAA] * 1000)
            f.write(test_data)
            temp_file = f.name
        
        file_with_header = "temp_info.bin"
        
        # Añadir cabecera con valores específicos
        DSK.add_amsdos_header(
            temp_file,
            file_with_header,
            load_addr=0x2000,
            exec_addr=0x2100,
            file_type=0,
            force=True
        )
        
        # Leer y analizar la cabecera
        with open(file_with_header, 'rb') as f:
            header = f.read(128)  # Primeros 128 bytes = cabecera AMSDOS
        
        import struct
        
        print("Información de la cabecera AMSDOS:")
        print("=" * 50)
        
        # Tipo de archivo
        file_type_byte = header[0]
        type_names = {0x00: "BASIC", 0x16: "Binario"}
        print(f"  Tipo de archivo:     {type_names.get(file_type_byte, 'Desconocido')} (0x{file_type_byte:02X})")
        
        # Nombre del archivo (bytes 1-8)
        filename = header[1:9].decode('ascii').strip()
        print(f"  Nombre:              {filename}")
        
        # Extensión (bytes 9-11)
        extension = header[9:12].decode('ascii').strip()
        print(f"  Extensión:           {extension}")
        
        # Tamaño del archivo (bytes 0x18-0x19)
        file_length = struct.unpack('<H', header[0x18:0x1A])[0]
        print(f"  Tamaño:              {file_length} bytes")
        
        # Dirección de carga (bytes 0x15-0x16)
        load_addr = struct.unpack('<H', header[0x15:0x17])[0]
        print(f"  Dirección de carga:  &{load_addr:04X}")
        
        # Dirección de ejecución (bytes 0x1A-0x1B)
        exec_addr = struct.unpack('<H', header[0x1A:0x1C])[0]
        print(f"  Dirección de ejec:   &{exec_addr:04X}")
        
        # Checksum (bytes 0x43-0x44)
        checksum = struct.unpack('<H', header[0x43:0x45])[0]
        print(f"  Checksum:            &{checksum:04X}")
        
        # Verificar checksum
        checksum_calc = sum(header[0:67]) & 0xFFFF
        print(f"  Checksum calculado:  &{checksum_calc:04X}")
        print(f"  Checksum válido:     {'Sí' if checksum == checksum_calc else 'No'}")
        
        # Limpiar
        os.unlink(temp_file)
        os.unlink(file_with_header)
        
    except DSKError as e:
        print(f"Error: {e}")


def ejemplo_cli_usage():
    """Ejemplo 6: Uso desde línea de comandos"""
    print_header("EJEMPLO 6: Uso desde línea de comandos (CLI)")
    
    print("Comandos disponibles para gestión de cabeceras AMSDOS:\n")
    
    print("1. Añadir cabecera a un archivo:")
    print("   python -m pydsk.cli add-header input.bin output.bin -l 0x4000 -e 0x4000 -t 0")
    print("   ")
    print("   Parámetros:")
    print("     input.bin   : Archivo sin cabecera")
    print("     output.bin  : Archivo con cabecera")
    print("     -l, --load  : Dirección de carga (hex o decimal, 0=auto)")
    print("     -e, --exec  : Dirección de ejecución (hex o decimal, 0=auto)")
    print("     -t, --type  : Tipo (0=binario, 1=BASIC protegido, 2=BASIC ASCII, 3=binario protegido)")
    print("     -f, --force : Sobrescribir si existe")
    
    print("\n2. Eliminar cabecera de un archivo:")
    print("   python -m pydsk.cli remove-header input.bin output.bin")
    print("   ")
    print("   Parámetros:")
    print("     input.bin   : Archivo con cabecera")
    print("     output.bin  : Archivo sin cabecera")
    print("     -f, --force : Sobrescribir si existe")
    
    print("\n3. Ejemplos prácticos:")
    print("   # Añadir cabecera a código máquina")
    print("   python -m pydsk.cli add-header game.bin game_cpc.bin -l 0x4000 -e 0x4000 -t 0")
    print("   ")
    print("   # Añadir cabecera a BASIC ASCII")
    print("   python -m pydsk.cli add-header program.bas program_cpc.bas -t 2")
    print("   ")
    print("   # Eliminar cabecera de archivo exportado")
    print("   python -m pydsk.cli remove-header exported.bin clean.bin")


def main():
    """Ejecutar todos los ejemplos"""
    print("\n" + "=" * 70)
    print(" PyDSK - Ejemplos de gestión de cabeceras AMSDOS externas")
    print("=" * 70 + "\n")
    
    # Ejecutar ejemplos
    ejemplo_add_header_binario()
    ejemplo_add_header_basic()
    ejemplo_remove_header()
    ejemplo_ciclo_completo()
    ejemplo_informacion_cabecera()
    ejemplo_cli_usage()
    
    print("\n" + "=" * 70)
    print("Todos los ejemplos completados")
    print("=" * 70)
    print()
    
    # Limpiar archivos temporales que pudieran quedar
    for temp_file in ["codigo_con_header.bin", "programa_con_header.bas"]:
        try:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
        except:
            pass


if __name__ == '__main__':
    main()
