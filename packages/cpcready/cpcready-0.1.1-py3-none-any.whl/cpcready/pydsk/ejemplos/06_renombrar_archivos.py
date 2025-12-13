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
PyDSK - Ejemplos de renombrado de archivos
==========================================

Ejemplos prácticos de cómo renombrar archivos en imágenes DSK
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


def ejemplo_renombrar_simple():
    """
    Ejemplo 1: Renombrar archivo básico
    ------------------------------------
    Renombra un archivo cambiando su nombre y/o extensión.
    """
    separador("Ejemplo 1: Renombrar archivo simple")
    
    # Crear DSK temporal
    with tempfile.NamedTemporaryFile(suffix='.dsk', delete=False) as tmp:
        dsk_path = tmp.name
    
    try:
        # Crear DSK e importar archivo de prueba
        dsk = DSK()
        dsk.create()
        
        # Crear archivo de prueba
        test_data = b"PRINT \"Programa original\"\n"
        with tempfile.NamedTemporaryFile(suffix='.bas', delete=False) as tmp_file:
            tmp_file.write(test_data)
            src_file = tmp_file.name
        
        # Importar
        dsk.write_file(src_file, file_type=2)  # BASIC ASCII
        dsk.save(dsk_path)
        
        print("📁 Archivo original:")
        entries = dsk.get_directory_entries()
        old_name = None
        for entry in entries:
            if not entry.is_deleted and entry.num_page == 0:
                old_name = entry.full_name.replace(' ', '').strip()
                print(f"   {old_name}")
                break
        
        # Renombrar
        new_name = "PROGRAM.BAS"
        
        print(f"\n🔄 Renombrando: {old_name} → {new_name}")
        dsk.rename_file(old_name, new_name)
        dsk.save(dsk_path)
        
        # Verificar
        dsk = DSK(dsk_path)
        print("\n✅ Directorio después del renombrado:")
        entries = dsk.get_directory_entries()
        for entry in entries:
            if not entry.is_deleted and entry.num_page == 0:
                print(f"   {entry.full_name}")
        
        # Limpiar
        os.unlink(src_file)
        
    finally:
        if os.path.exists(dsk_path):
            os.unlink(dsk_path)


def ejemplo_validaciones():
    """
    Ejemplo 2: Validaciones de renombrado
    --------------------------------------
    Prueba las validaciones al renombrar archivos.
    """
    separador("Ejemplo 2: Validaciones de renombrado")
    
    with tempfile.NamedTemporaryFile(suffix='.dsk', delete=False) as tmp:
        dsk_path = tmp.name
    
    try:
        # Crear DSK con dos archivos
        dsk = DSK()
        dsk.create()
        
        # Crear dos archivos
        data1 = b"10 PRINT \"FILE1\"\n"
        data2 = b"10 PRINT \"FILE2\"\n"
        
        with tempfile.NamedTemporaryFile(suffix='.bas', delete=False) as tmp1:
            tmp1.write(data1)
            file1 = tmp1.name
        
        with tempfile.NamedTemporaryFile(suffix='.bas', delete=False) as tmp2:
            tmp2.write(data2)
            file2 = tmp2.name
        
        dsk.write_file(file1, file_type=2, dsk_filename="FILE1.BAS")
        dsk.write_file(file2, file_type=2, dsk_filename="FILE2.BAS")
        dsk.save(dsk_path)
        
        print("📁 Archivos en el DSK:")
        entries = dsk.get_directory_entries()
        for entry in entries:
            if not entry.is_deleted and entry.num_page == 0:
                print(f"   {entry.full_name}")
        
        # Intento 1: Renombrar archivo que no existe
        print("\n⚠️  Intento 1: Renombrar archivo inexistente")
        try:
            dsk.rename_file("NOEXISTE.BAS", "NUEVO.BAS")
            print("   ❌ Debería haber fallado")
        except Exception as e:
            print(f"   ✅ Error esperado: {e}")
        
        # Intento 2: Renombrar a nombre que ya existe
        print("\n⚠️  Intento 2: Renombrar a nombre existente")
        try:
            dsk.rename_file("FILE1.BAS", "FILE2.BAS")
            print("   ❌ Debería haber fallado")
        except Exception as e:
            print(f"   ✅ Error esperado: {e}")
        
        # Intento 3: Nombre inválido (más de un punto)
        print("\n⚠️  Intento 3: Nombre inválido")
        try:
            dsk.rename_file("FILE1.BAS", "FILE.NAME.BAS")
            print("   ❌ Debería haber fallado")
        except Exception as e:
            print(f"   ✅ Error esperado: {e}")
        
        # Intento 4: Renombrado válido
        print("\n✅ Intento 4: Renombrado válido")
        dsk.rename_file("FILE1.BAS", "RENAMED.BAS")
        dsk.save(dsk_path)
        
        dsk = DSK(dsk_path)
        print("   Archivos después del renombrado:")
        entries = dsk.get_directory_entries()
        for entry in entries:
            if not entry.is_deleted and entry.num_page == 0:
                print(f"   - {entry.full_name}")
        
        # Limpiar
        os.unlink(file1)
        os.unlink(file2)
        
    finally:
        if os.path.exists(dsk_path):
            os.unlink(dsk_path)


def ejemplo_cambiar_extension():
    """
    Ejemplo 3: Cambiar solo la extensión
    -------------------------------------
    Renombra un archivo manteniendo el nombre pero cambiando la extensión.
    """
    separador("Ejemplo 3: Cambiar solo la extensión")
    
    with tempfile.NamedTemporaryFile(suffix='.dsk', delete=False) as tmp:
        dsk_path = tmp.name
    
    try:
        # Crear DSK con archivo
        dsk = DSK()
        dsk.create()
        
        data = b"10 PRINT \"Testing\"\n20 END\n"
        with tempfile.NamedTemporaryFile(suffix='.bas', delete=False) as tmp_file:
            tmp_file.write(data)
            src_file = tmp_file.name
        
        dsk.write_file(src_file, file_type=2, dsk_filename="PROGRAM.BAS")
        dsk.save(dsk_path)
        
        print("📁 Archivo original:")
        entries = dsk.get_directory_entries()
        for entry in entries:
            if not entry.is_deleted and entry.num_page == 0:
                print(f"   {entry.full_name}")
        
        # Cambiar extensión .BAS → .BAK
        print("\n🔄 Cambiando extensión: PROGRAM.BAS → PROGRAM.BAK")
        dsk.rename_file("PROGRAM.BAS", "PROGRAM.BAK")
        dsk.save(dsk_path)
        
        # Verificar
        dsk = DSK(dsk_path)
        print("\n✅ Después del cambio:")
        entries = dsk.get_directory_entries()
        for entry in entries:
            if not entry.is_deleted and entry.num_page == 0:
                print(f"   {entry.full_name}")
        
        # Cambiar a archivo sin extensión
        print("\n🔄 Cambiando a sin extensión: PROGRAM.BAK → PROGRAM")
        dsk.rename_file("PROGRAM.BAK", "PROGRAM")
        dsk.save(dsk_path)
        
        dsk = DSK(dsk_path)
        print("\n✅ Archivo sin extensión:")
        entries = dsk.get_directory_entries()
        for entry in entries:
            if not entry.is_deleted and entry.num_page == 0:
                name = entry.full_name if entry.ext else entry.name
                print(f"   {name}")
        
        # Limpiar
        os.unlink(src_file)
        
    finally:
        if os.path.exists(dsk_path):
            os.unlink(dsk_path)


def ejemplo_multiples_extents():
    """
    Ejemplo 4: Renombrar archivo con múltiples extents
    ---------------------------------------------------
    Archivos grandes ocupan múltiples entradas de directorio (extents).
    El renombrado debe actualizar todas las entradas.
    """
    separador("Ejemplo 4: Renombrar archivo con múltiples extents")
    
    with tempfile.NamedTemporaryFile(suffix='.dsk', delete=False) as tmp:
        dsk_path = tmp.name
    
    try:
        # Crear DSK
        dsk = DSK()
        dsk.create()
        
        # Crear archivo grande (> 16 KB para tener múltiples extents)
        # Un extent puede contener máximo 16 bloques × 1KB = 16KB
        large_data = b'\x00' * (20 * 1024)  # 20 KB
        
        with tempfile.NamedTemporaryFile(suffix='.bin', delete=False) as tmp_file:
            tmp_file.write(large_data)
            src_file = tmp_file.name
        
        # Importar archivo grande
        dsk.write_file(src_file, file_type=0, load_addr=0x4000, dsk_filename="BIGFILE.BIN")
        dsk.save(dsk_path)
        
        # Contar extents del archivo
        dsk = DSK(dsk_path)
        entries = dsk.get_directory_entries()
        extents = [e for e in entries if not e.is_deleted and e.name == "BIGFILE"]
        
        print(f"📁 Archivo original: BIGFILE.BIN")
        print(f"   Tamaño: {len(large_data)} bytes")
        print(f"   Extents: {len(extents)}")
        print(f"   Páginas por extent:")
        for i, ext in enumerate(extents):
            print(f"      Extent {i} (página {ext.num_page}): {ext.nb_pages} bloques")
        
        # Renombrar
        print(f"\n🔄 Renombrando: BIGFILE.BIN → RENAMED.BIN")
        dsk.rename_file("BIGFILE.BIN", "RENAMED.BIN")
        dsk.save(dsk_path)
        
        # Verificar que todos los extents fueron renombrados
        dsk = DSK(dsk_path)
        entries = dsk.get_directory_entries()
        renamed_extents = [e for e in entries if not e.is_deleted and e.name == "RENAMED"]
        
        print(f"\n✅ Archivo renombrado: RENAMED.BIN")
        print(f"   Extents renombrados: {len(renamed_extents)}")
        print(f"   Páginas por extent:")
        for i, ext in enumerate(renamed_extents):
            print(f"      Extent {i} (página {ext.num_page}): {ext.nb_pages} bloques")
        
        # Verificar que no quedaron extents con el nombre antiguo
        old_extents = [e for e in entries if not e.is_deleted and e.name == "BIGFILE"]
        if old_extents:
            print(f"\n❌ ERROR: Quedaron {len(old_extents)} extents sin renombrar")
        else:
            print(f"\n✅ Todos los extents fueron renombrados correctamente")
        
        # Limpiar
        os.unlink(src_file)
        
    finally:
        if os.path.exists(dsk_path):
            os.unlink(dsk_path)


def ejemplo_usuario_especifico():
    """
    Ejemplo 5: Renombrar en área de usuario específica
    ---------------------------------------------------
    Los archivos pueden estar en diferentes áreas de usuario (0-15).
    """
    separador("Ejemplo 5: Renombrar en área de usuario específica")
    
    with tempfile.NamedTemporaryFile(suffix='.dsk', delete=False) as tmp:
        dsk_path = tmp.name
    
    try:
        # Crear DSK con archivos en diferentes usuarios
        dsk = DSK()
        dsk.create()
        
        data = b"10 PRINT \"Test\"\n"
        with tempfile.NamedTemporaryFile(suffix='.bas', delete=False) as tmp_file:
            tmp_file.write(data)
            src_file = tmp_file.name
        
        # Importar mismo archivo en usuarios 0 y 10
        dsk.write_file(src_file, file_type=2, user=0, dsk_filename="FILE.BAS")
        # Note: Como write_file no verifica por usuario, usamos nombres diferentes temporalmente
        dsk.write_file(src_file, file_type=2, user=10, dsk_filename="FILEU10.BAS")
        dsk.save(dsk_path)
        
        # Renombrar el archivo en usuario 10 para que tenga el mismo nombre
        dsk.rename_file("FILEU10.BAS", "FILE.BAS", user=10)
        dsk.save(dsk_path)
        
        print("📁 Archivos originales:")
        entries = dsk.get_directory_entries()
        for entry in entries:
            if not entry.is_deleted and entry.num_page == 0:
                print(f"   Usuario {entry.user:2d}: {entry.full_name}")
        
        # Renombrar solo en usuario 10
        print("\n🔄 Renombrando en usuario 10: FILE.BAS → RENAMED.BAS")
        dsk.rename_file("FILE.BAS", "RENAMED.BAS", user=10)
        dsk.save(dsk_path)
        
        # Verificar que solo se renombró en usuario 10
        dsk = DSK(dsk_path)
        print("\n✅ Después del renombrado:")
        entries = dsk.get_directory_entries()
        for entry in entries:
            if not entry.is_deleted and entry.num_page == 0:
                print(f"   Usuario {entry.user:2d}: {entry.full_name}")
        
        print("\n💡 Nota: El archivo en usuario 0 no fue modificado")
        
        # Limpiar
        os.unlink(src_file)
        
    finally:
        if os.path.exists(dsk_path):
            os.unlink(dsk_path)


def ejemplo_ciclo_completo():
    """
    Ejemplo 6: Ciclo completo de gestión de archivos
    -------------------------------------------------
    Crear → Importar → Renombrar → Exportar
    """
    separador("Ejemplo 6: Ciclo completo con renombrado")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        dsk_path = os.path.join(tmpdir, "test.dsk")
        
        # 1. Crear DSK
        print("1️⃣  Creando DSK vacío...")
        dsk = DSK()
        dsk.create()
        dsk.save(dsk_path)
        print(f"   ✅ DSK creado: {dsk_path}")
        
        # 2. Importar archivos
        print("\n2️⃣  Importando archivos...")
        files_to_import = [
            ("VERSION1.BAS", b"10 PRINT \"Version 1.0\"\n"),
            ("MAIN.BAS", b"10 REM Main program\n20 PRINT \"Running...\"\n"),
            ("UTILS.BIN", bytes(range(256)))
        ]
        
        for filename, data in files_to_import:
            src = os.path.join(tmpdir, filename)
            with open(src, 'wb') as f:
                f.write(data)
            
            file_type = 2 if filename.endswith('.BAS') else 0
            dsk.write_file(src, file_type=file_type)
            print(f"   ✅ Importado: {filename}")
        
        dsk.save(dsk_path)
        
        # 3. Listar archivos
        print("\n3️⃣  Archivos en el DSK:")
        dsk = DSK(dsk_path)
        entries = dsk.get_directory_entries()
        for entry in entries:
            if not entry.is_deleted and entry.num_page == 0:
                print(f"   - {entry.full_name}")
        
        # 4. Renombrar archivos
        print("\n4️⃣  Renombrando archivos...")
        renames = [
            ("VERSION1.BAS", "VERSION2.BAS"),
            ("UTILS.BIN", "HELPERS.BIN")
        ]
        
        for old, new in renames:
            dsk.rename_file(old, new)
            print(f"   ✅ {old} → {new}")
        
        dsk.save(dsk_path)
        
        # 5. Listar después de renombrar
        print("\n5️⃣  Archivos después de renombrar:")
        dsk = DSK(dsk_path)
        entries = dsk.get_directory_entries()
        for entry in entries:
            if not entry.is_deleted and entry.num_page == 0:
                print(f"   - {entry.full_name}")
        
        # 6. Exportar archivos renombrados
        print("\n6️⃣  Exportando archivos renombrados...")
        export_dir = os.path.join(tmpdir, "exported")
        exported = dsk.export_all(export_dir, keep_header=False)
        
        for filename in exported:
            export_path = os.path.join(export_dir, filename)
            size = os.path.getsize(export_path)
            print(f"   ✅ {filename} ({size} bytes)")
        
        print(f"\n✅ Ciclo completo finalizado")
        print(f"   DSK: {dsk_path}")
        print(f"   Exportados: {export_dir}")


def main():
    """Ejecuta todos los ejemplos"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║              PyDSK - Ejemplos de Renombrado de Archivos              ║
║                                                                      ║
║  Demostraciones prácticas de renombrado de archivos en DSK          ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        ejemplo_renombrar_simple()
        ejemplo_validaciones()
        ejemplo_cambiar_extension()
        ejemplo_multiples_extents()
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
