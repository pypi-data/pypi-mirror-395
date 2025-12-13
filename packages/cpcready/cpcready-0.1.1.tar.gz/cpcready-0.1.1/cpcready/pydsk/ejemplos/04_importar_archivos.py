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
Ejemplos de importación de archivos a DSK
Muestra cómo usar PyDSK para importar archivos al DSK
"""

import sys
import os
from pathlib import Path
import tempfile

# Añadir el directorio padre al path para importar pydsk
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pydsk import DSK, DSKError



def print_header(text):
    """Imprime un encabezado con formato"""
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)


def ejemplo_importar_basic_ascii():
    """Ejemplo 1: Importar archivo BASIC en modo ASCII"""
    print_header("EJEMPLO 1: Importar archivo BASIC (modo ASCII)")
    
    try:
        # Crear archivo BASIC de prueba
        basic_code = """10 REM Programa de ejemplo
20 PRINT "Hola desde PyDSK!"
30 FOR I=1 TO 10
40 PRINT "Numero: "; I
50 NEXT I
60 PRINT "Fin del programa"
"""
        
        # Guardar temporalmente
        with tempfile.NamedTemporaryFile(mode='w', suffix='.bas', delete=False) as f:
            f.write(basic_code)
            temp_file = f.name
        
        # Crear DSK e importar
        dsk = DSK()
        dsk.create(40, 9)
        
        # Modo 2 = BASIC ASCII (sin cabecera, conversión de line endings)
        dsk.write_file(temp_file, dsk_filename='HELLO.BAS', file_type=2, user=0)
        dsk.save('ejemplo1_basic.dsk')
        
        print("Archivo BASIC importado exitosamente")
        print("\nContenido del DSK:")
        # list_files() usa Rich automáticamente si está disponible
        dsk.list_files()
        
        # Limpiar
        os.unlink(temp_file)
        
    except DSKError as e:
        print(f"❌ Error: {e}")


def ejemplo_importar_binario():
    """Ejemplo 2: Importar archivo binario con direcciones load/exec"""
    print_header("EJEMPLO 2: Importar binario con direcciones")
    
    try:
        # Crear archivo binario de prueba (código ficticio)
        binary_data = bytearray([
            0x21, 0x00, 0x40,  # LD HL, 0x4000
            0x11, 0x00, 0xC0,  # LD DE, 0xC000
            0x01, 0x00, 0x10,  # LD BC, 0x1000
            0xED, 0xB0,        # LDIR
            0xC9               # RET
        ])
        
        # Guardar temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.bin') as f:
            f.write(binary_data)
            temp_file = f.name
        
        # Crear DSK e importar con direcciones
        dsk = DSK()
        dsk.create(40, 9)
        
        # Modo 0 = Binario con cabecera AMSDOS
        dsk.write_file(
            temp_file, 
            dsk_filename='CODE.BIN',
            file_type=0,
            load_addr=0x4000,  # Dirección de carga
            exec_addr=0x4000,  # Dirección de ejecución
            user=0
        )
        dsk.save('ejemplo2_binario.dsk')
        
        print("Binario importado con direcciones")
        print("\nContenido del DSK:")
        dsk.list_files()
        
        # Limpiar
        os.unlink(temp_file)
        
    except DSKError as e:
        print(f"❌ Error: {e}")


def ejemplo_importar_multiples():
    """Ejemplo 3: Importar múltiples archivos"""
    print_header("EJEMPLO 3: Importar múltiples archivos")
    
    try:
        # Crear varios archivos de prueba
        archivos = []
        
        # Archivo 1: BASIC
        with tempfile.NamedTemporaryFile(mode='w', suffix='.bas', delete=False) as f:
            f.write("10 PRINT \"Archivo 1\"\n")
            archivos.append(('PROG1.BAS', f.name, 2, 0, 0))
        
        # Archivo 2: BASIC
        with tempfile.NamedTemporaryFile(mode='w', suffix='.bas', delete=False) as f:
            f.write("10 PRINT \"Archivo 2\"\n")
            archivos.append(('PROG2.BAS', f.name, 2, 0, 0))
        
        # Archivo 3: Binario
        with tempfile.NamedTemporaryFile(delete=False, suffix='.bin') as f:
            f.write(b'\x00' * 256)
            archivos.append(('DATA.BIN', f.name, 0, 0x8000, 0x8000))
        
        # Crear DSK e importar todos
        dsk = DSK()
        dsk.create(40, 9)
        
        for dsk_name, host_file, tipo, load, exec_addr in archivos:
            dsk.write_file(
                host_file,
                dsk_filename=dsk_name,
                file_type=tipo,
                load_addr=load,
                exec_addr=exec_addr,
                user=0
            )
            print(f"   ✓ Importado: {dsk_name}")
        
        dsk.save('ejemplo3_multiples.dsk')
        
        print("\nMúltiples archivos importados")
        print("\nContenido del DSK:")
        dsk.list_files()
        
        # Limpiar
        for _, temp_file, *_ in archivos:
            os.unlink(temp_file)
        
    except DSKError as e:
        print(f"❌ Error: {e}")


def ejemplo_importar_con_atributos():
    """Ejemplo 4: Importar con atributos (sistema, solo lectura)"""
    print_header("EJEMPLO 4: Importar con atributos especiales")
    
    try:
        # Crear archivo de prueba
        with tempfile.NamedTemporaryFile(mode='w', suffix='.bas', delete=False) as f:
            f.write("10 REM Archivo del sistema\n20 PRINT \"PROTEGIDO\"\n")
            temp_file = f.name
        
        # Crear DSK
        dsk = DSK()
        dsk.create(40, 9)
        
        # Importar como archivo de sistema y solo lectura
        dsk.write_file(
            temp_file,
            dsk_filename='SYSTEM.BAS',
            file_type=2,
            user=0,
            system=True,      # Marcar como sistema
            read_only=True    # Marcar como solo lectura
        )
        dsk.save('ejemplo4_atributos.dsk')
        
        print("Archivo importado con atributos:")
        print("   - System file: Sí")
        print("   - Read only: Sí")
        print("\nContenido del DSK:")
        dsk.list_files()
        
        # Limpiar
        os.unlink(temp_file)
        
    except DSKError as e:
        print(f"❌ Error: {e}")


def ejemplo_importar_con_forzado():
    """Ejemplo 5: Sobrescribir archivo existente con force=True"""
    print_header("EJEMPLO 5: Sobrescribir archivo existente (force)")
    
    try:
        # Crear dos versiones del archivo
        with tempfile.NamedTemporaryFile(mode='w', suffix='.bas', delete=False) as f:
            f.write("10 PRINT \"Version 1\"\n")
            temp_file1 = f.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.bas', delete=False) as f:
            f.write("10 PRINT \"Version 2 - ACTUALIZADA\"\n")
            temp_file2 = f.name
        
        # Crear DSK e importar primera versión
        dsk = DSK()
        dsk.create(40, 9)
        
        dsk.write_file(temp_file1, dsk_filename='TEST.BAS', file_type=2, user=0)
        print("Primera versión importada")
        print(dsk.list_files(simple=True))
        
        # Intentar importar segunda versión sin force (debería fallar)
        try:
            dsk.write_file(temp_file2, dsk_filename='TEST.BAS', file_type=2, user=0)
            print("⚠️  No debería llegar aquí")
        except DSKError as e:
            print(f"\n❌ Sin force=True: {e}")
        
        # Ahora con force=True
        dsk.write_file(temp_file2, dsk_filename='TEST.BAS', file_type=2, user=0, force=True)
        print("\nCon force=True: Archivo sobrescrito")
        print(dsk.list_files(simple=True))
        
        dsk.save('ejemplo5_force.dsk')
        
        # Limpiar
        os.unlink(temp_file1)
        os.unlink(temp_file2)
        
    except DSKError as e:
        print(f"❌ Error: {e}")


def ejemplo_importar_usuarios():
    """Ejemplo 6: Importar archivos en diferentes áreas de usuario"""
    print_header("EJEMPLO 6: Importar en diferentes usuarios")
    
    try:
        # Crear archivos de prueba
        archivos_por_usuario = []
        
        for user in [0, 1, 2, 10]:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.bas', delete=False) as f:
                f.write(f"10 PRINT \"Usuario {user}\"\n")
                archivos_por_usuario.append((user, f.name))
        
        # Crear DSK e importar en diferentes usuarios
        dsk = DSK()
        dsk.create(40, 9)
        
        for user, temp_file in archivos_por_usuario:
            dsk.write_file(
                temp_file,
                dsk_filename=f'U{user}.BAS',
                file_type=2,
                user=user
            )
            print(f"   ✓ Importado en usuario {user}")
        
        dsk.save('ejemplo6_usuarios.dsk')
        
        print("\nArchivos en diferentes usuarios")
        print("\nContenido del DSK:")
        dsk.list_files()
        
        # Limpiar
        for _, temp_file in archivos_por_usuario:
            os.unlink(temp_file)
        
    except DSKError as e:
        print(f"❌ Error: {e}")


def main():
    """Ejecuta todos los ejemplos"""
    print("=" * 70)
    print(" PyDSK - Ejemplos de importación de archivos")
    print("=" * 70)
    
    ejemplo_importar_basic_ascii()
    ejemplo_importar_binario()
    ejemplo_importar_multiples()
    ejemplo_importar_con_atributos()
    ejemplo_importar_con_forzado()
    ejemplo_importar_usuarios()
    
    print("\n" + "=" * 70)
    print("✅ Todos los ejemplos completados")
    print("=" * 70)
    print("\nArchivos DSK creados:")
    print("   - ejemplo1_basic.dsk")
    print("   - ejemplo2_binario.dsk")
    print("   - ejemplo3_multiples.dsk")
    print("   - ejemplo4_atributos.dsk")
    print("   - ejemplo5_force.dsk")
    print("   - ejemplo6_usuarios.dsk")


if __name__ == '__main__':
    main()
