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
Script de prueba directo - Sin wrapper CLI
Ejecuta directamente los métodos para ver errores originales
"""

import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from pydsk import DSK, DSKError

print("=" * 70)
print("PRUEBAS DIRECTAS - Errores originales sin wrapper")
print("=" * 70)

# Test 1: Archivo de entrada no existe
print("\n1. add_amsdos_header - Archivo de entrada no existe:")
print("-" * 70)
try:
    DSK.add_amsdos_header('no_existe.bin', 'output.bin')
except Exception as e:
    print(f"Tipo: {type(e).__name__}")
    print(f"Mensaje: {e}")

# Test 2: Archivo de salida ya existe (sin force)
print("\n2. add_amsdos_header - Archivo de salida existe (sin force):")
print("-" * 70)
try:
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        f.write(b"test data")
        temp_in = f.name
    
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        f.write(b"existing")
        temp_out = f.name
    
    DSK.add_amsdos_header(temp_in, temp_out, force=False)
except Exception as e:
    print(f"Tipo: {type(e).__name__}")
    print(f"Mensaje: {e}")
finally:
    os.unlink(temp_in)
    os.unlink(temp_out)

# Test 3: Archivo ya tiene cabecera AMSDOS
print("\n3. add_amsdos_header - Archivo ya tiene cabecera:")
print("-" * 70)
try:
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        f.write(b"test data")
        temp_in = f.name
    
    temp_with_header = temp_in + "_header.bin"
    
    # Primero añadimos cabecera
    DSK.add_amsdos_header(temp_in, temp_with_header, force=True)
    
    # Ahora intentamos añadir otra vez
    temp_out = temp_in + "_double.bin"
    DSK.add_amsdos_header(temp_with_header, temp_out)
except Exception as e:
    print(f"Tipo: {type(e).__name__}")
    print(f"Mensaje: {e}")
finally:
    try:
        os.unlink(temp_in)
        os.unlink(temp_with_header)
        if os.path.exists(temp_out):
            os.unlink(temp_out)
    except:
        pass

# Test 4: remove_amsdos_header - Archivo de entrada no existe
print("\n4. remove_amsdos_header - Archivo de entrada no existe:")
print("-" * 70)
try:
    DSK.remove_amsdos_header('no_existe.bin', 'output.bin')
except Exception as e:
    print(f"Tipo: {type(e).__name__}")
    print(f"Mensaje: {e}")

# Test 5: remove_amsdos_header - Archivo de salida existe (sin force)
print("\n5. remove_amsdos_header - Archivo de salida existe (sin force):")
print("-" * 70)
try:
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        f.write(b"x" * 200)
        temp_in = f.name
    
    # Añadir cabecera primero
    temp_with_header = temp_in + "_header.bin"
    DSK.add_amsdos_header(temp_in, temp_with_header, force=True)
    
    # Crear archivo de salida que ya existe
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        f.write(b"existing")
        temp_out = f.name
    
    DSK.remove_amsdos_header(temp_with_header, temp_out, force=False)
except Exception as e:
    print(f"Tipo: {type(e).__name__}")
    print(f"Mensaje: {e}")
finally:
    try:
        os.unlink(temp_in)
        os.unlink(temp_with_header)
        os.unlink(temp_out)
    except:
        pass

# Test 6: remove_amsdos_header - Archivo muy pequeño
print("\n6. remove_amsdos_header - Archivo demasiado pequeño:")
print("-" * 70)
try:
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        f.write(b"small")  # Solo 5 bytes
        temp_in = f.name
    
    temp_out = temp_in + "_out.bin"
    DSK.remove_amsdos_header(temp_in, temp_out)
except Exception as e:
    print(f"Tipo: {type(e).__name__}")
    print(f"Mensaje: {e}")
finally:
    os.unlink(temp_in)

# Test 7: remove_amsdos_header - Tipo de archivo incorrecto
print("\n7. remove_amsdos_header - Tipo de archivo incorrecto:")
print("-" * 70)
try:
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        # Crear 128 bytes pero con tipo incorrecto (0xFF en lugar de 0x00 o 0x16)
        header = bytearray(128)
        header[0] = 0xFF  # Tipo inválido
        f.write(header)
        f.write(b"data" * 50)
        temp_in = f.name
    
    temp_out = temp_in + "_out.bin"
    DSK.remove_amsdos_header(temp_in, temp_out)
except Exception as e:
    print(f"Tipo: {type(e).__name__}")
    print(f"Mensaje: {e}")
finally:
    os.unlink(temp_in)

# Test 8: remove_amsdos_header - Checksum incorrecto
print("\n8. remove_amsdos_header - Checksum incorrecto:")
print("-" * 70)
try:
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        # Crear cabecera con tipo válido pero checksum malo
        header = bytearray(128)
        header[0] = 0x16  # Tipo binario (válido)
        header[0x43] = 0xFF  # Checksum incorrecto
        header[0x44] = 0xFF
        f.write(header)
        f.write(b"data" * 50)
        temp_in = f.name
    
    temp_out = temp_in + "_out.bin"
    DSK.remove_amsdos_header(temp_in, temp_out)
except Exception as e:
    print(f"Tipo: {type(e).__name__}")
    print(f"Mensaje: {e}")
finally:
    os.unlink(temp_in)

# Test 9: add_amsdos_header - Verificar direcciones automáticas para BASIC
print("\n9. add_amsdos_header - Direcciones automáticas para BASIC (tipo 1):")
print("-" * 70)
try:
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bas') as f:
        f.write(b"10 PRINT \"TEST\"\n")
        temp_in = f.name
    
    temp_out = temp_in + "_header.bas"
    DSK.add_amsdos_header(temp_in, temp_out, load_addr=0, exec_addr=0, file_type=1, force=True)
    
    # Leer cabecera para verificar
    with open(temp_out, 'rb') as f:
        header = f.read(128)
        import struct
        load_addr = struct.unpack('<H', header[0x15:0x17])[0]
        exec_addr = struct.unpack('<H', header[0x1A:0x1C])[0]
        print(f"OK - Load: &{load_addr:04X}, Exec: &{exec_addr:04X}")
        if load_addr == 0x0170:
            print("✓ Dirección automática correcta para BASIC")
        else:
            print(f"✗ ERROR: Esperaba 0x0170, obtuvo 0x{load_addr:04X}")
except Exception as e:
    print(f"Tipo: {type(e).__name__}")
    print(f"Mensaje: {e}")
finally:
    try:
        os.unlink(temp_in)
        os.unlink(temp_out)
    except:
        pass

# Test 10: add_amsdos_header - Verificar direcciones automáticas para BASIC ASCII
print("\n10. add_amsdos_header - Direcciones automáticas para BASIC ASCII (tipo 2):")
print("-" * 70)
try:
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bas') as f:
        f.write(b"10 PRINT \"TEST\"\n")
        temp_in = f.name
    
    temp_out = temp_in + "_header.bas"
    DSK.add_amsdos_header(temp_in, temp_out, load_addr=0, exec_addr=0, file_type=2, force=True)
    
    # Leer cabecera para verificar
    with open(temp_out, 'rb') as f:
        header = f.read(128)
        import struct
        load_addr = struct.unpack('<H', header[0x15:0x17])[0]
        exec_addr = struct.unpack('<H', header[0x1A:0x1C])[0]
        print(f"OK - Load: &{load_addr:04X}, Exec: &{exec_addr:04X}")
        if load_addr == 0x0170:
            print("✓ Dirección automática correcta para BASIC ASCII")
        else:
            print(f"✗ ERROR: Esperaba 0x0170, obtuvo 0x{load_addr:04X}")
except Exception as e:
    print(f"Tipo: {type(e).__name__}")
    print(f"Mensaje: {e}")
finally:
    try:
        os.unlink(temp_in)
        os.unlink(temp_out)
    except:
        pass

# Test 11: add_amsdos_header - Verificar direcciones automáticas para binario
print("\n11. add_amsdos_header - Direcciones automáticas para binario (tipo 0):")
print("-" * 70)
try:
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
        f.write(b"\x00\x00\xC9")
        temp_in = f.name
    
    temp_out = temp_in + "_header.bin"
    DSK.add_amsdos_header(temp_in, temp_out, load_addr=0, exec_addr=0, file_type=0, force=True)
    
    # Leer cabecera para verificar
    with open(temp_out, 'rb') as f:
        header = f.read(128)
        import struct
        load_addr = struct.unpack('<H', header[0x15:0x17])[0]
        exec_addr = struct.unpack('<H', header[0x1A:0x1C])[0]
        print(f"OK - Load: &{load_addr:04X}, Exec: &{exec_addr:04X}")
        if load_addr == 0x4000:
            print("✓ Dirección automática correcta para binario")
        else:
            print(f"✗ ERROR: Esperaba 0x4000, obtuvo 0x{load_addr:04X}")
except Exception as e:
    print(f"Tipo: {type(e).__name__}")
    print(f"Mensaje: {e}")
finally:
    try:
        os.unlink(temp_in)
        os.unlink(temp_out)
    except:
        pass

print("\n" + "=" * 70)
print("PRUEBAS COMPLETADAS")
print("=" * 70)
