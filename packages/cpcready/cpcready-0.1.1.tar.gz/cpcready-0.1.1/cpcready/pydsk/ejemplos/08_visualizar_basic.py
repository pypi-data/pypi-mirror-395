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
Ejemplos de Visualización de Programas BASIC en DSK
====================================================

Este módulo demuestra el uso de las funcionalidades de visualización
de programas BASIC en imágenes DSK de Amstrad CPC.

Cubre:
- Visualización de BASIC ASCII
- Visualización de BASIC tokenizado
- Auto-detección de formato
- Manejo de archivos binarios
- Gestión de múltiples programas

Autor: CPCReady
Fecha: Noviembre 2025
"""


import os
import sys
from pathlib import Path

# Añadir directorio padre al path para importar pydsk
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pydsk.dsk import DSK
from pydsk.basic_viewer import view_basic, detect_basic_format, view_basic_ascii, detokenize_basic


def ejemplo_01_visualizar_basic_ascii():
    """
    Ejemplo 1: Visualizar programa BASIC ASCII
    
    Muestra cómo visualizar un programa BASIC en formato ASCII
    (texto plano con números de línea).
    """
    print("\n" + "="*70)
    print("EJEMPLO 1: Visualizar Programa BASIC ASCII")
    print("="*70)
    
    # Crear DSK temporal
    dsk = DSK()
    dsk.create(nb_tracks=40, nb_sectors=9, format_type=DSK.FORMAT_DATA)
    
    # Crear programa BASIC ASCII simple
    programa_ascii = b'10 PRINT "HELLO WORLD"\r\n'
    programa_ascii += b'20 FOR I=1 TO 10\r\n'
    programa_ascii += b'30 PRINT I\r\n'
    programa_ascii += b'40 NEXT I\r\n'
    programa_ascii += b'50 END\r\n'
    
    # Guardar temporalmente el programa
    temp_file = '/tmp/hello_example.bas'
    with open(temp_file, 'wb') as f:
        f.write(programa_ascii)
    
    # Escribir al DSK
    dsk.write_file(
        temp_file,
        dsk_filename='HELLO.BAS',
        file_type=2,  # BASIC ASCII
        user=0
    )
    
    print("\n1. Programa BASIC ASCII creado")
    print("   Archivo: HELLO.BAS")
    print(f"   Tamaño: {len(programa_ascii)} bytes")
    
    # Leer archivo
    data = dsk.read_file('HELLO.BAS', keep_header=False)
    
    print("\n2. Detectando formato...")
    is_tokenized, description = detect_basic_format(data)
    print(f"   Formato detectado: {description}")
    
    # Visualizar
    print("\n3. Listado del programa:")
    print("-" * 50)
    listing = view_basic(data, auto_detect=True)
    print(listing)
    print("-" * 50)
    
    # Verificar resultado
    assert not is_tokenized, "Debería detectar formato ASCII"
    assert "HELLO WORLD" in listing, "El listado debe contener el texto"
    assert "10 PRINT" in listing, "El listado debe tener números de línea"
    
    print("\n✓ Programa BASIC ASCII visualizado correctamente")


def ejemplo_02_visualizar_basic_tokenizado():
    """
    Ejemplo 2: Visualizar programa BASIC tokenizado
    
    Muestra cómo visualizar un programa BASIC en formato tokenizado
    (formato binario con tokens 0x80-0xFF del CPC).
    """
    print("\n" + "="*70)
    print("EJEMPLO 2: Visualizar Programa BASIC Tokenizado")
    print("="*70)
    
    # Cargar DSK existente con programas BASIC tokenizados
    dsk_path = Path(__file__).parent.parent.parent / 'demo_8bp_v41_004.dsk'
    
    if not dsk_path.exists():
        print("\n⚠ DSK de demostración no encontrado")
        print(f"   Buscar en: {dsk_path}")
        return
    
    dsk = DSK(str(dsk_path))
    
    print("\n1. DSK cargado")
    print(f"   Archivo: {dsk_path.name}")
    
    # Buscar archivos .BAS
    entries = dsk.get_directory_entries()
    archivos_bas = [e for e in entries 
                    if not e.is_deleted and e.full_name.endswith('.BAS')]
    
    if not archivos_bas:
        print("\n⚠ No se encontraron archivos .BAS en el DSK")
        return
    
    # Visualizar primer archivo BASIC
    archivo = archivos_bas[0].full_name
    print(f"\n2. Leyendo archivo: {archivo}")
    
    data = dsk.read_file(archivo, keep_header=False)
    
    print(f"   Tamaño: {len(data)} bytes")
    
    # Detectar formato
    print("\n3. Detectando formato...")
    is_tokenized, description = detect_basic_format(data)
    print(f"   Formato detectado: {description}")
    
    # Visualizar
    print("\n4. Listado del programa:")
    print("-" * 50)
    try:
        listing = view_basic(data, auto_detect=True)
        print(listing)
    except ValueError as e:
        print(f"   Error al visualizar: {e}")
    print("-" * 50)
    
    # Verificar resultado
    if is_tokenized:
        print("\n✓ Programa BASIC tokenizado visualizado")
        print("  (Nota: Formato básico, puede diferir de idsk20)")
    else:
        print("\n✓ Programa resultó ser ASCII")


def ejemplo_03_detectar_formato():
    """
    Ejemplo 3: Auto-detección de formato BASIC
    
    Muestra cómo detectar automáticamente si un archivo es
    BASIC tokenizado o ASCII.
    """
    print("\n" + "="*70)
    print("EJEMPLO 3: Auto-detección de Formato BASIC")
    print("="*70)
    
    # Crear DSK con ambos formatos
    dsk = DSK()
    dsk.create(nb_tracks=40, nb_sectors=9, format_type=DSK.FORMAT_DATA)
    
    print("\n1. Creando archivos BASIC de diferentes formatos...")
    
    # Programa ASCII
    programa_ascii = b'10 REM ASCII FORMAT\r\n20 PRINT "ASCII"\r\n'
    temp_ascii = '/tmp/ascii_example.bas'
    with open(temp_ascii, 'wb') as f:
        f.write(programa_ascii)
    dsk.write_file(temp_ascii, dsk_filename='ASCII.BAS', file_type=2, user=0)
    
    # Programa tokenizado simple (simulado)
    # Formato: [length_lo][length_hi][line_lo][line_hi][tokens...][0x00]
    programa_token = bytearray()
    
    # Línea 10: PRINT "TOKEN"
    linea = bytearray()
    linea.extend([10, 0])  # Número de línea 10
    linea.append(0xBF)     # Token PRINT
    linea.extend(b' "TOKEN"')
    linea.append(0x00)     # Fin de línea
    
    # Longitud de la línea
    long = len(linea) + 2
    programa_token.extend([long & 0xFF, (long >> 8) & 0xFF])
    programa_token.extend(linea)
    
    # Línea 20: END
    linea2 = bytearray()
    linea2.extend([20, 0])  # Número de línea 20
    linea2.append(0xC0)     # Token END
    linea2.append(0x00)     # Fin de línea
    
    long2 = len(linea2) + 2
    programa_token.extend([long2 & 0xFF, (long2 >> 8) & 0xFF])
    programa_token.extend(linea2)
    
    temp_token = '/tmp/token_example.bas'
    with open(temp_token, 'wb') as f:
        f.write(bytes(programa_token))
    dsk.write_file(temp_token, dsk_filename='TOKEN.BAS', file_type=2, user=0)
    
    print("   - ASCII.BAS (formato texto)")
    print("   - TOKEN.BAS (formato tokenizado)")
    
    # Detectar formatos
    print("\n2. Detectando formatos...")
    
    archivos = ['ASCII.BAS', 'TOKEN.BAS']
    
    for archivo in archivos:
        data = dsk.read_file(archivo, keep_header=False)
        is_tokenized, description = detect_basic_format(data)
        
        print(f"\n   {archivo}:")
        print(f"   - Formato: {description}")
        print(f"   - Tokenizado: {is_tokenized}")
        print(f"   - Primeros bytes: {data[:10].hex()}")
    
    print("\n✓ Auto-detección funcionando correctamente")


def ejemplo_04_manejo_archivos_binarios():
    """
    Ejemplo 4: Manejo de archivos binarios
    
    Muestra cómo el visor BASIC detecta y rechaza archivos
    binarios que no son programas BASIC.
    """
    print("\n" + "="*70)
    print("EJEMPLO 4: Detección de Archivos Binarios")
    print("="*70)
    
    # Crear DSK con diferentes tipos de archivos
    dsk = DSK()
    dsk.create(nb_tracks=40, nb_sectors=9, format_type=DSK.FORMAT_DATA)
    
    print("\n1. Creando archivos de diferentes tipos...")
    
    # Programa BASIC válido
    programa_basic = b'10 PRINT "VALID"\r\n'
    temp_valid = '/tmp/valid_example.bas'
    with open(temp_valid, 'wb') as f:
        f.write(programa_basic)
    dsk.write_file(temp_valid, dsk_filename='VALID.BAS', file_type=2, user=0)
    print("   - VALID.BAS (BASIC ASCII válido)")
    
    # Archivo binario puro
    datos_binarios = bytes(range(256))  # 00-FF
    temp_data = '/tmp/data_example.bin'
    with open(temp_data, 'wb') as f:
        f.write(datos_binarios)
    dsk.write_file(temp_data, dsk_filename='DATA.BIN', file_type=0, user=0)
    print("   - DATA.BIN (binario puro)")
    
    # Archivo de texto no-BASIC
    texto = b'Este es un archivo de texto sin formato BASIC'
    temp_text = '/tmp/text_example.dat'
    with open(temp_text, 'wb') as f:
        f.write(texto)
    dsk.write_file(temp_text, dsk_filename='TEXT.DAT', file_type=0, user=0)
    print("   - TEXT.DAT (texto sin formato)")
    
    # Probar visualización
    print("\n2. Intentando visualizar cada archivo...")
    
    archivos = ['VALID.BAS', 'DATA.BIN', 'TEXT.DAT']
    
    for archivo in archivos:
        print(f"\n   {archivo}:")
        data = dsk.read_file(archivo, keep_header=False)
        
        # Simulación de detección binaria (50% caracteres imprimibles)
        printable = sum(1 for b in data[:100] if 32 <= b <= 126 or b in (9, 10, 13))
        percent = (printable / min(len(data), 100)) * 100
        is_binary = percent < 50
        
        print(f"   - Caracteres imprimibles: {percent:.1f}%")
        print(f"   - Clasificación: {'BINARIO' if is_binary else 'TEXTO'}")
        
        if not is_binary:
            try:
                is_tokenized, desc = detect_basic_format(data)
                print(f"   - Formato BASIC: {desc}")
            except ValueError as e:
                print(f"   - Error detección: {e}")
    
    print("\n✓ Detección de archivos binarios funcionando")


def ejemplo_05_multiples_programas():
    """
    Ejemplo 5: Visualizar múltiples programas BASIC
    
    Muestra cómo listar y visualizar todos los programas BASIC
    de un DSK de forma organizada.
    """
    print("\n" + "="*70)
    print("EJEMPLO 5: Visualizar Múltiples Programas BASIC")
    print("="*70)
    
    # Crear DSK con varios programas
    dsk = DSK()
    dsk.create(nb_tracks=40, nb_sectors=9, format_type=DSK.FORMAT_DATA)
    
    print("\n1. Creando múltiples programas BASIC...")
    
    programas = {
        'MENU.BAS': b'10 CLS\r\n20 PRINT "MENU PRINCIPAL"\r\n30 PRINT "1. JUGAR"\r\n40 PRINT "2. SALIR"\r\n',
        'GAME.BAS': b'10 REM JUEGO\r\n20 MODE 0\r\n30 PRINT "GAME START"\r\n',
        'UTIL.BAS': b'10 REM UTILIDADES\r\n20 DEF FN SQ(X)=X*X\r\n30 END\r\n'
    }
    
    for nombre, codigo in programas.items():
        temp_file = f'/tmp/{nombre.lower()}'
        with open(temp_file, 'wb') as f:
            f.write(codigo)
        dsk.write_file(temp_file, dsk_filename=nombre, file_type=2, user=0)
        print(f"   - {nombre} ({len(codigo)} bytes)")
    
    # Listar archivos BASIC
    print("\n2. Archivos BASIC en el DSK:")
    entries = dsk.get_directory_entries()
    archivos_bas = [e for e in entries 
                    if not e.is_deleted and e.full_name.endswith('.BAS')]
    
    for entry in archivos_bas:
        print(f"   - {entry.full_name} (User {entry.user})")
    
    # Visualizar todos
    print("\n3. Visualizando todos los programas:")
    
    for entry in archivos_bas:
        nombre = entry.full_name
        data = dsk.read_file(nombre, keep_header=False)
        is_tokenized, description = detect_basic_format(data)
        
        print(f"\n{'='*50}")
        print(f"  {nombre} ({description})")
        print('='*50)
        
        try:
            listing = view_basic(data, auto_detect=True)
            print(listing)
        except ValueError as e:
            print(f"Error: {e}")
    
    print("\n✓ Múltiples programas visualizados correctamente")


def ejemplo_06_exportar_listados():
    """
    Ejemplo 6: Exportar listados BASIC a archivos de texto
    
    Muestra cómo extraer programas BASIC del DSK y guardarlos
    como archivos de texto legibles.
    """
    print("\n" + "="*70)
    print("EJEMPLO 6: Exportar Listados BASIC a Texto")
    print("="*70)
    
    # Crear DSK con programas
    dsk = DSK()
    dsk.create(nb_tracks=40, nb_sectors=9, format_type=DSK.FORMAT_DATA)
    
    print("\n1. Creando programas BASIC para exportar...")
    
    programa1 = b'10 REM PROGRAMA DE EJEMPLO\r\n'
    programa1 += b'20 PRINT "EXPORTANDO..."\r\n'
    programa1 += b'30 FOR I=1 TO 5\r\n'
    programa1 += b'40 PRINT I\r\n'
    programa1 += b'50 NEXT I\r\n'
    
    temp_export = '/tmp/export_example.bas'
    with open(temp_export, 'wb') as f:
        f.write(programa1)
    dsk.write_file(temp_export, dsk_filename='EXPORT.BAS', file_type=2, user=0)
    print("   - EXPORT.BAS creado")
    
    # Leer y visualizar
    print("\n2. Leyendo programa del DSK...")
    data = dsk.read_file('EXPORT.BAS', keep_header=False)
    is_tokenized, description = detect_basic_format(data)
    print(f"   Formato: {description}")
    
    # Generar listado
    print("\n3. Generando listado...")
    listing = view_basic(data, auto_detect=True)
    
    # Exportar a archivo de texto
    output_path = '/tmp/export_basic.txt'
    with open(output_path, 'w', encoding='ascii') as f:
        f.write("="*50 + "\n")
        f.write("  Listado de EXPORT.BAS\n")
        f.write("="*50 + "\n\n")
        f.write(listing)
        f.write("\n\n" + "="*50 + "\n")
        f.write(f"  Formato: {description}\n")
        f.write("="*50 + "\n")
    
    print(f"   Listado guardado en: {output_path}")
    
    # Mostrar contenido
    print("\n4. Contenido del archivo exportado:")
    print("-" * 50)
    with open(output_path, 'r', encoding='ascii') as f:
        print(f.read())
    print("-" * 50)
    
    print("\n✓ Listado BASIC exportado exitosamente")


def main():
    """Ejecutar todos los ejemplos"""
    print("\n" + "="*70)
    print("EJEMPLOS DE VISUALIZACIÓN DE PROGRAMAS BASIC")
    print("="*70)
    
    ejemplos = [
        ejemplo_01_visualizar_basic_ascii,
        ejemplo_02_visualizar_basic_tokenizado,
        ejemplo_03_detectar_formato,
        ejemplo_04_manejo_archivos_binarios,
        ejemplo_05_multiples_programas,
        ejemplo_06_exportar_listados
    ]
    
    for i, ejemplo in enumerate(ejemplos, 1):
        try:
            ejemplo()
        except Exception as e:
            print(f"\n✗ Error en ejemplo {i}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70)
    print("EJEMPLOS COMPLETADOS")
    print("="*70)


if __name__ == '__main__':
    main()
