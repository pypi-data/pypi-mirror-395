# PyDSK - Python DSK Manager para Amstrad CPC

Implementación Python de un gestor de imágenes DSK para Amstrad CPC, compatible con el formato CPCEMU.

## Estado del Proyecto

### Funcionalidades Implementadas

- ✅ **Crear imágenes DSK** - Nuevas imágenes vacías con diferentes formatos (DATA, SYSTEM, VENDOR)
- ✅ **Listar archivos** - Ver contenido del DSK en formato tabla o simple con Rich
- ✅ **Información del DSK** - Obtener detalles técnicos del disco
- ✅ **Importar archivos** - Añadir archivos al DSK con soporte completo de cabeceras AMSDOS
- ✅ **Exportar archivos** - Extraer archivos del DSK con/sin cabecera AMSDOS
- ✅ **Gestión de cabeceras AMSDOS** - Añadir/eliminar cabeceras en archivos externos
- ✅ **Renombrar archivos** - Cambiar nombre de archivos en el DSK (múltiples extents soportados)
- ✅ **Eliminar archivos** - Borrar archivos del DSK (marcado lógico, múltiples archivos)
- ✅ **Visualizar BASIC** - Ver programas BASIC tokenizados y ASCII
- ✅ **Detectar tipos** - Identificar tipo de archivo (BASIC/BINARY/ASCII/RAW/DELETED)

## Instalación

```bash
# Clonar el repositorio
cd idsk/pydsk

# No requiere instalación, usar directamente
python3 cli.py --help
```

## Uso desde CLI

### Crear una nueva imagen DSK

```bash
# Crear DSK con configuración por defecto (40 pistas, 9 sectores, formato DATA)
python3 cli.py new mydisk.dsk

# Crear con opciones personalizadas
python3 cli.py new mydisk.dsk --tracks 42 --sectors 9 --format data

# Crear formato SYSTEM
python3 cli.py new system.dsk --format system
```

### Ver información de un DSK

```bash
python3 cli.py info mydisk.dsk
```

### Listar archivos

```bash
# Formato tabla con colores (requiere Rich) - por defecto
python3 cli.py list mydisk.dsk
python3 cli.py ls mydisk.dsk      # Alias corto

# Características del formato Rich:
# - Colores por tipo de archivo (BASIC en cyan, BINARY en amarillo, etc.)
# - Detección automática de tipo (BASIC, BINARY, SCREEN$, etc.)
# - Tabla con bordes mejorados y encabezados destacados
# - Columna adicional mostrando el tipo de archivo

# Formato simple (columnas, sin colores)
python3 cli.py list mydisk.dsk --simple
python3 cli.py ls mydisk.dsk -s

# Formato tradicional sin colores (sin Rich)
python3 cli.py list mydisk.dsk --no-color
```

### Importar archivos

```bash
# Importar archivo BASIC (modo ASCII)
python3 cli.py import mydisk.dsk program.bas --type 2

# Importar binario con direcciones de carga y ejecución
python3 cli.py import mydisk.dsk code.bin --type 0 --load 0x4000 --exec 0x4000

# Importar múltiples archivos
python3 cli.py import mydisk.dsk file1.bas file2.bin file3.dat

# Importar con atributos especiales
python3 cli.py import mydisk.dsk system.bas --system --read-only

# Importar en área de usuario específica
python3 cli.py import mydisk.dsk file.bas --user 10

# Sobrescribir archivo existente
python3 cli.py import mydisk.dsk file.bas --force

# Tipos de archivo (-t):
#   0 = Binario con cabecera AMSDOS (default)
#   1 = BASIC protegido con cabecera
#   2 = BASIC ASCII sin cabecera
#   3 = Binario protegido con cabecera
#  -1 = RAW (sin procesamiento)
```

### Exportar archivos

```bash
# Exportar archivo específico
python3 cli.py export mydisk.dsk "PROGRAM.BAS" -o program.bas

# Exportar sin cabecera AMSDOS
python3 cli.py export mydisk.dsk "CODE.BIN" -o code.bin --no-header

# Exportar todos los archivos a un directorio
python3 cli.py export mydisk.dsk --all -o ./extracted_files

# Exportar de usuario específico
python3 cli.py export mydisk.dsk "FILE.TXT" --user 10

# Aliases disponibles:
python3 cli.py get mydisk.dsk "FILE.BIN"      # Alias de export
python3 cli.py extract mydisk.dsk --all       # Alias de export
```

### Renombrar archivos

```bash
# Renombrar archivo
python3 cli.py rename mydisk.dsk "OLD.BAS" --to "NEW.BAS"

# Renombrar en usuario específico
python3 cli.py rename mydisk.dsk "FILE.TXT" --to "RENAMED.TXT" --user 10

# Ver directorio después de renombrar
python3 cli.py rename mydisk.dsk "PROGRAM.BAS" --to "MAIN.BAS" -v

# Aliases disponibles:
python3 cli.py mv mydisk.dsk "OLD.BIN" --to "NEW.BIN"      # Alias de rename
python3 cli.py move mydisk.dsk "FILE.DAT" --to "DATA.DAT"  # Alias de rename
```

### Eliminar archivos

```bash
# Eliminar un archivo
python3 cli.py delete mydisk.dsk "OLDFILE.BAS"

# Eliminar múltiples archivos
python3 cli.py delete mydisk.dsk "FILE1.BAS" "FILE2.BAS" "FILE3.BIN"

# Eliminar de usuario específico
python3 cli.py delete mydisk.dsk "FILE.TXT" --user 10

# Ver directorio después de eliminar
python3 cli.py delete mydisk.dsk "TEMP.DAT" -v

# Aliases disponibles:
python3 cli.py remove mydisk.dsk "FILE.BIN"   # Alias de delete
python3 cli.py rm mydisk.dsk "OLD.DAT"        # Alias de delete
python3 cli.py del mydisk.dsk "TRASH.TMP"     # Alias de delete
```

### Visualizar programas BASIC

```bash
# Ver programa BASIC (auto-detecta formato tokenizado o ASCII)
python3 cli.py basic demo_8bp_v41_004.dsk "DEMO1.BAS"

# Ver múltiples archivos
python3 cli.py basic demo_8bp_v41_004.dsk "DEMO1.BAS" "DEMO2.BAS"

# Ver BASIC de usuario específico
python3 cli.py basic mydisk.dsk "FILE.BAS" --user 10

# Forzar visualización incluso si parece binario
python3 cli.py basic mydisk.dsk "DATA.BAS" --force

# Aliases disponibles:
python3 cli.py view demo_8bp_v41_004.dsk "DEMO1.BAS"   # Alias de basic
python3 cli.py show demo_8bp_v41_004.dsk "DEMO2.BAS"   # Alias de basic
python3 cli.py cat demo_8bp_v41_004.dsk "DEMO3.BAS"    # Alias de basic

# El comando detecta automáticamente:
# - BASIC tokenizado (formato CPC con tokens 0x80-0xFF)
# - BASIC ASCII (texto plano con números de línea)
# - Archivos binarios (los omite automáticamente)

# Ejemplo completo: crear DSK, importar BASIC y visualizar
python3 cli.py new test.dsk
echo -e '10 PRINT "HELLO"\n20 END' > test.bas
python3 cli.py import test.dsk test.bas --type 2
python3 cli.py basic test.dsk "TEST.BAS"
```

### Detectar tipo de archivo

```bash
# Mostrar tipo de archivo (BASIC-TOKENIZED/BASIC-ASCII/BINARY/ASCII/RAW/DELETED)
python3 cli.py filetype demo_8bp_v41_004.dsk "DEMO1.BAS"
# Salida: DEMO1.BAS: BASIC-TOKENIZED

# Verificar múltiples archivos
python3 cli.py filetype demo_8bp_v41_004.dsk "DEMO1.BAS" "8bp.bin" "LOADER.BAS"
# Salida:
# DEMO1.BAS: BASIC-TOKENIZED
# 8bp.bin: BINARY
# LOADER.BAS: BASIC-TOKENIZED

# Verificar archivos de usuario específico
python3 cli.py filetype mydisk.dsk "FILE.BAS" --user 10

# Tipos de archivo detectados:
# - BASIC-TOKENIZED: Programa BASIC en formato tokenizado
# - BASIC-ASCII: Programa BASIC en formato ASCII/texto
# - BINARY: Archivo binario ejecutable
# - ASCII: Archivo de texto ASCII
# - RAW: Archivo sin formato reconocible
# - DELETED: Archivo marcado como eliminado
```

## Uso desde Python

### Ejemplo básico

```python
from pydsk import DSK

# Crear nueva imagen DSK
dsk = DSK()
dsk.create(nb_tracks=40, nb_sectors=9, format_type=DSK.FORMAT_DATA)
dsk.save("mydisk.dsk")

# Cargar imagen existente
dsk = DSK("mydisk.dsk")
info = dsk.get_info()
print(f"Capacidad: {info['capacity_kb']} KB")

# Listar archivos (usa Rich automáticamente si está disponible)
dsk.list_files()  # Formato con colores y bordes redondeados

# Listar sin Rich (formato tradicional ASCII)
print(dsk.list_files(use_rich=False))

# Formato simple sin tabla
print(dsk.list_files(simple=True))
```

### Más ejemplos

Ver el archivo `examples.py` para más ejemplos de uso:

```bash
python3 examples.py
```

## API de la clase DSK

### Crear nueva imagen

```python
dsk = DSK()
dsk.create(
    nb_tracks=40,              # Número de pistas (1-84)
    nb_sectors=9,              # Sectores por pista (1-10)
    format_type=DSK.FORMAT_DATA  # DATA, SYSTEM o VENDOR
)
dsk.save("output.dsk")
```

### Cargar imagen existente

```python
# Cargar DSK existente
dsk = DSK("input.dsk")

# Manejo de errores si el archivo no existe
from pydsk.exceptions import DSKFileNotFoundError

try:
    dsk = DSK("myfile.dsk")
except DSKFileNotFoundError as e:
    print(f"Error: {e}")
```

### Listar archivos

```python
# Con Rich (por defecto) - bordes redondeados, colores, tipo de archivo
dsk.list_files()

# Formato tradicional ASCII sin colores
listing = dsk.list_files(use_rich=False)
print(listing)

# Formato simple (columnas)
listing = dsk.list_files(simple=True)
print(listing)
```

### Obtener información

```python
info = dsk.get_info()
# Retorna dict con: filename, format, tracks, heads, track_size, total_size, capacity_kb

formato = dsk.get_format_type()  # 'DATA', 'SYSTEM', 'VENDOR'
min_sector = dsk.get_min_sector()  # 0xC1, 0x41, 0x01
```

### Importar archivos

```python
# Importar archivo BASIC ASCII
dsk.write_file(
    'program.bas',
    file_type=2,  # BASIC ASCII
    user=0
)

# Importar binario con direcciones
dsk.write_file(
    'code.bin',
    file_type=0,
    load_addr=0x8000,
    exec_addr=0x8000
)
```

### Exportar archivos

```python
# Exportar archivo específico con cabecera
data = dsk.read_file('PROGRAM.BIN', keep_header=True)
with open('program.bin', 'wb') as f:
    f.write(data)

# Exportar sin cabecera AMSDOS
data = dsk.read_file('CODE.BIN', keep_header=False)

# Exportar directamente a archivo
dsk.export_file('PROGRAM.BIN', 'output/program.bin', keep_header=False)

# Exportar todos los archivos
# Exportar todos los archivos
dsk.export_all('output_dir/', keep_header=False)

# Renombrar archivos
dsk.rename_file('OLD.BAS', 'NEW.BAS')

# Renombrar en usuario específico
dsk.rename_file('FILE.TXT', 'RENAMED.TXT', user=10)

# Eliminar archivos
extents = dsk.delete_file('OLDFILE.BAS')
print(f"{extents} extent(s) eliminado(s)")

# Eliminar en usuario específico
dsk.delete_file('FILE.DAT', user=10)
```

### Visualizar programas BASIC

```python
from pydsk.basic_viewer import view_basic, detect_basic_format

# Leer archivo BASIC del DSK (sin cabecera AMSDOS)
data = dsk.read_file('PROGRAM.BAS', keep_header=False)

# Detectar formato
is_tokenized, description = detect_basic_format(data)
print(f"Formato: {description}")

# Visualizar programa
try:
    listing = view_basic(data, auto_detect=True)
    print(listing)
except ValueError as e:
    print(f"Error: {e}")

# Forzar formato específico
from pydsk.basic_viewer import view_basic_ascii, detokenize_basic

# ASCII
if not is_tokenized:
    listing = view_basic_ascii(data)
    
# Tokenizado
else:
    listing = detokenize_basic(data)
```

## Estructura del Proyecto

# Importar con atributos especiales
dsk.write_file(
    'system.bas',
    file_type=2,
    user=0,
    system=True,         # Archivo de sistema
    read_only=True,      # Solo lectura
    force=True           # Sobrescribir si existe
)

# Cambiar nombre en el DSK
dsk.write_file(
    '/path/to/myfile.txt',
    dsk_filename='DATA.BIN',  # Nombre en el DSK
    file_type=0,
    user=0
)

# Guardar cambios
dsk.save("mydisk.dsk")
```

### Listar archivos

```python
# Formato tabla profesional
print(dsk.list_files(simple=False))

# Formato simple (columnas)
print(dsk.list_files(simple=True))

# Obtener entradas del directorio
entries = dsk.get_directory_entries()
for entry in entries:
    if not entry.is_deleted:
        print(f"{entry.full_name} - User {entry.user}")

# Calcular espacio libre
free_kb = dsk.get_free_space()
print(f"Espacio libre: {free_kb} KB")
```

## Formatos soportados

### DATA Format (0xC1)
- Formato estándar para datos
- Sectores comienzan en 0xC1
- Más común

### SYSTEM Format (0x41)
- Formato para discos de sistema
- Sectores comienzan en 0x41
- Reserva pistas iniciales

### VENDOR Format (0x01)
- Formato de fabricante
- Sectores comienzan en 0x01

### Gestión de cabeceras AMSDOS en archivos externos

PyDSK permite añadir y eliminar cabeceras AMSDOS en archivos fuera de imágenes DSK. Esto es útil para preparar archivos antes de importarlos o para procesar archivos exportados.

```python
# Añadir cabecera AMSDOS a un archivo externo
DSK.add_amsdos_header(
    input_file='program.bin',
    output_file='program_cpc.bin',
    load_addr=0x4000,    # Dirección de carga
    exec_addr=0x4000,    # Dirección de ejecución
    file_type=0,         # 0=binario, 1=BASIC protegido, 2=BASIC ASCII, 3=binario protegido
    force=True           # Sobrescribir si existe
)

# Eliminar cabecera AMSDOS de un archivo externo
DSK.remove_amsdos_header(
    input_file='exported.bin',
    output_file='clean.bin',
    force=True
)

# Ejemplo de uso con direcciones automáticas
DSK.add_amsdos_header(
    'program.bas',
    'program_cpc.bas',
    load_addr=0,    # 0 = AUTO (0x0170 para BASIC, 0x4000 para binario)
    exec_addr=0,    # 0 = AUTO (igual que load_addr)
    file_type=2     # BASIC ASCII
)
```

#### Comandos CLI para cabeceras externas

```bash
# Añadir cabecera a archivo binario
python -m pydsk.cli add-header input.bin output.bin -l 0x4000 -e 0x4000 -t 0

# Añadir cabecera a BASIC ASCII (direcciones automáticas)
python -m pydsk.cli add-header program.bas program_cpc.bas -t 2

# Eliminar cabecera de archivo
python -m pydsk.cli remove-header exported.bin clean.bin

# Opciones disponibles
# -l, --load : Dirección de carga (hex o decimal, 0=auto)
# -e, --exec : Dirección de ejecución (hex o decimal, 0=auto)
# -t, --type : Tipo de archivo (0-3)
# -f, --force: Sobrescribir si existe
```

## Estructura del proyecto

```
pydsk/
├── __init__.py       # Módulo principal
├── dsk.py            # Clase DSK principal
├── structures.py     # Estructuras de datos (CPCEMUHeader, etc.)
├── exceptions.py     # Excepciones personalizadas
├── cli.py            # Interfaz de línea de comandos
├── basic_viewer.py   # Visualizador de programas BASIC
├── README.md         # Esta documentación
└── ejemplos/         # Ejemplos de uso
    ├── 01_crear_dsk.py
    ├── 02_listar_archivos.py
    ├── 03_informacion_dsk.py
    ├── 04_importar_archivos.py
    ├── 05_exportar_archivos.py
    ├── 06_renombrar_archivos.py
    ├── 07_eliminar_archivos.py
    ├── 08_visualizar_basic.py
    ├── 09_detectar_tipo_archivo.py
    └── 10_cabecera_amsdos_externa.py
```

## Especificaciones técnicas

- **Formato**: CPCEMU DSK (estándar y extendido)
- **Tamaño de sector**: 512 bytes
- **Pistas**: 1-84 (típicamente 40 o 42)
- **Sectores por pista**: 1-10 (típicamente 9)
- **Capacidad típica**: 178 KB (40 pistas × 9 sectores × 512 bytes)
- **Entrelazado de sectores**: Implementado (0, 5, 1, 6, 2, 7, 3, 8, 4)

## Características implementadas

- [x] Crear imágenes DSK vacías (DATA/SYSTEM/VENDOR)
- [x] Listar archivos del directorio AMSDOS
- [x] Importar archivos al DSK
- [x] Exportar archivos del DSK
- [x] Renombrar archivos (con soporte de extents)
- [x] Eliminar archivos
- [x] Visualizar programas BASIC (ASCII y tokenizado)
- [x] Detectar tipo de archivo (BASIC/ASCII/BINARY/RAW/DELETED)
- [x] Información detallada del DSK
- [x] Soporte completo de cabeceras AMSDOS
- [x] Añadir/eliminar cabeceras AMSDOS en archivos externos
- [x] Gestión de múltiples usuarios (0-15)
- [x] CLI completo compatible con iDSK
- [x] Formato Rich con bordes redondeados y colores

## Próximas características

- [ ] Desfragmentación de disco
- [ ] Soporte para imágenes DSK extendidas
- [ ] Conversión entre formatos
- [ ] Protección de archivos
- [ ] Recuperación de archivos eliminados

## Licencia

GPL - Compatible con el proyecto original iDSK

## Autor

CPCReady - 2025
