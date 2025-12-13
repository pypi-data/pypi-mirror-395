# PyDSK - Ejemplos de Uso

Esta carpeta contiene ejemplos prácticos de cómo utilizar la librería PyDSK.

## Ejemplos disponibles

### 01_crear_dsk.py
Muestra diferentes formas de crear imágenes DSK:
- Creación básica con configuración por defecto
- DSK con formato SYSTEM
- DSK de alta capacidad (80 pistas)
- Creación de colecciones de DSK
- DSK con diferentes tamaños
- Verificación de DSK creados

### 02_listar_archivos.py
Ejemplos de listado de archivos en DSK:
- Listado en formato tabla
- Listado simple en columnas
- Filtrado de archivos por extensión y usuario
- Estadísticas de uso de espacio
- Detalles de archivos individuales
- Comparación de múltiples DSK

### 03_informacion_dsk.py
Obtención de información de imágenes DSK:
- Información básica del DSK
- Análisis de formato
- Análisis completo de estructura
- Comparación de múltiples DSK en tabla

### 04_importar_archivos.py
Importación de archivos al DSK:
- Importar archivos BASIC en modo ASCII
- Importar binarios con direcciones load/exec
- Importar múltiples archivos
- Usar atributos (sistema, solo lectura)
- Sobrescribir archivos existentes (force)
- - Importar en diferentes áreas de usuario

### 05_exportar_archivos.py
Exportación de archivos desde DSK:
- Exportar archivo específico
- Exportar con/sin cabecera AMSDOS
- Exportar todos los archivos
- Exportar desde área de usuario específica
- Ciclo completo: crear→importar→exportar
- Analizar estructura de cabecera AMSDOS

### 06_renombrar_archivos.py
Renombrado de archivos en DSK:
- Renombrar archivo simple
- Validaciones (archivo no existe, nombre duplicado, nombre inválido)
- Cambiar solo la extensión
- Renombrar archivos con múltiples extents
- Renombrar en área de usuario específica
- Ciclo completo con renombrado

### 07_eliminar_archivos.py
Eliminación de archivos en DSK:
- Eliminar archivo simple
- Eliminar múltiples archivos de una vez
- Eliminar archivos con múltiples extents
- Validaciones (archivo no existe, archivo ya eliminado)
- Eliminar en área de usuario específica
- Ciclo completo de gestión con eliminación

```
