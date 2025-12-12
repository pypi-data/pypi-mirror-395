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
PyDSK - Ejemplos de eliminación de archivos
============================================

Ejemplos prácticos de cómo eliminar archivos de imágenes DSK
usando la librería PyDSK.

Autor: PyDSK
Fecha: 2025
"""

import sys
import os
import tempfile
from pathlib import Path

# Agregar path para importar pydsk
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pydsk.dsk import DSK


def separador(titulo):
    """Imprime un separador visual"""
    print("\n" + "="*70)
    print(f"  {titulo}")
    print("="*70 + "\n")


def ejemplo_eliminar_simple():
    """
    Ejemplo 1: Eliminar archivo básico
    -----------------------------------
    Elimina un archivo marcando su entrada como borrada (0xE5).
    """
    separador("Ejemplo 1: Eliminar archivo simple")
    
    with tempfile.NamedTemporaryFile(suffix='.dsk', delete=False) as tmp:
        dsk_path = tmp.name
    
    try:
        # Crear DSK con archivos de prueba
        dsk = DSK()
        dsk.create()
        
        # Crear archivos
        files_data = [
            ("FILE1.BAS", b"10 PRINT \"File 1\"\n"),
            ("FILE2.BAS", b"10 PRINT \"File 2\"\n"),
            ("FILE3.BAS", b"10 PRINT \"File 3\"\n"),
        ]
        
        for filename, data in files_data:
            src = os.path.join(tempfile.gettempdir(), filename)
            with open(src, 'wb') as f:
                f.write(data)
            dsk.write_file(src, file_type=2, dsk_filename=filename)
            os.unlink(src)
        
        dsk.save(dsk_path)
        
        print("📁 Archivos originales:")
        entries = dsk.get_directory_entries()
        for entry in entries:
            if not entry.is_deleted and entry.num_page == 0:
                print(f"   {entry.full_name}")
        
        # Eliminar FILE2.BAS
        print("\n🗑️  Eliminando: FILE2.BAS")
        extents = dsk.delete_file("FILE2.BAS")
        print(f"   ✅ {extents} extent(s) eliminado(s)")
        dsk.save(dsk_path)
        
        # Verificar
        dsk = DSK(dsk_path)
        print("\n✅ Archivos después de eliminar:")
        entries = dsk.get_directory_entries()
        for entry in entries:
            if not entry.is_deleted and entry.num_page == 0:
                print(f"   {entry.full_name}")
        
        print(f"\n💡 El archivo FILE2.BAS ya no aparece en el directorio")
        
    finally:
        if os.path.exists(dsk_path):
            os.unlink(dsk_path)


def ejemplo_eliminar_multiples():
    """
    Ejemplo 2: Eliminar múltiples archivos
    ---------------------------------------
    Elimina varios archivos de una vez.
    """
    separador("Ejemplo 2: Eliminar múltiples archivos")
    
    with tempfile.NamedTemporaryFile(suffix='.dsk', delete=False) as tmp:
        dsk_path = tmp.name
    
    try:
        # Crear DSK con varios archivos
        dsk = DSK()
        dsk.create()
        
        # Crear 10 archivos
        print("📁 Creando 10 archivos de prueba...")
        for i in range(1, 11):
            filename = f"FILE{i:02d}.BAS"
            data = f"10 PRINT \"File {i}\"\n".encode()
            src = os.path.join(tempfile.gettempdir(), filename)
            with open(src, 'wb') as f:
                f.write(data)
            dsk.write_file(src, file_type=2, dsk_filename=filename)
            os.unlink(src)
        
        dsk.save(dsk_path)
        
        print("   ✅ 10 archivos creados")
        
        # Listar
        dsk = DSK(dsk_path)
        entries = dsk.get_directory_entries()
        count_before = sum(1 for e in entries if not e.is_deleted and e.num_page == 0)
        print(f"\n📊 Total de archivos: {count_before}")
        
        # Eliminar archivos pares
        print("\n🗑️  Eliminando archivos pares (FILE02, FILE04, FILE06, ...):")
        files_to_delete = [f"FILE{i:02d}.BAS" for i in range(2, 11, 2)]
        
        deleted_total = 0
        for filename in files_to_delete:
            extents = dsk.delete_file(filename)
            deleted_total += 1
            print(f"   ✅ {filename} eliminado")
        
        dsk.save(dsk_path)
        
        # Verificar
        dsk = DSK(dsk_path)
        print(f"\n✅ {deleted_total} archivo(s) eliminado(s)")
        
        print("\n📁 Archivos restantes:")
        entries = dsk.get_directory_entries()
        for entry in entries:
            if not entry.is_deleted and entry.num_page == 0:
                print(f"   {entry.full_name}")
        
        count_after = sum(1 for e in entries if not e.is_deleted and e.num_page == 0)
        print(f"\n📊 Total restante: {count_after} archivos")
        
    finally:
        if os.path.exists(dsk_path):
            os.unlink(dsk_path)


def ejemplo_eliminar_con_extents():
    """
    Ejemplo 3: Eliminar archivo con múltiples extents
    --------------------------------------------------
    Archivos grandes tienen múltiples entradas de directorio.
    """
    separador("Ejemplo 3: Eliminar archivo con múltiples extents")
    
    with tempfile.NamedTemporaryFile(suffix='.dsk', delete=False) as tmp:
        dsk_path = tmp.name
    
    try:
        # Crear DSK
        dsk = DSK()
        dsk.create()
        
        # Crear archivo pequeño
        small_data = b"Small file" * 100
        small_file = os.path.join(tempfile.gettempdir(), "SMALL.BIN")
        with open(small_file, 'wb') as f:
            f.write(small_data)
        
        # Crear archivo grande (> 16 KB)
        large_data = b'\x00' * (20 * 1024)
        large_file = os.path.join(tempfile.gettempdir(), "LARGE.BIN")
        with open(large_file, 'wb') as f:
            f.write(large_data)
        
        # Importar ambos
        dsk.write_file(small_file, file_type=0, load_addr=0x4000)
        dsk.write_file(large_file, file_type=0, load_addr=0x8000)
        dsk.save(dsk_path)
        
        # Analizar extents
        dsk = DSK(dsk_path)
        entries = dsk.get_directory_entries()
        
        print("📁 Archivos en el DSK:")
        small_extents = [e for e in entries if not e.is_deleted and e.name == "SMALL"]
        large_extents = [e for e in entries if not e.is_deleted and e.name == "LARGE"]
        
        print(f"\n   SMALL.BIN:")
        print(f"      Tamaño: {len(small_data)} bytes")
        print(f"      Extents: {len(small_extents)}")
        
        print(f"\n   LARGE.BIN:")
        print(f"      Tamaño: {len(large_data)} bytes")
        print(f"      Extents: {len(large_extents)}")
        
        # Eliminar archivo grande
        print(f"\n🗑️  Eliminando LARGE.BIN...")
        extents_deleted = dsk.delete_file("LARGE.BIN")
        print(f"   ✅ {extents_deleted} extent(s) eliminado(s)")
        dsk.save(dsk_path)
        
        # Verificar que todos los extents fueron eliminados
        dsk = DSK(dsk_path)
        entries = dsk.get_directory_entries()
        remaining_large = [e for e in entries if not e.is_deleted and e.name == "LARGE"]
        
        if remaining_large:
            print(f"\n   ❌ ERROR: Quedaron {len(remaining_large)} extents sin eliminar")
        else:
            print(f"\n   ✅ Todos los extents fueron eliminados correctamente")
        
        print("\n📁 Archivos restantes:")
        for entry in entries:
            if not entry.is_deleted and entry.num_page == 0:
                print(f"   {entry.full_name}")
        
        # Limpiar
        os.unlink(small_file)
        os.unlink(large_file)
        
    finally:
        if os.path.exists(dsk_path):
            os.unlink(dsk_path)


def ejemplo_validaciones():
    """
    Ejemplo 4: Validaciones al eliminar
    ------------------------------------
    Prueba las validaciones al intentar eliminar archivos.
    """
    separador("Ejemplo 4: Validaciones al eliminar")
    
    with tempfile.NamedTemporaryFile(suffix='.dsk', delete=False) as tmp:
        dsk_path = tmp.name
    
    try:
        # Crear DSK con un archivo
        dsk = DSK()
        dsk.create()
        
        data = b"10 PRINT \"Test\"\n"
        src = os.path.join(tempfile.gettempdir(), "TEST.BAS")
        with open(src, 'wb') as f:
            f.write(data)
        dsk.write_file(src, file_type=2)
        dsk.save(dsk_path)
        os.unlink(src)
        
        print("📁 Archivo en el DSK:")
        entries = dsk.get_directory_entries()
        for entry in entries:
            if not entry.is_deleted and entry.num_page == 0:
                print(f"   {entry.full_name}")
        
        # Intento 1: Eliminar archivo que no existe
        print("\n⚠️  Intento 1: Eliminar archivo inexistente")
        try:
            dsk.delete_file("NOEXISTE.BAS")
            print("   ❌ Debería haber fallado")
        except Exception as e:
            print(f"   ✅ Error esperado: {e}")
        
        # Intento 2: Eliminar archivo válido
        print("\n✅ Intento 2: Eliminar archivo válido")
        extents = dsk.delete_file("TEST.BAS")
        print(f"   ✅ Archivo eliminado ({extents} extents)")
        dsk.save(dsk_path)
        
        # Intento 3: Intentar eliminar el mismo archivo de nuevo
        print("\n⚠️  Intento 3: Eliminar archivo ya eliminado")
        dsk = DSK(dsk_path)
        try:
            dsk.delete_file("TEST.BAS")
            print("   ❌ Debería haber fallado")
        except Exception as e:
            print(f"   ✅ Error esperado: {e}")
        
        # Verificar que el DSK está vacío
        print("\n📁 Directorio final:")
        entries = dsk.get_directory_entries()
        active_files = [e for e in entries if not e.is_deleted and e.num_page == 0]
        if not active_files:
            print("   (vacío)")
        else:
            for entry in active_files:
                print(f"   {entry.full_name}")
        
    finally:
        if os.path.exists(dsk_path):
            os.unlink(dsk_path)


def ejemplo_usuario_especifico():
    """
    Ejemplo 5: Eliminar en área de usuario específica
    --------------------------------------------------
    Los archivos en diferentes usuarios son independientes.
    """
    separador("Ejemplo 5: Eliminar en área de usuario específica")
    
    with tempfile.NamedTemporaryFile(suffix='.dsk', delete=False) as tmp:
        dsk_path = tmp.name
    
    try:
        # Crear DSK con archivos en diferentes usuarios
        dsk = DSK()
        dsk.create()
        
        data = b"10 PRINT \"Test\"\n"
        src = os.path.join(tempfile.gettempdir(), "FILE.BAS")
        with open(src, 'wb') as f:
            f.write(data)
        
        # Importar en usuarios 0, 5 y 10
        # Usamos nombres temporales diferentes ya que write_file no verifica por usuario
        dsk.write_file(src, file_type=2, user=0, dsk_filename="FILE.BAS")
        dsk.write_file(src, file_type=2, user=5, dsk_filename="FILEU5.BAS")
        dsk.write_file(src, file_type=2, user=10, dsk_filename="FILEU10.BAS")
        dsk.save(dsk_path)
        
        # Renombrar para que todos tengan el mismo nombre
        dsk.rename_file("FILEU5.BAS", "FILE.BAS", user=5)
        dsk.rename_file("FILEU10.BAS", "FILE.BAS", user=10)
        dsk.save(dsk_path)
        os.unlink(src)
        
        print("📁 Archivos originales:")
        entries = dsk.get_directory_entries()
        for entry in entries:
            if not entry.is_deleted and entry.num_page == 0:
                print(f"   Usuario {entry.user:2d}: {entry.full_name}")
        
        # Eliminar solo en usuario 5
        print("\n🗑️  Eliminando FILE.BAS en usuario 5")
        extents = dsk.delete_file("FILE.BAS", user=5)
        print(f"   ✅ {extents} extent(s) eliminado(s)")
        dsk.save(dsk_path)
        
        # Verificar que solo se eliminó en usuario 5
        dsk = DSK(dsk_path)
        print("\n✅ Archivos después de eliminar:")
        entries = dsk.get_directory_entries()
        for entry in entries:
            if not entry.is_deleted and entry.num_page == 0:
                print(f"   Usuario {entry.user:2d}: {entry.full_name}")
        
        print("\n💡 Los archivos en usuarios 0 y 10 no fueron modificados")
        
    finally:
        if os.path.exists(dsk_path):
            os.unlink(dsk_path)


def ejemplo_ciclo_completo():
    """
    Ejemplo 6: Ciclo completo con gestión de archivos
    --------------------------------------------------
    Crear → Importar → Renombrar → Listar → Eliminar
    """
    separador("Ejemplo 6: Ciclo completo con eliminación")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        dsk_path = os.path.join(tmpdir, "project.dsk")
        
        # 1. Crear DSK
        print("1️⃣  Creando DSK...")
        dsk = DSK()
        dsk.create()
        dsk.save(dsk_path)
        
        # 2. Importar archivos
        print("\n2️⃣  Importando archivos de proyecto...")
        project_files = [
            ("MAIN.BAS", b"10 REM Main program\n"),
            ("UTILS.BAS", b"10 REM Utilities\n"),
            ("CONFIG.DAT", b"CONFIG=123"),
            ("TEMP1.TMP", b"Temporary file 1"),
            ("TEMP2.TMP", b"Temporary file 2"),
            ("README.TXT", b"Project README"),
        ]
        
        for filename, data in project_files:
            src = os.path.join(tmpdir, filename)
            with open(src, 'wb') as f:
                f.write(data)
            
            file_type = 2 if filename.endswith('.BAS') else 0
            dsk.write_file(src, file_type=file_type)
        
        dsk.save(dsk_path)
        print(f"   ✅ {len(project_files)} archivos importados")
        
        # 3. Listar archivos
        print("\n3️⃣  Archivos en el proyecto:")
        dsk = DSK(dsk_path)
        entries = dsk.get_directory_entries()
        for entry in entries:
            if not entry.is_deleted and entry.num_page == 0:
                print(f"   - {entry.full_name}")
        
        # 4. Eliminar archivos temporales
        print("\n4️⃣  Limpiando archivos temporales (.TMP)...")
        temp_files = ["TEMP1.TMP", "TEMP2.TMP"]
        
        for filename in temp_files:
            dsk.delete_file(filename)
            print(f"   ✅ {filename} eliminado")
        
        dsk.save(dsk_path)
        
        # 5. Listar archivos finales
        print("\n5️⃣  Archivos después de limpiar:")
        dsk = DSK(dsk_path)
        entries = dsk.get_directory_entries()
        final_count = 0
        for entry in entries:
            if not entry.is_deleted and entry.num_page == 0:
                print(f"   - {entry.full_name}")
                final_count += 1
        
        # 6. Mostrar espacio
        print(f"\n6️⃣  Estadísticas:")
        print(f"   Archivos originales: {len(project_files)}")
        print(f"   Archivos eliminados: {len(temp_files)}")
        print(f"   Archivos finales: {final_count}")
        print(f"   Espacio libre: {dsk.get_free_space()} KB")
        
        print(f"\n✅ Ciclo completo finalizado")


def main():
    """Ejecuta todos los ejemplos"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║              PyDSK - Ejemplos de Eliminación de Archivos             ║
║                                                                      ║
║  Demostraciones prácticas de eliminación de archivos en DSK         ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        ejemplo_eliminar_simple()
        ejemplo_eliminar_multiples()
        ejemplo_eliminar_con_extents()
        ejemplo_validaciones()
        ejemplo_usuario_especifico()
        ejemplo_ciclo_completo()
        
        print("\n" + "="*70)
        print("✅ Todos los ejemplos completados exitosamente")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error ejecutando ejemplos: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
