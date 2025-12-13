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
CLI para PyDSK - Gestor de imágenes DSK para Amstrad CPC
Script principal para usar desde línea de comandos
"""

import sys
import argparse
from pathlib import Path

# Añadir el directorio padre al path para importar pydsk
sys.path.insert(0, str(Path(__file__).parent.parent))

from pydsk.dsk import DSK
from pydsk.exceptions import DSKError
from pydsk.basic_viewer import view_basic, detect_basic_format

# Importar Rich si está disponible
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


def cmd_new(args):
    """Crea una nueva imagen DSK"""
    try:
        dsk = DSK()
        
        # Determinar formato
        format_type = DSK.FORMAT_DATA  # Default
        if args.format:
            format_map = {
                'data': DSK.FORMAT_DATA,
                'system': DSK.FORMAT_SYSTEM,
                'vendor': DSK.FORMAT_VENDOR
            }
            format_type = format_map.get(args.format.lower(), DSK.FORMAT_DATA)
        
        # Crear DSK
        dsk.create(
            nb_tracks=args.tracks,
            nb_sectors=args.sectors,
            format_type=format_type
        )
        
        # Guardar
        dsk.save(args.dskfile)
        
        print(f"✅ Imagen DSK creada exitosamente: {args.dskfile}")
        info = dsk.get_info()
        print(f"   Formato: {info['format']}")
        print(f"   Pistas: {info['tracks']}")
        print(f"   Capacidad: {info['capacity_kb']} KB")
        
        return 0
        
    except DSKError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Error inesperado: {e}", file=sys.stderr)
        return 1


def cmd_info(args):
    """Muestra información de una imagen DSK"""
    try:
        dsk = DSK(args.dskfile)
        info = dsk.get_info()
        
        print(f"\n📀 Información de DSK: {args.dskfile}")
        print(f"{'─' * 50}")
        print(f"Formato:      {info['format']}")
        print(f"Pistas:       {info['tracks']}")
        print(f"Caras:        {info['heads']}")
        print(f"Tamaño pista: {info['track_size']} bytes")
        print(f"Tamaño total: {info['total_size']:,} bytes")
        print(f"Capacidad:    {info['capacity_kb']} KB")
        print()
        
        return 0
        
    except DSKError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_list(args):
    """Lista los archivos de una imagen DSK"""
    try:
        dsk = DSK(args.dskfile)
        
        # Usar Rich desde la clase DSK si está disponible
        use_rich = not args.no_color
        result = dsk.list_files(simple=args.simple, use_rich=use_rich)
        
        # Si devuelve None, Rich ya imprimió la salida
        # Si devuelve string, imprimir en formato tradicional
        if result is not None:
            print()
            print(result)
            print()
        
        return 0
        
    except DSKError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_import(args):
    """Importa archivos a una imagen DSK"""
    try:
        dsk = DSK(args.dskfile)
        
        # Procesar cada archivo
        for host_file in args.files:
            try:
                # Determinar nombre en DSK
                dsk_name = args.name if args.name else None
                
                # Importar archivo
                dsk.write_file(
                    host_filename=host_file,
                    dsk_filename=dsk_name,
                    file_type=args.type,
                    load_addr=args.load if args.load else 0,
                    exec_addr=args.exec if args.exec else 0,
                    user=args.user,
                    system=args.system,
                    read_only=args.read_only,
                    force=args.force
                )
                
                print(f"✅ Importado: {host_file}")
                
            except DSKError as e:
                print(f"❌ Error importando {host_file}: {e}", file=sys.stderr)
                if not args.force:
                    return 1
        
        # Guardar cambios
        dsk.save(args.dskfile)
        print(f"\n💾 Cambios guardados en: {args.dskfile}")
        
        # Mostrar directorio actualizado
        if args.verbose:
            print()
            listing = dsk.list_files(simple=True)
            print(listing)
        
        return 0
        
    except DSKError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_export(args):
    """Exporta archivos desde una imagen DSK"""
    try:
        dsk = DSK(args.dskfile)
        
        # Exportar todos los archivos
        if args.all:
            output_dir = args.output if args.output else '.'
            print(f"📦 Exportando todos los archivos a: {output_dir}/\n")
            
            exported = dsk.export_all(output_dir, keep_header=not args.no_header)
            
            print(f"\n✅ {len(exported)} archivo(s) exportado(s):")
            for filename in exported:
                print(f"   - {filename}")
            
            return 0
        
        # Exportar archivos específicos
        for dsk_file in args.files:
            try:
                # Determinar nombre de salida
                if args.output:
                    output_file = args.output
                else:
                    output_file = dsk_file.replace(' ', '').strip()
                
                # Exportar
                dsk.export_file(
                    dsk_filename=dsk_file,
                    host_filename=output_file,
                    user=args.user,
                    keep_header=not args.no_header
                )
                
                print(f"✅ Exportado: {dsk_file} -> {output_file}")
                
            except DSKError as e:
                print(f"❌ Error exportando {dsk_file}: {e}", file=sys.stderr)
                if not args.force:
                    return 1
        
        return 0
        
    except DSKError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_rename(args):
    """Renombra un archivo en una imagen DSK"""
    try:
        dsk = DSK(args.dskfile)
        
        # Validar que se proporcionó el nuevo nombre
        if not args.to:
            print("❌ Error: Debe especificar el nuevo nombre con --to", file=sys.stderr)
            return 1
        
        # Validar que solo se renombra un archivo
        if len(args.files) != 1:
            print("❌ Error: Solo se puede renombrar un archivo a la vez", file=sys.stderr)
            return 1
        
        old_name = args.files[0]
        new_name = args.to
        
        print(f"📝 Renombrando: {old_name} → {new_name}")
        
        # Renombrar
        dsk.rename_file(old_name, new_name, args.user)
        
        # Guardar cambios
        dsk.save(args.dskfile)
        
        print(f"✅ Archivo renombrado exitosamente")
        
        # Mostrar directorio actualizado
        if args.verbose:
            print("\n📋 Directorio actualizado:")
            entries = dsk.get_directory_entries()
            for entry in entries:
                if not entry.is_deleted:
                    print(f"   {entry.full_name}")
        
        return 0
        
    except DSKError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_delete(args):
    """Elimina archivos de una imagen DSK"""
    try:
        dsk = DSK(args.dskfile)
        
        if not args.files:
            print("❌ Error: Debe especificar al menos un archivo para eliminar", file=sys.stderr)
            return 1
        
        deleted_total = 0
        for filename in args.files:
            try:
                print(f"🗑️  Eliminando: {filename}")
                
                # Eliminar archivo
                extents = dsk.delete_file(filename, args.user)
                deleted_total += 1
                
                print(f"   ✅ {extents} extent(s) eliminado(s)")
                
            except DSKError as e:
                print(f"   ❌ Error: {e}", file=sys.stderr)
                if not args.force:
                    return 1
        
        # Guardar cambios
        if deleted_total > 0:
            dsk.save(args.dskfile)
            print(f"\n✅ {deleted_total} archivo(s) eliminado(s)")
            
            # Mostrar directorio actualizado
            if args.verbose:
                print("\n📋 Directorio actualizado:")
                entries = dsk.get_directory_entries()
                for entry in entries:
                    if not entry.is_deleted and entry.num_page == 0:
                        print(f"   {entry.full_name}")
        
        return 0
        
    except DSKError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_basic(args):
    """Muestra el listado de programas BASIC"""
    try:
        dsk = DSK(args.dskfile)
        
        if not args.files:
            print("❌ Error: Debe especificar al menos un archivo", file=sys.stderr)
            return 1
        
        for filename in args.files:
            try:
                # Leer archivo (sin cabecera AMSDOS)
                data = dsk.read_file(filename, args.user, keep_header=False)
                
                # Detectar formato primero
                is_tokenized, fmt = detect_basic_format(data)
                
                # Si no es un formato BASIC reconocido, verificar si es binario
                if fmt == "BASIC ASCII o texto":
                    # Verificar que no sea binario (ignorando padding de ceros al final)
                    # Buscar el último byte no-cero para ignorar padding
                    last_nonzero = len(data) - 1
                    while last_nonzero > 0 and data[last_nonzero] == 0:
                        last_nonzero -= 1
                    
                    # Analizar solo la parte con contenido real
                    content = data[:last_nonzero + 1]
                    if len(content) > 0:
                        # Para ASCII: verificar si tiene números de línea válidos
                        # Buscar patrones como "10 ", "20 ", etc.
                        text = content[:min(200, len(content))].decode('ascii', errors='ignore')
                        lines = text.split('\n')
                        valid_lines = 0
                        for line in lines[:5]:  # Verificar primeras 5 líneas
                            line = line.strip()
                            if line and line[0].isdigit():
                                parts = line.split(None, 1)
                                if parts and parts[0].isdigit():
                                    valid_lines += 1
                        
                        # Si no hay líneas numeradas válidas, es binario
                        if valid_lines == 0 and len(lines) > 0:
                            if not args.force:
                                print(f"\n{'='*70}")
                                print(f"  {filename}")
                                print(f"{'='*70}")
                                print(f"❌ Cannot display: Binary file (not a BASIC program)")
                                print(f"   Use --force flag to attempt display anyway\n")
                                continue
                
                # Mostrar encabezado
                print(f"\n{'='*70}")
                print(f"  {filename} ({fmt})")
                print(f"{'='*70}\n")
                
                # Visualizar
                listing = view_basic(data)
                print(listing)
                
            except DSKError as e:
                print(f"❌ Error con {filename}: {e}", file=sys.stderr)
                if not args.force:
                    return 1
        
        return 0
        
    except DSKError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_filetype(args):
    """Muestra el tipo de archivo (BASIC/ASCII/BINARY/RAW)"""
    try:
        dsk = DSK(args.dskfile)
        
        if not args.files:
            print("❌ Error: Debe especificar al menos un archivo", file=sys.stderr)
            return 1
        
        for filename in args.files:
            try:
                # Normalizar nombre para búsqueda
                amsdos_name = dsk._get_amsdos_filename(filename)
                
                # Verificar si el archivo existe y si está eliminado
                entries = dsk.get_directory_entries()
                file_found = False
                is_deleted = False
                
                # Primero buscar archivo no eliminado
                for entry in entries:
                    if (entry.full_name == amsdos_name and 
                        entry.user == args.user and
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
                    print(f"{filename}: DELETED")
                    continue
                
                # Leer archivo (sin cabecera AMSDOS)
                data = dsk.read_file(filename, args.user, keep_header=False)
                
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
                
                # Mostrar resultado
                print(f"{filename}: {file_type}")
                
            except DSKError as e:
                print(f"❌ Error con {filename}: {e}", file=sys.stderr)
                if not args.force:
                    return 1
        
        return 0
        
    except DSKError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_add_header(args):
    """Comando para añadir cabecera AMSDOS a archivo externo"""
    try:
        # Añadir cabecera
        DSK.add_amsdos_header(
            args.input_file,
            args.output_file,
            load_addr=args.load,
            exec_addr=args.exec,
            file_type=args.type,
            force=args.force
        )
        
        print(f"Cabecera AMSDOS añadida exitosamente")
        print(f"  Entrada:  {args.input_file}")
        print(f"  Salida:   {args.output_file}")
        print(f"  Load:     &{args.load:04X}" if args.load else "  Load:     AUTO")
        print(f"  Exec:     &{args.exec:04X}" if args.exec else "  Exec:     AUTO")
        
        type_names = {
            0: "Binario",
            1: "BASIC protegido",
            2: "BASIC ASCII",
            3: "Binario protegido"
        }
        print(f"  Tipo:     {type_names.get(args.type, 'Desconocido')}")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except FileExistsError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except DSKError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error inesperado: {e}", file=sys.stderr)
        return 1


def cmd_remove_header(args):
    """Comando para eliminar cabecera AMSDOS de archivo externo"""
    try:
        # Eliminar cabecera
        DSK.remove_amsdos_header(
            args.input_file,
            args.output_file,
            force=args.force
        )
        
        print(f"Cabecera AMSDOS eliminada exitosamente")
        print(f"  Entrada:  {args.input_file}")
        print(f"  Salida:   {args.output_file}")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except FileExistsError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except DSKError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error inesperado: {e}", file=sys.stderr)
        return 1


def main():
    """Función principal del CLI"""
    parser = argparse.ArgumentParser(
        prog='pydsk',
        description='PyDSK - Gestor de imágenes DSK para Amstrad CPC',
        epilog='Ejemplo: pydsk new mydisk.dsk --tracks 40 --sectors 9'
    )
    
    subparsers = parser.add_subparsers(
        title='Comandos',
        dest='command',
        help='Comando a ejecutar'
    )
    
    # Comando: new
    parser_new = subparsers.add_parser(
        'new',
        help='Crear una nueva imagen DSK vacía'
    )
    parser_new.add_argument(
        'dskfile',
        help='Nombre del archivo DSK a crear'
    )
    parser_new.add_argument(
        '-t', '--tracks',
        type=int,
        default=40,
        help='Número de pistas (por defecto: 40)'
    )
    parser_new.add_argument(
        '-s', '--sectors',
        type=int,
        default=9,
        help='Número de sectores por pista (por defecto: 9)'
    )
    parser_new.add_argument(
        '-f', '--format',
        choices=['data', 'system', 'vendor'],
        default='data',
        help='Tipo de formato (por defecto: data)'
    )
    parser_new.set_defaults(func=cmd_new)
    
    # Comando: list
    parser_list = subparsers.add_parser(
        'list',
        aliases=['ls', 'l'],
        help='Listar archivos en una imagen DSK'
    )
    parser_list.add_argument(
        'dskfile',
        help='Archivo DSK a listar'
    )
    parser_list.add_argument(
        '-s', '--simple',
        action='store_true',
        help='Formato simple (columnas) en lugar de tabla'
    )
    parser_list.add_argument(
        '--no-color',
        action='store_true',
        help='Desactivar colores y usar formato tradicional'
    )
    parser_list.set_defaults(func=cmd_list)
    
    # Comando: info
    parser_info = subparsers.add_parser(
        'info',
        help='Mostrar información de un archivo DSK'
    )
    parser_info.add_argument(
        'dskfile',
        help='Archivo DSK a analizar'
    )
    parser_info.set_defaults(func=cmd_info)
    
    # Comando: import
    parser_import = subparsers.add_parser(
        'import',
        aliases=['add', 'put'],
        help='Importar archivos a una imagen DSK'
    )
    parser_import.add_argument(
        'dskfile',
        help='Archivo DSK donde importar'
    )
    parser_import.add_argument(
        'files',
        nargs='+',
        help='Archivo(s) a importar'
    )
    parser_import.add_argument(
        '-n', '--name',
        help='Nombre del archivo en el DSK (solo si se importa un archivo)'
    )
    parser_import.add_argument(
        '-t', '--type',
        type=int,
        default=0,
        choices=[0, 1, 2, 3, -1],
        help='Tipo de archivo: 0=binario, 1=BASIC protegido, 2=BASIC ASCII, 3=binario protegido, -1=RAW (por defecto: 0)'
    )
    parser_import.add_argument(
        '-l', '--load',
        type=lambda x: int(x, 0),  # Permite 0x1234 o 4660
        help='Dirección de carga (hexadecimal: 0x1234 o decimal: 4660)'
    )
    parser_import.add_argument(
        '-e', '--exec',
        type=lambda x: int(x, 0),
        help='Dirección de ejecución (hexadecimal: 0x1234 o decimal: 4660)'
    )
    parser_import.add_argument(
        '-u', '--user',
        type=int,
        default=0,
        choices=range(0, 16),
        help='Número de usuario (0-15, por defecto: 0)'
    )
    parser_import.add_argument(
        '-s', '--system',
        action='store_true',
        help='Marcar como archivo de sistema'
    )
    parser_import.add_argument(
        '-r', '--read-only',
        action='store_true',
        help='Marcar como solo lectura'
    )
    parser_import.add_argument(
        '-f', '--force',
        action='store_true',
        help='Sobrescribir si el archivo ya existe'
    )
    parser_import.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Mostrar directorio después de importar'
    )
    parser_import.set_defaults(func=cmd_import)
    
    # Comando: export
    parser_export = subparsers.add_parser(
        'export',
        aliases=['get', 'extract'],
        help='Exportar archivos desde una imagen DSK'
    )
    parser_export.add_argument(
        'dskfile',
        help='Archivo DSK desde donde exportar'
    )
    parser_export.add_argument(
        'files',
        nargs='*',
        help='Archivo(s) a exportar (si no se especifica, usar --all)'
    )
    parser_export.add_argument(
        '-o', '--output',
        help='Archivo o directorio de salida'
    )
    parser_export.add_argument(
        '-a', '--all',
        action='store_true',
        help='Exportar todos los archivos'
    )
    parser_export.add_argument(
        '-u', '--user',
        type=int,
        default=0,
        choices=range(0, 16),
        help='Número de usuario (0-15, por defecto: 0)'
    )
    parser_export.add_argument(
        '--no-header',
        action='store_true',
        help='Remover cabecera AMSDOS al exportar'
    )
    parser_export.add_argument(
        '-f', '--force',
        action='store_true',
        help='Continuar aunque haya errores'
    )
    parser_export.set_defaults(func=cmd_export)
    
    # Comando: rename
    parser_rename = subparsers.add_parser(
        'rename',
        aliases=['mv', 'move'],
        help='Renombrar un archivo en una imagen DSK'
    )
    parser_rename.add_argument(
        'dskfile',
        help='Archivo DSK donde renombrar'
    )
    parser_rename.add_argument(
        'files',
        nargs=1,
        help='Archivo a renombrar'
    )
    parser_rename.add_argument(
        '--to',
        required=True,
        help='Nuevo nombre para el archivo'
    )
    parser_rename.add_argument(
        '-u', '--user',
        type=int,
        default=0,
        choices=range(0, 16),
        help='Número de usuario (0-15, por defecto: 0)'
    )
    parser_rename.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Mostrar directorio después de renombrar'
    )
    parser_rename.set_defaults(func=cmd_rename)
    
    # Comando: delete
    parser_delete = subparsers.add_parser(
        'delete',
        aliases=['remove', 'rm', 'del'],
        help='Eliminar archivos de una imagen DSK'
    )
    parser_delete.add_argument(
        'dskfile',
        help='Archivo DSK del cual eliminar'
    )
    parser_delete.add_argument(
        'files',
        nargs='+',
        help='Archivo(s) a eliminar'
    )
    parser_delete.add_argument(
        '-u', '--user',
        type=int,
        default=0,
        choices=range(0, 16),
        help='Número de usuario (0-15, por defecto: 0)'
    )
    parser_delete.add_argument(
        '-f', '--force',
        action='store_true',
        help='Continuar aunque haya errores'
    )
    parser_delete.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Mostrar directorio después de eliminar'
    )
    parser_delete.set_defaults(func=cmd_delete)
    
    # Comando: basic
    parser_basic = subparsers.add_parser(
        'basic',
        aliases=['view', 'show', 'cat'],
        help='Mostrar listado de programas BASIC'
    )
    parser_basic.add_argument(
        'dskfile',
        help='Archivo DSK a leer'
    )
    parser_basic.add_argument(
        'files',
        nargs='+',
        help='Archivo(s) BASIC a mostrar'
    )
    parser_basic.add_argument(
        '-u', '--user',
        type=int,
        default=0,
        choices=range(0, 16),
        help='Número de usuario (0-15, por defecto: 0)'
    )
    parser_basic.add_argument(
        '-f', '--force',
        action='store_true',
        help='Continuar aunque haya errores'
    )
    parser_basic.set_defaults(func=cmd_basic)
    
    # Comando: filetype
    parser_filetype = subparsers.add_parser(
        'filetype',
        help='Mostrar tipo de archivo (BASIC/ASCII/BINARY/RAW)'
    )
    parser_filetype.add_argument(
        'dskfile',
        help='Archivo DSK a leer'
    )
    parser_filetype.add_argument(
        'files',
        nargs='+',
        help='Archivo(s) a analizar'
    )
    parser_filetype.add_argument(
        '-u', '--user',
        type=int,
        default=0,
        choices=range(0, 16),
        help='Número de usuario (0-15, por defecto: 0)'
    )
    parser_filetype.add_argument(
        '-f', '--force',
        action='store_true',
        help='Continuar aunque haya errores'
    )
    parser_filetype.set_defaults(func=cmd_filetype)
    
    # Comando: add-header - Añadir cabecera AMSDOS a archivo externo
    parser_addheader = subparsers.add_parser(
        'add-header',
        help='Añadir cabecera AMSDOS a un archivo externo'
    )
    parser_addheader.add_argument(
        'input_file',
        help='Archivo de entrada (sin cabecera)'
    )
    parser_addheader.add_argument(
        'output_file',
        help='Archivo de salida (con cabecera)'
    )
    parser_addheader.add_argument(
        '-l', '--load',
        type=lambda x: int(x, 0),
        default=0,
        help='Dirección de carga en hexadecimal (ej: 0x4000) o decimal. 0=auto'
    )
    parser_addheader.add_argument(
        '-e', '--exec',
        type=lambda x: int(x, 0),
        default=0,
        help='Dirección de ejecución en hexadecimal (ej: 0x4000) o decimal. 0=auto'
    )
    parser_addheader.add_argument(
        '-t', '--type',
        type=int,
        default=0,
        choices=[0, 1, 2, 3],
        help='Tipo de archivo: 0=binario, 1=BASIC protegido, 2=BASIC ASCII, 3=binario protegido'
    )
    parser_addheader.add_argument(
        '-f', '--force',
        action='store_true',
        help='Sobrescribir archivo de salida si existe'
    )
    parser_addheader.set_defaults(func=cmd_add_header)
    
    # Comando: remove-header - Eliminar cabecera AMSDOS de archivo externo
    parser_rmheader = subparsers.add_parser(
        'remove-header',
        help='Eliminar cabecera AMSDOS de un archivo externo'
    )
    parser_rmheader.add_argument(
        'input_file',
        help='Archivo de entrada (con cabecera)'
    )
    parser_rmheader.add_argument(
        'output_file',
        help='Archivo de salida (sin cabecera)'
    )
    parser_rmheader.add_argument(
        '-f', '--force',
        action='store_true',
        help='Sobrescribir archivo de salida si existe'
    )
    parser_rmheader.set_defaults(func=cmd_remove_header)
    
    # Parsear argumentos
    args = parser.parse_args()
    
    # Si no hay comando, mostrar ayuda
    if not args.command:
        parser.print_help()
        return 1
    
    # Ejecutar comando
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
