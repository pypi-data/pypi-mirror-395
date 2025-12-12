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
Módulo para visualización de programas BASIC de Amstrad CPC
Soporta detokenización de BASIC tokenizado y muestra de BASIC ASCII
"""

from typing import Optional, Tuple

# Tabla de comandos BASIC (0x80-0xFF, índice 0-0x7F)
# Basado en el código C++ de iDSK
BASIC_TOKENS = [
    "AFTER", "AUTO", "BORDER", "CALL", "CAT", "CHAIN", "CLEAR", "CLG",
    "CLOSEIN", "CLOSEOUT", "CLS", "CONT", "DATA", "DEF", "DEFINT",
    "DEFREAL", "DEFSTR", "DEG", "DELETE", "DIM", "DRAW", "DRAWR", "EDIT",
    "ELSE", "END", "ENT", "ENV", "ERASE", "ERROR", "EVERY", "FOR",
    "GOSUB", "GOTO", "IF", "INK", "INPUT", "KEY", "LET", "LINE", "LIST",
    "LOAD", "LOCATE", "MEMORY", "MERGE", "MID$", "MODE", "MOVE", "MOVER",
    "NEXT", "NEW", "ON", "ON BREAK", "ON ERROR GOTO", "SQ", "OPENIN",
    "OPENOUT", "ORIGIN", "OUT", "PAPER", "PEN", "PLOT", "PLOTR", "POKE",
    "PRINT", "'", "RAD", "RANDOMIZE", "READ", "RELEASE", "REM", "RENUM",
    "RESTORE", "RESUME", "RETURN", "RUN", "SAVE", "SOUND", "SPEED", "STOP",
    "SYMBOL", "TAG", "TAGOFF", "TROFF", "TRON", "WAIT", "WEND", "WHILE",
    "WIDTH", "WINDOW", "WRITE", "ZONE", "DI", "EI", "FILL", "GRAPHICS",
    "MASK", "FRAME", "CURSOR", "#E2", "ERL", "FN", "SPC", "STEP", "SWAP",
    "#E8", "#E9", "TAB", "THEN", "TO", "USING", ">", "=", ">=", "<", "<>",
    "<=", "+", "-", "*", "/", "^", "\\ ", "AND", "MOD", "OR", "XOR", "NOT",
    "#FF"
]

# Tabla de funciones (0xFF + 0x00-0x7F)
# Basado en el código C++ de iDSK
BASIC_FUNCTIONS = [
    "ABS", "ASC", "ATN", "CHR$", "CINT", "COS", "CREAL", "EXP", "FIX",
    "FRE", "INKEY", "INP", "INT", "JOY", "LEN", "LOG", "LOG10", "LOWER$",
    "PEEK", "REMAIN", "SGN", "SIN", "SPACE$", "SQ", "SQR", "STR$", "TAN",
    "UNT", "UPPER$", "VAL", "", "", "", "", "", "", "", "", "", "", "",
    "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
    "", "", "", "", "", "", "EOF", "ERR", "HIMEM", "INKEY$", "PI", "RND",
    "TIME", "XPOS", "YPOS", "DERR", "", "", "", "", "", "", "", "", "", "",
    "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
    "", "", "", "", "", "", "", "", "", "", "", "BIN$", "DEC$", "HEX$",
    "INSTR", "LEFT$", "MAX", "MIN", "POS", "RIGHT$", "ROUND", "STRING$",
    "TEST", "TESTR", "COPYCHR$", "VPOS"
]


def detect_basic_format(data: bytes) -> Tuple[bool, str]:
    """
    Detecta si un archivo es BASIC tokenizado o ASCII.
    
    Args:
        data: Datos del archivo (sin cabecera AMSDOS)
        
    Returns:
        Tupla (es_tokenizado, descripción)
    """
    if len(data) < 4:
        return False, "Archivo demasiado pequeño"
    
    # BASIC tokenizado empieza con: [2 bytes longitud][2 bytes número línea]
    length = data[0] | (data[1] << 8)
    line_num = data[2] | (data[3] << 8)
    
    # Verificar si parece tokenizado
    looks_tokenized = (
        length > 4 and 
        length < len(data) and 
        line_num > 0 and 
        line_num < 65000
    )
    
    # Si empieza con dígito ASCII, probablemente es ASCII
    if data[0] >= ord('0') and data[0] <= ord('9'):
        return False, "BASIC ASCII"
    
    # Si parece tokenizado, validar que tenga estructura correcta
    if looks_tokenized:
        # Verificar que la primera línea termine en 0x00
        try:
            if length < len(data):
                # Buscar el terminador 0x00 de la primera línea
                has_terminator = False
                for i in range(4, min(length, len(data))):
                    if data[i] == 0x00:
                        has_terminator = True
                        break
                if has_terminator:
                    return True, "BASIC tokenizado"
        except:
            pass
    
    # Por defecto, asumir ASCII
    return False, "BASIC ASCII o texto"


def detokenize_basic(data: bytes) -> str:
    """
    Detokeniza un programa BASIC tokenizado de Amstrad CPC.
    Implementación basada en el código C++ de iDSK.
    
    Args:
        data: Datos del programa BASIC tokenizado (sin cabecera AMSDOS)
        
    Returns:
        str: Listado del programa BASIC
        
    Raises:
        ValueError: Si el formato no es válido
    """
    listing = []
    pos = 0
    
    while pos < len(data):
        # Leer longitud de línea (2 bytes, little-endian)
        if pos + 2 > len(data):
            break
            
        line_length = data[pos] | (data[pos + 1] << 8)
        pos += 2
        
        # Longitud 0 = fin del programa
        if line_length == 0:
            break
        
        # Leer número de línea (2 bytes, little-endian)
        if pos + 2 > len(data):
            break
            
        line_num = data[pos] | (data[pos + 1] << 8)
        pos += 2
        
        # Construir línea
        line = f"{line_num} "
        in_string = False
        
        while pos < len(data):
            token = data[pos]
            pos += 1
            
            if token == 0:  # Fin de línea
                break
            
            # Dentro de string, copiar literal
            if in_string:
                line += chr(token) if token < 128 else ' '
                if token == ord('"'):
                    in_string = False
                continue
            
            # Tokens de comandos (0x80-0xFE)
            if 0x80 <= token <= 0xFE:
                idx = token & 0x7F
                # Eliminar ':' antes de ELSE (token 0x97)
                if token == 0x97 and line.endswith(':'):
                    line = line[:-1]
                if idx < len(BASIC_TOKENS):
                    line += BASIC_TOKENS[idx]
                continue
            
            # Números pequeños (0x0E-0x18 = 0-10)
            if 0x0E <= token <= 0x18:
                line += str(token - 0x0E)
                continue
            
            # Caracteres imprimibles (0x20-0x7B)
            if 0x20 <= token < 0x7C:
                line += chr(token)
                if token == ord('"'):
                    in_string = True
                continue
            
            # Tokens especiales
            if token == 0x01:  # Separador ':'
                line += ':'
                
            elif token == 0x02:  # Variable entera (%)
                pos += 2  # Saltar dirección
                while pos < len(data):
                    b = data[pos]
                    pos += 1
                    line += chr(b & 0x7F)
                    if b & 0x80:
                        break
                line += '%'
                
            elif token == 0x03:  # Variable string ($)
                pos += 2
                while pos < len(data):
                    b = data[pos]
                    pos += 1
                    line += chr(b & 0x7F)
                    if b & 0x80:
                        break
                line += '$'
                
            elif token == 0x04:  # Variable float (!)
                pos += 2
                while pos < len(data):
                    b = data[pos]
                    pos += 1
                    line += chr(b & 0x7F)
                    if b & 0x80:
                        break
                line += '!'
                
            elif token in (0x0B, 0x0C, 0x0D):  # Variable estándar
                pos += 2
                while pos < len(data):
                    b = data[pos]
                    pos += 1
                    line += chr(b & 0x7F)
                    if b & 0x80:
                        break
                        
            elif token == 0x19:  # Entero 8-bit
                if pos < len(data):
                    line += str(data[pos])
                    pos += 1
                    
            elif token == 0x1A or token == 0x1E:  # Entero 16-bit decimal
                if pos + 1 < len(data):
                    val = data[pos] | (data[pos + 1] << 8)
                    # Convertir a signed si es negativo
                    if val >= 32768:
                        val = val - 65536
                    line += str(val)
                    pos += 2
                    
            elif token == 0x1B:  # Hexadecimal binario (&X)
                if pos + 1 < len(data):
                    val = data[pos] | (data[pos + 1] << 8)
                    line += f"&X{val:X}"
                    pos += 2
                    
            elif token == 0x1C:  # Hexadecimal (&)
                if pos + 1 < len(data):
                    val = data[pos] | (data[pos + 1] << 8)
                    line += f"&{val:X}"
                    pos += 2
                    
            elif token == 0x1F:  # Floating point (5 bytes)
                if pos + 4 < len(data):
                    # Leer mantisa (4 bytes) y exponente (1 byte)
                    mantissa = (data[pos] | 
                               (data[pos + 1] << 8) | 
                               (data[pos + 2] << 16) | 
                               ((data[pos + 3] & 0x7F) << 24))
                    f = 1.0 + (mantissa / 0x80000000)
                    
                    # Signo
                    if data[pos + 3] & 0x80:
                        f = -f
                    
                    # Exponente
                    exp = data[pos + 4] - 129
                    result = f * (2 ** exp)
                    
                    # Formatear eliminando ceros innecesarios
                    s = f"{result:f}"
                    s = s.rstrip('0').rstrip('.')
                    line += s
                    pos += 5
                    
            elif token == 0x7C:  # RSX (|comando)
                line += '|'
                pos += 1  # Saltar un byte
                while pos < len(data):
                    b = data[pos]
                    pos += 1
                    line += chr(b & 0x7F)
                    if b & 0x80:
                        break
                        
            elif token == 0xFF:  # Funciones extendidas
                if pos < len(data):
                    func_token = data[pos]
                    pos += 1
                    if func_token < 0x80:
                        # Funciones definidas
                        if func_token < len(BASIC_FUNCTIONS) and BASIC_FUNCTIONS[func_token]:
                            line += BASIC_FUNCTIONS[func_token]
                        else:
                            line += f"[FN#{func_token:02X}]"
                    else:
                        # Carácter especial
                        line += chr(func_token & 0x7F)
        
        listing.append(line.rstrip())
    
    return '\n'.join(listing)


def view_basic_ascii(data: bytes) -> str:
    """
    Muestra un programa BASIC en formato ASCII.
    
    Args:
        data: Datos del BASIC ASCII (sin cabecera AMSDOS)
        
    Returns:
        Contenido del programa
    """
    try:
        # Buscar el final real del programa (0x1A = EOF o secuencia de 0x00)
        end_pos = len(data)
        
        # Buscar EOF (Ctrl+Z)
        if 0x1A in data:
            end_pos = min(end_pos, data.index(0x1A))
        
        # Buscar secuencia larga de 0x00 (relleno)
        zero_count = 0
        for i, byte in enumerate(data):
            if byte == 0:
                zero_count += 1
                if zero_count >= 10:  # 10 ceros seguidos = fin
                    end_pos = min(end_pos, i - 9)
                    break
            else:
                zero_count = 0
        
        # Tomar solo hasta el final detectado
        text_data = data[:end_pos]
        
        # Intentar decodificar como ASCII/UTF-8
        text = text_data.decode('ascii', errors='replace')
        
        # Limpiar caracteres no imprimibles excepto newlines/tabs
        text = ''.join(c if c.isprintable() or c in '\n\r\t' else '' for c in text)
        
        return text.strip()
    except:
        return "[Error decodificando archivo]"


def view_basic(data: bytes, auto_detect: bool = True) -> str:
    """
    Visualiza un programa BASIC (auto-detecta formato).
    
    Args:
        data: Datos del archivo (sin cabecera AMSDOS)
        auto_detect: Si True, detecta automáticamente el formato
        
    Returns:
        Listado del programa
    """
    if auto_detect:
        is_tokenized, fmt = detect_basic_format(data)
        if is_tokenized:
            return detokenize_basic(data)
        else:
            return view_basic_ascii(data)
    else:
        # Intentar tokenizado primero
        try:
            return detokenize_basic(data)
        except:
            return view_basic_ascii(data)
