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
Ejemplos de exportación de archivos desde DSK
Muestra cómo usar PyDSK para extraer archivos del DSK
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


def ejemplo_exportar_archivo():
    """Ejemplo 1: Exportar un archivo específico"""
    print_header("EJEMPLO 1: Exportar archivo específico")
    
    try:
        # Ruta al DSK demo
        dsk_path = Path(__file__).parent.parent.parent / "demo_8bp_v41_004.dsk"
        
        if not dsk_path.exists():
            print(f"⚠️  DSK demo no encontrado: {dsk_path}")
            return
        
        dsk = DSK(str(dsk_path))
        
        # Exportar archivo con cabecera AMSDOS
        output_file = "exported_8bp.bin"
        dsk.export_file("8BP.BIN", output_file, keep_header=True)
        
        print(f"✅ Archivo exportado: {output_file}")
        print(f"   Tamaño: {os.path.getsize(output_file)} bytes")
        print(f"   Con cabecera AMSDOS incluida")
        
        # Limpiar
        if os.path.exists(output_file):
            os.remove(output_file)
        
    except DSKError as e:
        print(f"❌ Error: {e}")


def ejemplo_exportar_sin_cabecera():
    """Ejemplo 2: Exportar sin cabecera AMSDOS"""
    print_header("EJEMPLO 2: Exportar sin cabecera AMSDOS")
    
    try:
        dsk_path = Path(__file__).parent.parent.parent / "demo_8bp_v41_004.dsk"
        
        if not dsk_path.exists():
            print(f"⚠️  DSK demo no encontrado")
            return
        
        dsk = DSK(str(dsk_path))
        
        # Exportar con cabecera
        with_header = "8bp_with_header.bin"
        dsk.export_file("8BP.BIN", with_header, keep_header=True)
        size_with = os.path.getsize(with_header)
        
        # Exportar sin cabecera
        without_header = "8bp_without_header.bin"
        dsk.export_file("8BP.BIN", without_header, keep_header=False)
        size_without = os.path.getsize(without_header)
        
        print(f"✅ Con cabecera:    {size_with:,} bytes")
        print(f"✅ Sin cabecera:    {size_without:,} bytes")
        print(f"   Diferencia:     {size_with - size_without} bytes (128 = header AMSDOS)")
        
        # Limpiar
        for f in [with_header, without_header]:
            if os.path.exists(f):
                os.remove(f)
        
    except DSKError as e:
        print(f"❌ Error: {e}")


def ejemplo_exportar_todos():
    """Ejemplo 3: Exportar todos los archivos"""
    print_header("EJEMPLO 3: Exportar todos los archivos del DSK")
    
    try:
        dsk_path = Path(__file__).parent.parent.parent / "demo_8bp_v41_004.dsk"
        
        if not dsk_path.exists():
            print(f"⚠️  DSK demo no encontrado")
            return
        
        dsk = DSK(str(dsk_path))
        
        # Crear directorio temporal
        with tempfile.TemporaryDirectory() as output_dir:
            # Exportar todos
            exported = dsk.export_all(output_dir, keep_header=True)
            
            print(f"✅ {len(exported)} archivos exportados a: {output_dir}/")
            print("\nArchivos exportados:")
            
            for filename in sorted(exported)[:10]:
                filepath = os.path.join(output_dir, filename)
                size = os.path.getsize(filepath)
                print(f"   - {filename:<15} ({size:>6,} bytes)")
            
            if len(exported) > 10:
                print(f"   ... y {len(exported) - 10} más")
        
    except DSKError as e:
        print(f"❌ Error: {e}")


def ejemplo_exportar_usuario():
    """Ejemplo 4: Exportar archivo de usuario específico"""
    print_header("EJEMPLO 4: Exportar de área de usuario específica")
    
    try:
        dsk_path = Path(__file__).parent.parent.parent / "demo_8bp_v41_004.dsk"
        
        if not dsk_path.exists():
            print(f"⚠️  DSK demo no encontrado")
            return
        
        dsk = DSK(str(dsk_path))
        
        # Ver archivos en diferentes usuarios
        entries = dsk.get_directory_entries()
        
        users_with_files = {}
        for entry in entries:
            if not entry.is_deleted and entry.num_page == 0:
                if entry.user not in users_with_files:
                    users_with_files[entry.user] = []
                users_with_files[entry.user].append(entry.full_name)
        
        print("📂 Archivos por usuario:")
        for user in sorted(users_with_files.keys()):
            files = users_with_files[user]
            print(f"\n   Usuario {user}: {len(files)} archivo(s)")
            for filename in files[:3]:
                print(f"      - {filename}")
            if len(files) > 3:
                print(f"      ... y {len(files) - 3} más")
        
        # Exportar archivo de usuario 10 si existe
        if 10 in users_with_files:
            filename = users_with_files[10][0]
            output_file = f"user10_{filename.replace('.', '_').strip()}.bas"
            dsk.export_file(filename, output_file, user=10, keep_header=False)
            print(f"\n✅ Exportado archivo de usuario 10: {output_file}")
            
            # Limpiar
            if os.path.exists(output_file):
                os.remove(output_file)
        
    except DSKError as e:
        print(f"❌ Error: {e}")


def ejemplo_exportar_desde_creado():
    """Ejemplo 5: Crear DSK, importar y luego exportar"""
    print_header("EJEMPLO 5: Ciclo completo: crear → importar → exportar")
    
    try:
        # Crear DSK temporal
        temp_dsk = "temp_ciclo.dsk"
        dsk = DSK()
        dsk.create(40, 9)
        
        # Crear archivo de prueba
        test_content = b"Contenido de prueba para PyDSK\n" * 10
        test_file = "test_content.txt"
        
        with open(test_file, 'wb') as f:
            f.write(test_content)
        
        # Importar
        print("📥 Importando archivo...")
        dsk.write_file(test_file, dsk_filename="DATA.TXT", file_type=0, 
                      load_addr=0x8000, exec_addr=0x8000)
        dsk.save(temp_dsk)
        print(f"   ✓ Archivo importado al DSK")
        
        # Recargar y exportar
        print("\n📤 Exportando archivo...")
        dsk2 = DSK(temp_dsk)
        exported_file = "exported_data.txt"
        dsk2.export_file("DATA.TXT", exported_file, keep_header=True)
        
        # Comparar
        with open(exported_file, 'rb') as f:
            exported_data = f.read()
        
        # Verificar cabecera AMSDOS
        has_header = dsk2._check_amsdos_header(exported_data)
        
        print(f"   ✓ Archivo exportado")
        print(f"\n📊 Comparación:")
        print(f"   Tamaño original:  {len(test_content):,} bytes")
        print(f"   Tamaño exportado: {len(exported_data):,} bytes")
        print(f"   Tiene cabecera:   {'Sí' if has_header else 'No'}")
        print(f"   Cabecera válida:  {'✅' if has_header else '❌'}")
        
        # Limpiar
        for f in [test_file, temp_dsk, exported_file]:
            if os.path.exists(f):
                os.remove(f)
        
        print("\n✅ Ciclo completo exitoso")
        
    except DSKError as e:
        print(f"❌ Error: {e}")


def ejemplo_comparar_formatos():
    """Ejemplo 6: Comparar exportación con y sin cabecera"""
    print_header("EJEMPLO 6: Análisis de cabecera AMSDOS")
    
    try:
        dsk_path = Path(__file__).parent.parent.parent / "demo_8bp_v41_004.dsk"
        
        if not dsk_path.exists():
            print(f"⚠️  DSK demo no encontrado")
            return
        
        dsk = DSK(str(dsk_path))
        
        # Exportar archivo binario
        filename = "8BP.BIN"
        
        # Con cabecera
        with_header = "with_header.bin"
        dsk.export_file(filename, with_header, keep_header=True)
        
        with open(with_header, 'rb') as f:
            data = f.read()
        
        print(f"📄 Archivo: {filename}")
        print(f"\n🔍 Análisis de cabecera AMSDOS:")
        print(f"   Tamaño total: {len(data):,} bytes")
        
        if dsk._check_amsdos_header(data):
            import struct
            
            # Parsear cabecera
            file_type = data[0]
            name = data[1:9].decode('ascii', errors='ignore').strip()
            ext = data[9:12].decode('ascii', errors='ignore').strip()
            file_length = struct.unpack('<H', data[0x18:0x1A])[0]
            load_addr = struct.unpack('<H', data[0x15:0x17])[0]
            exec_addr = struct.unpack('<H', data[0x1A:0x1C])[0]
            checksum = struct.unpack('<H', data[0x43:0x45])[0]
            
            print(f"\n   Tipo:            0x{file_type:02X}")
            print(f"   Nombre:          {name}.{ext}")
            print(f"   Longitud:        {file_length:,} bytes")
            print(f"   Load address:    0x{load_addr:04X}")
            print(f"   Exec address:    0x{exec_addr:04X}")
            print(f"   Checksum:        0x{checksum:04X}")
            print(f"\n   ✅ Cabecera válida")
        else:
            print("   ❌ No tiene cabecera válida")
        
        # Limpiar
        if os.path.exists(with_header):
            os.remove(with_header)
        
    except DSKError as e:
        print(f"❌ Error: {e}")


def main():
    """Ejecuta todos los ejemplos"""
    print("=" * 70)
    print(" PyDSK - Ejemplos de exportación de archivos")
    print("=" * 70)
    
    ejemplo_exportar_archivo()
    ejemplo_exportar_sin_cabecera()
    ejemplo_exportar_todos()
    ejemplo_exportar_usuario()
    ejemplo_exportar_desde_creado()
    ejemplo_comparar_formatos()
    
    print("\n" + "=" * 70)
    print("✅ Todos los ejemplos completados")
    print("=" * 70)


if __name__ == '__main__':
    main()
