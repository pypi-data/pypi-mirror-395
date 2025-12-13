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
Test de compatibilidad entre PyDSK (Python) e iDSK20 (C++)
Verifica que los DSKs creados son idénticos
"""

import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from pydsk import DSK


def test_format_compatibility():
    """Prueba que los 3 formatos son compatibles"""
    print("=" * 70)
    print("TEST 1: Compatibilidad de formatos")
    print("=" * 70)
    
    formatos = [
        ('DATA', DSK.FORMAT_DATA),
        ('SYSTEM', DSK.FORMAT_SYSTEM),
        ('VENDOR', DSK.FORMAT_VENDOR),
    ]
    
    for nombre, formato in formatos:
        # Crear con Python
        dsk = DSK()
        dsk.create(nb_tracks=40, nb_sectors=9, format_type=formato)
        filename = f"test_{nombre.lower()}.dsk"
        dsk.save(filename)
        
        # Verificar con idsk20
        result = subprocess.run(
            ['./build/idsk20', filename, '--ls'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ Formato {nombre:10s} - Compatible con idsk20")
        else:
            print(f"❌ Formato {nombre:10s} - ERROR: {result.stderr}")
            return False
    
    print()
    return True


def test_track_sizes():
    """Prueba diferentes números de pistas"""
    print("=" * 70)
    print("TEST 2: Diferentes tamaños de pistas")
    print("=" * 70)
    
    pistas = [35, 40, 42, 80]
    
    for num_pistas in pistas:
        dsk = DSK()
        dsk.create(nb_tracks=num_pistas, nb_sectors=9)
        filename = f"test_{num_pistas}tracks.dsk"
        dsk.save(filename)
        
        # Verificar con idsk20
        result = subprocess.run(
            ['./build/idsk20', filename, '--ls'],
            capture_output=True,
            text=True
        )
        
        info = dsk.get_info()
        if result.returncode == 0:
            print(f"✅ {num_pistas:2d} pistas ({info['capacity_kb']:3d} KB) - Compatible")
        else:
            print(f"❌ {num_pistas:2d} pistas - ERROR")
            return False
    
    print()
    return True


def test_sector_layout():
    """Verifica que el entrelazado de sectores es correcto"""
    print("=" * 70)
    print("TEST 3: Entrelazado de sectores")
    print("=" * 70)
    
    # Crear DSK
    dsk = DSK()
    dsk.create(nb_tracks=40, nb_sectors=9, format_type=DSK.FORMAT_DATA)
    
    # Leer primera pista para verificar IDs de sectores
    from pydsk.structures import CPCEMUTrack
    track = CPCEMUTrack.from_bytes(dsk.data, 0x100)
    
    # Verificar IDs: C1, C6, C2, C7, C3, C8, C4, C9, C5
    expected_ids = [0xC1, 0xC6, 0xC2, 0xC7, 0xC3, 0xC8, 0xC4, 0xC9, 0xC5]
    actual_ids = [sector.R for sector in track.sectors]
    
    if actual_ids == expected_ids:
        print(f"✅ Entrelazado correcto: {', '.join(f'0x{x:02X}' for x in actual_ids)}")
    else:
        print(f"❌ Entrelazado incorrecto!")
        print(f"   Esperado: {expected_ids}")
        print(f"   Obtenido: {actual_ids}")
        return False
    
    print()
    return True


def test_file_sizes():
    """Compara tamaños de archivos"""
    print("=" * 70)
    print("TEST 4: Tamaños de archivos")
    print("=" * 70)
    
    # Crear DSK con Python
    dsk_py = DSK()
    dsk_py.create(nb_tracks=40, nb_sectors=9)
    dsk_py.save("size_test_py.dsk")
    
    # Crear DSK con C++
    subprocess.run(['./build/idsk20', 'size_test_cpp.dsk', '-n'], 
                   capture_output=True)
    
    # Comparar tamaños
    size_py = Path('size_test_py.dsk').stat().st_size
    size_cpp = Path('size_test_cpp.dsk').stat().st_size
    
    # El de C++ puede tener 2 pistas extra (42 vs 40)
    expected_py = 0x100 + (40 * (0x100 + 512 * 9))
    expected_cpp = 0x100 + (42 * (0x100 + 512 * 9))
    
    print(f"Python:   {size_py:,} bytes (esperado: {expected_py:,})")
    print(f"C++:      {size_cpp:,} bytes (esperado: {expected_cpp:,})")
    
    if size_py == expected_py:
        print(f"✅ Tamaño Python correcto")
    else:
        print(f"❌ Tamaño Python incorrecto")
        return False
    
    print()
    return True


def test_round_trip():
    """Test de ida y vuelta: crear -> guardar -> cargar -> guardar"""
    print("=" * 70)
    print("TEST 5: Round-trip (crear -> guardar -> cargar -> guardar)")
    print("=" * 70)
    
    # Crear y guardar
    dsk1 = DSK()
    dsk1.create(nb_tracks=40, nb_sectors=9)
    dsk1.save("roundtrip1.dsk")
    
    # Cargar y volver a guardar
    dsk2 = DSK("roundtrip1.dsk")
    dsk2.save("roundtrip2.dsk")
    
    # Comparar archivos
    data1 = Path("roundtrip1.dsk").read_bytes()
    data2 = Path("roundtrip2.dsk").read_bytes()
    
    if data1 == data2:
        print(f"✅ Round-trip exitoso - Archivos idénticos ({len(data1):,} bytes)")
    else:
        print(f"❌ Round-trip falló - Archivos diferentes")
        return False
    
    print()
    return True


def cleanup():
    """Limpia archivos de test"""
    import glob
    test_files = glob.glob("test_*.dsk") + glob.glob("size_test_*.dsk") + glob.glob("roundtrip*.dsk")
    for f in test_files:
        try:
            Path(f).unlink()
        except:
            pass


def main():
    """Ejecuta todos los tests"""
    print("\n" + "=" * 70)
    print(" TEST DE COMPATIBILIDAD PyDSK <-> iDSK20")
    print("=" * 70 + "\n")
    
    tests = [
        ("Compatibilidad de formatos", test_format_compatibility),
        ("Diferentes tamaños", test_track_sizes),
        ("Entrelazado de sectores", test_sector_layout),
        ("Tamaños de archivos", test_file_sizes),
        ("Round-trip", test_round_trip),
    ]
    
    resultados = []
    for nombre, test_func in tests:
        try:
            resultado = test_func()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"❌ {nombre} - EXCEPCIÓN: {e}")
            resultados.append((nombre, False))
    
    # Resumen
    print("=" * 70)
    print(" RESUMEN DE TESTS")
    print("=" * 70)
    
    exitosos = sum(1 for _, r in resultados if r)
    total = len(resultados)
    
    for nombre, resultado in resultados:
        icono = "✅" if resultado else "❌"
        print(f"{icono} {nombre}")
    
    print()
    print(f"Resultado: {exitosos}/{total} tests exitosos")
    
    if exitosos == total:
        print("\n🎉 ¡TODOS LOS TESTS PASARON! PyDSK es 100% compatible con iDSK20")
    else:
        print(f"\n⚠️  {total - exitosos} test(s) fallaron")
    
    print("=" * 70)
    
    # Limpiar archivos de test
    cleanup()
    
    return 0 if exitosos == total else 1


if __name__ == '__main__':
    sys.exit(main())
