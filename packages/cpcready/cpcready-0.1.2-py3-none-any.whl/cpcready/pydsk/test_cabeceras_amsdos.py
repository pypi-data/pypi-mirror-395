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
Test completo de gestión de cabeceras AMSDOS - Casos de error
==============================================================

Este script prueba todos los posibles errores y casos extremos
de las funcionalidades add_amsdos_header() y remove_amsdos_header()
"""

import sys
import os
import tempfile
from pathlib import Path

# Añadir PyDSK al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pydsk import DSK, DSKError


def print_test(title: str):
    """Imprime encabezado de test"""
    print("\n" + "=" * 70)
    print(f"TEST: {title}")
    print("=" * 70)


def print_result(success: bool, message: str):
    """Imprime resultado de test"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status}: {message}\n")


# ============================================================================
# TESTS DE add_amsdos_header()
# ============================================================================

def test_add_header_archivo_no_existe():
    """Error: Archivo de entrada no existe"""
    print_test("add_amsdos_header() - Archivo de entrada no existe")
    
    try:
        DSK.add_amsdos_header(
            'archivo_que_no_existe.bin',
            'output.bin',
            load_addr=0x4000,
            exec_addr=0x4000,
            file_type=0
        )
        print_result(False, "No lanzó FileNotFoundError")
    except FileNotFoundError as e:
        print_result(True, f"FileNotFoundError capturado: {e}")
    except Exception as e:
        print_result(False, f"Error inesperado: {type(e).__name__}: {e}")


def test_add_header_archivo_salida_existe():
    """Error: Archivo de salida ya existe (sin force)"""
    print_test("add_amsdos_header() - Archivo de salida existe (sin force)")
    
    try:
        # Crear archivo de entrada
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            f.write(b'\x00' * 100)
            input_file = f.name
        
        # Crear archivo de salida que ya existe
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            f.write(b'\xFF' * 50)
            output_file = f.name
        
        try:
            DSK.add_amsdos_header(
                input_file,
                output_file,
                load_addr=0x4000,
                exec_addr=0x4000,
                file_type=0,
                force=False
            )
            print_result(False, "No lanzó FileExistsError")
        except FileExistsError as e:
            print_result(True, f"FileExistsError capturado: {e}")
        except Exception as e:
            print_result(False, f"Error inesperado: {type(e).__name__}: {e}")
        finally:
            os.unlink(input_file)
            os.unlink(output_file)
            
    except Exception as e:
        print_result(False, f"Error en setup: {e}")


def test_add_header_archivo_ya_tiene_cabecera():
    """Error: Archivo ya tiene cabecera AMSDOS válida"""
    print_test("add_amsdos_header() - Archivo ya tiene cabecera válida")
    
    temp_file = None
    output1 = None
    output2 = None
    
    try:
        # Crear archivo sin cabecera
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            f.write(b'\x00' * 200)
            temp_file = f.name
        
        # Añadir cabecera (primera vez debe funcionar)
        output1 = tempfile.mktemp(suffix='.bin')
        
        try:
            DSK.add_amsdos_header(temp_file, output1, load_addr=0x4000, file_type=0)
        except Exception as e:
            print_result(False, f"Error añadiendo cabecera inicial: {e}")
            return
        
        # Intentar añadir cabecera de nuevo (debe fallar)
        output2 = tempfile.mktemp(suffix='.bin')
        try:
            DSK.add_amsdos_header(output1, output2, load_addr=0x4000, file_type=0)
            print_result(False, "No lanzó DSKError")
        except DSKError as e:
            if "ya tiene" in str(e).lower():
                print_result(True, f"DSKError capturado: {e}")
            else:
                print_result(False, f"DSKError con mensaje inesperado: {e}")
        except Exception as e:
            print_result(False, f"Error inesperado: {type(e).__name__}: {e}")
                
    except Exception as e:
        print_result(False, f"Error en setup: {e}")
    finally:
        # Limpiar archivos
        if temp_file and os.path.exists(temp_file):
            os.unlink(temp_file)
        if output1 and os.path.exists(output1):
            os.unlink(output1)
        if output2 and os.path.exists(output2):
            os.unlink(output2)


def test_add_header_con_force():
    """Success: Sobrescribir archivo con force=True"""
    print_test("add_amsdos_header() - Sobrescribir con force=True")
    
    try:
        # Crear archivo de entrada
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            f.write(b'\xAA' * 100)
            input_file = f.name
        
        # Crear archivo de salida
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            f.write(b'\xFF' * 50)
            output_file = f.name
        
        original_size = os.path.getsize(output_file)
        
        try:
            DSK.add_amsdos_header(
                input_file,
                output_file,
                load_addr=0x4000,
                exec_addr=0x4000,
                file_type=0,
                force=True  # Debe sobrescribir
            )
            
            new_size = os.path.getsize(output_file)
            if new_size == 228:  # 100 bytes + 128 cabecera
                print_result(True, f"Sobrescribió correctamente: {original_size}B → {new_size}B")
            else:
                print_result(False, f"Tamaño incorrecto: esperado 228B, obtenido {new_size}B")
        except Exception as e:
            print_result(False, f"Error: {type(e).__name__}: {e}")
        finally:
            os.unlink(input_file)
            os.unlink(output_file)
            
    except Exception as e:
        print_result(False, f"Error en setup: {e}")


def test_add_header_archivo_vacio():
    """Edge case: Añadir cabecera a archivo vacío"""
    print_test("add_amsdos_header() - Archivo vacío")
    
    try:
        # Crear archivo vacío
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            # No escribir nada
            input_file = f.name
        
        output_file = tempfile.mktemp(suffix='.bin')
        
        try:
            DSK.add_amsdos_header(
                input_file,
                output_file,
                load_addr=0x4000,
                exec_addr=0x4000,
                file_type=0
            )
            
            # Verificar que se creó solo con cabecera
            size = os.path.getsize(output_file)
            if size == 128:
                print_result(True, f"Cabecera añadida a archivo vacío: {size}B")
            else:
                print_result(False, f"Tamaño incorrecto: esperado 128B, obtenido {size}B")
        except Exception as e:
            print_result(False, f"Error: {type(e).__name__}: {e}")
        finally:
            os.unlink(input_file)
            if os.path.exists(output_file):
                os.unlink(output_file)
                
    except Exception as e:
        print_result(False, f"Error en setup: {e}")


def test_add_header_direcciones_automaticas():
    """Success: Direcciones automáticas según tipo"""
    print_test("add_amsdos_header() - Direcciones automáticas")
    
    try:
        # Crear archivo de prueba
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            f.write(b'\x00' * 100)
            input_file = f.name
        
        # Probar diferentes tipos
        test_cases = [
            (0, 0x4000, "Binario"),
            (1, 0x0170, "BASIC protegido"),
            (2, 0x0170, "BASIC ASCII"),
            (3, 0x4000, "Binario protegido")
        ]
        
        all_ok = True
        for file_type, expected_load, type_name in test_cases:
            output_file = tempfile.mktemp(suffix='.bin')
            
            try:
                DSK.add_amsdos_header(
                    input_file,
                    output_file,
                    load_addr=0,  # AUTO
                    exec_addr=0,  # AUTO
                    file_type=file_type
                )
                
                # Leer cabecera para verificar dirección
                with open(output_file, 'rb') as f:
                    header = f.read(128)
                
                import struct
                load_addr = struct.unpack('<H', header[0x15:0x17])[0]
                
                if load_addr == expected_load:
                    print(f"  ✅ {type_name}: load=&{load_addr:04X} (esperado &{expected_load:04X})")
                else:
                    print(f"  ❌ {type_name}: load=&{load_addr:04X} (esperado &{expected_load:04X})")
                    all_ok = False
                    
                os.unlink(output_file)
                
            except Exception as e:
                print(f"  ❌ {type_name}: Error: {e}")
                all_ok = False
        
        os.unlink(input_file)
        print_result(all_ok, "Direcciones automáticas" if all_ok else "Algunas direcciones incorrectas")
        
    except Exception as e:
        print_result(False, f"Error en setup: {e}")


def test_add_header_tipos_validos():
    """Success: Todos los tipos de archivo válidos"""
    print_test("add_amsdos_header() - Tipos de archivo válidos (0-3)")
    
    try:
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            f.write(b'\x00' * 50)
            input_file = f.name
        
        all_ok = True
        for file_type in range(4):  # 0, 1, 2, 3
            output_file = tempfile.mktemp(suffix='.bin')
            
            try:
                DSK.add_amsdos_header(
                    input_file,
                    output_file,
                    load_addr=0x4000,
                    exec_addr=0x4000,
                    file_type=file_type
                )
                
                # Verificar que se creó
                if os.path.exists(output_file):
                    print(f"  ✅ Tipo {file_type}: OK")
                    os.unlink(output_file)
                else:
                    print(f"  ❌ Tipo {file_type}: No se creó archivo")
                    all_ok = False
                    
            except Exception as e:
                print(f"  ❌ Tipo {file_type}: {e}")
                all_ok = False
        
        os.unlink(input_file)
        print_result(all_ok, "Todos los tipos funcionan" if all_ok else "Algunos tipos fallaron")
        
    except Exception as e:
        print_result(False, f"Error en setup: {e}")


# ============================================================================
# TESTS DE remove_amsdos_header()
# ============================================================================

def test_remove_header_archivo_no_existe():
    """Error: Archivo de entrada no existe"""
    print_test("remove_amsdos_header() - Archivo de entrada no existe")
    
    try:
        DSK.remove_amsdos_header(
            'archivo_que_no_existe.bin',
            'output.bin'
        )
        print_result(False, "No lanzó FileNotFoundError")
    except FileNotFoundError as e:
        print_result(True, f"FileNotFoundError capturado: {e}")
    except Exception as e:
        print_result(False, f"Error inesperado: {type(e).__name__}: {e}")


def test_remove_header_archivo_salida_existe():
    """Error: Archivo de salida ya existe (sin force)"""
    print_test("remove_amsdos_header() - Archivo de salida existe (sin force)")
    
    try:
        # Crear archivo con cabecera
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            f.write(b'\x00' * 100)
            temp_file = f.name
        
        input_file = tempfile.mktemp(suffix='.bin')
        DSK.add_amsdos_header(temp_file, input_file, load_addr=0x4000, file_type=0)
        os.unlink(temp_file)
        
        # Crear archivo de salida que ya existe
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            f.write(b'\xFF' * 50)
            output_file = f.name
        
        try:
            DSK.remove_amsdos_header(
                input_file,
                output_file,
                force=False
            )
            print_result(False, "No lanzó FileExistsError")
        except FileExistsError as e:
            print_result(True, f"FileExistsError capturado: {e}")
        except Exception as e:
            print_result(False, f"Error inesperado: {type(e).__name__}: {e}")
        finally:
            os.unlink(input_file)
            os.unlink(output_file)
            
    except Exception as e:
        print_result(False, f"Error en setup: {e}")


def test_remove_header_archivo_muy_pequeno():
    """Error: Archivo demasiado pequeño (< 128 bytes)"""
    print_test("remove_amsdos_header() - Archivo muy pequeño (< 128 bytes)")
    
    try:
        # Crear archivo de menos de 128 bytes
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            f.write(b'\x00' * 100)  # Solo 100 bytes
            input_file = f.name
        
        output_file = tempfile.mktemp(suffix='.bin')
        
        try:
            DSK.remove_amsdos_header(input_file, output_file)
            print_result(False, "No lanzó DSKError")
        except DSKError as e:
            if "demasiado pequeño" in str(e).lower():
                print_result(True, f"DSKError capturado: {e}")
            else:
                print_result(False, f"DSKError con mensaje inesperado: {e}")
        except Exception as e:
            print_result(False, f"Error inesperado: {type(e).__name__}: {e}")
        finally:
            os.unlink(input_file)
            if os.path.exists(output_file):
                os.unlink(output_file)
                
    except Exception as e:
        print_result(False, f"Error en setup: {e}")


def test_remove_header_sin_cabecera_valida_tipo():
    """Error: Archivo sin cabecera válida (tipo incorrecto)"""
    print_test("remove_amsdos_header() - Tipo de archivo incorrecto")
    
    try:
        # Crear archivo con tipo inválido (no 0x00 ni 0x16)
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            header = bytearray(128)
            header[0] = 0xFF  # Tipo inválido
            f.write(header)
            f.write(b'\x00' * 100)
            input_file = f.name
        
        output_file = tempfile.mktemp(suffix='.bin')
        
        try:
            DSK.remove_amsdos_header(input_file, output_file)
            print_result(False, "No lanzó DSKError")
        except DSKError as e:
            if "tipo incorrecto" in str(e).lower():
                print_result(True, f"DSKError capturado: {e}")
            else:
                print_result(False, f"DSKError con mensaje inesperado: {e}")
        except Exception as e:
            print_result(False, f"Error inesperado: {type(e).__name__}: {e}")
        finally:
            os.unlink(input_file)
            if os.path.exists(output_file):
                os.unlink(output_file)
                
    except Exception as e:
        print_result(False, f"Error en setup: {e}")


def test_remove_header_checksum_incorrecto():
    """Error: Archivo con checksum incorrecto"""
    print_test("remove_amsdos_header() - Checksum incorrecto")
    
    try:
        # Crear archivo con checksum inválido
        import struct
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            header = bytearray(128)
            header[0] = 0x16  # Tipo válido (binario)
            # Poner datos pero checksum incorrecto
            struct.pack_into('<H', header, 0x43, 0xFFFF)  # Checksum malo
            f.write(header)
            f.write(b'\x00' * 100)
            input_file = f.name
        
        output_file = tempfile.mktemp(suffix='.bin')
        
        try:
            DSK.remove_amsdos_header(input_file, output_file)
            print_result(False, "No lanzó DSKError")
        except DSKError as e:
            if "checksum" in str(e).lower():
                print_result(True, f"DSKError capturado: {e}")
            else:
                print_result(False, f"DSKError con mensaje inesperado: {e}")
        except Exception as e:
            print_result(False, f"Error inesperado: {type(e).__name__}: {e}")
        finally:
            os.unlink(input_file)
            if os.path.exists(output_file):
                os.unlink(output_file)
                
    except Exception as e:
        print_result(False, f"Error en setup: {e}")


def test_remove_header_con_force():
    """Success: Sobrescribir archivo con force=True"""
    print_test("remove_amsdos_header() - Sobrescribir con force=True")
    
    try:
        # Crear archivo con cabecera válida
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            f.write(b'\xAA' * 100)
            temp_file = f.name
        
        input_file = tempfile.mktemp(suffix='.bin')
        DSK.add_amsdos_header(temp_file, input_file, load_addr=0x4000, file_type=0)
        os.unlink(temp_file)
        
        # Crear archivo de salida
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            f.write(b'\xFF' * 50)
            output_file = f.name
        
        original_size = os.path.getsize(output_file)
        
        try:
            DSK.remove_amsdos_header(
                input_file,
                output_file,
                force=True  # Debe sobrescribir
            )
            
            new_size = os.path.getsize(output_file)
            if new_size == 100:  # Tamaño original sin cabecera
                print_result(True, f"Sobrescribió correctamente: {original_size}B → {new_size}B")
            else:
                print_result(False, f"Tamaño incorrecto: esperado 100B, obtenido {new_size}B")
        except Exception as e:
            print_result(False, f"Error: {type(e).__name__}: {e}")
        finally:
            os.unlink(input_file)
            os.unlink(output_file)
            
    except Exception as e:
        print_result(False, f"Error en setup: {e}")


def test_remove_header_verifica_contenido():
    """Success: Contenido idéntico después de ciclo añadir/eliminar"""
    print_test("remove_amsdos_header() - Verificar integridad de contenido")
    
    try:
        # Crear archivo original con datos únicos
        original_data = bytes([i % 256 for i in range(500)])
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as f:
            f.write(original_data)
            original_file = f.name
        
        # Añadir cabecera
        with_header = tempfile.mktemp(suffix='.bin')
        DSK.add_amsdos_header(original_file, with_header, load_addr=0x8000, file_type=0)
        
        # Eliminar cabecera
        final_file = tempfile.mktemp(suffix='.bin')
        DSK.remove_amsdos_header(with_header, final_file)
        
        # Verificar contenido
        with open(final_file, 'rb') as f:
            final_data = f.read()
        
        if original_data == final_data:
            print_result(True, f"Contenido idéntico: {len(original_data)} bytes preservados")
        else:
            print_result(False, f"Contenido difiere: original {len(original_data)}B, final {len(final_data)}B")
        
        # Limpiar
        os.unlink(original_file)
        os.unlink(with_header)
        os.unlink(final_file)
        
    except Exception as e:
        print_result(False, f"Error: {type(e).__name__}: {e}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n" + "=" * 70)
    print(" TEST SUITE: Gestión de Cabeceras AMSDOS Externas")
    print(" Probando todos los casos de error y edge cases")
    print("=" * 70)
    
    print("\n" + "▶" * 35)
    print(" TESTS DE add_amsdos_header()")
    print("▶" * 35)
    
    test_add_header_archivo_no_existe()
    test_add_header_archivo_salida_existe()
    test_add_header_archivo_ya_tiene_cabecera()
    test_add_header_con_force()
    test_add_header_archivo_vacio()
    test_add_header_direcciones_automaticas()
    test_add_header_tipos_validos()
    
    print("\n" + "▶" * 35)
    print(" TESTS DE remove_amsdos_header()")
    print("▶" * 35)
    
    test_remove_header_archivo_no_existe()
    test_remove_header_archivo_salida_existe()
    test_remove_header_archivo_muy_pequeno()
    test_remove_header_sin_cabecera_valida_tipo()
    test_remove_header_checksum_incorrecto()
    test_remove_header_con_force()
    test_remove_header_verifica_contenido()
    
    print("\n" + "=" * 70)
    print(" FIN DE TESTS")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    main()
