#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Validador del Analizador Léxico - JONATHAN PACALLA
Genera logs con los tokens reconocidos y/o errores
"""

import sys
from datetime import datetime
from javalex import lexer

# Nombre y apellido del estudiante
NOMBRE_APELLIDO = "JonathanPacalla"

# Obtener fecha y hora actual en formato: DD-MM-AAAA-HHhMM
ahora = datetime.now()
fecha_hora = ahora.strftime("%d-%m-%Y-%Hh%M")

# Nombre del archivo log
archivo_log = f"lexico-{NOMBRE_APELLIDO}-{fecha_hora}.txt"

# Leer el archivo Java a validar
archivo_java = "PruebaJonathanPacalla.java"

try:
    with open(archivo_java, 'r', encoding='utf-8') as f:
        codigo_fuente = f.read()
except FileNotFoundError:
    print(f"Error: No se encontró el archivo '{archivo_java}'")
    sys.exit(1)

# Crear contenido del log
log_content = []
log_content.append("=" * 80)
log_content.append("VALIDACIÓN DEL ANALIZADOR LÉXICO - JONATHAN PACALLA")
log_content.append("=" * 80)
log_content.append(f"Fecha y Hora: {ahora.strftime('%d de %B de %Y - %H:%M:%S')}")
log_content.append(f"Archivo Analizado: {archivo_java}")
log_content.append(f"Tokens del Integrante: Palabras reservadas (IF, ELSE, FOR, WHILE, CLASS, PUBLIC, PRIVATE, RETURN, INT, FLOAT, DOUBLE, LONG, SHORT, BYTE, CHAR, BOOLEAN, BOOLEAN_LITERAL), Operadores Bitwise (BIT_AND, BIT_OR, BIT_XOR, LSHIFT, RSHIFT, BIT_NOT), Operador Ternario (QUESTION)")
log_content.append("=" * 80)

log_content.append("\n[CÓDIGO FUENTE ANALIZADO]")
log_content.append("-" * 80)
log_content.append(codigo_fuente)
log_content.append("-" * 80)

# Pasar el código al lexer
lexer.input(codigo_fuente)

# Recolectar tokens y errores
tokens_encontrados = []
errores = []

log_content.append("\n[TOKENS RECONOCIDOS]")
log_content.append("-" * 80)
log_content.append(f"{'Línea':<8} {'Tipo de Token':<20} {'Valor':<25} {'Descripción'}")
log_content.append("-" * 80)

while True:
    tok = lexer.token()
    if not tok:
        break
    
    tokens_encontrados.append({
        'tipo': tok.type,
        'valor': str(tok.value),
        'linea': tok.lineno
    })
    
    # Descripción del token
    descripcion_tokens = {
        'IDENTIFIER': 'Identificador (variable/función)',
        'ASSIGN': 'Operador de asignación (=)',
        'INTEGER_LITERAL': 'Literal entero',
        'SEMICOLON': 'Punto y coma',
        'LPAREN': 'Paréntesis de apertura',
        'RPAREN': 'Paréntesis de cierre',
        'LBRACE': 'Llave de apertura',
        'RBRACE': 'Llave de cierre',
        'DOT': 'Punto',
        'PLUS': 'Operador suma (+)',
        'COMMA': 'Coma',
        'BIT_AND': 'Operador AND bitwise (&)',
        'BIT_OR': 'Operador OR bitwise (|)',
        'BIT_XOR': 'Operador XOR bitwise (^)',
        'BIT_NOT': 'Operador NOT bitwise (~)',
        'LSHIFT': 'Desplazamiento izquierda (<<)',
        'RSHIFT': 'Desplazamiento derecha (>>)',
        'QUESTION': 'Operador ternario (?)',
        'COLON': 'Dos puntos',
        'GT': 'Mayor que (>)',
        'STRING_LITERAL': 'Literal de cadena',
    }
    
    # Palabras reservadas
    reservadas = {
        'IF': 'Palabra reservada: if',
        'ELSE': 'Palabra reservada: else',
        'FOR': 'Palabra reservada: for',
        'WHILE': 'Palabra reservada: while',
        'CLASS': 'Palabra reservada: class',
        'PUBLIC': 'Palabra reservada: public',
        'PRIVATE': 'Palabra reservada: private',
        'RETURN': 'Palabra reservada: return',
        'INT': 'Palabra reservada: tipo int',
        'FLOAT': 'Palabra reservada: tipo float',
        'DOUBLE': 'Palabra reservada: tipo double',
        'LONG': 'Palabra reservada: tipo long',
        'SHORT': 'Palabra reservada: tipo short',
        'BYTE': 'Palabra reservada: tipo byte',
        'CHAR': 'Palabra reservada: tipo char',
        'BOOLEAN': 'Palabra reservada: tipo boolean',
        'BOOLEAN_LITERAL': 'Literal booleano (true/false)',
    }
    
    descripcion = descripcion_tokens.get(tok.type, reservadas.get(tok.type, 'Token desconocido'))
    
    log_content.append(f"{tok.lineno:<8} {tok.type:<20} {str(tok.value):<25} {descripcion}")

log_content.append("-" * 80)
log_content.append(f"\nTotal de tokens reconocidos: {len(tokens_encontrados)}")

# Sección de errores (si los hay)
if errores:
    log_content.append("\n[ERRORES LÉXICOS DETECTADOS]")
    log_content.append("-" * 80)
    for error in errores:
        log_content.append(error)
    log_content.append("-" * 80)
else:
    log_content.append("\n[ERRORES LÉXICOS DETECTADOS]")
    log_content.append("-" * 80)
    log_content.append("✓ No se detectaron errores léxicos")
    log_content.append("-" * 80)

# Resumen
log_content.append("\n[RESUMEN]")
log_content.append("-" * 80)
log_content.append(f"Tokens reconocidos: {len(tokens_encontrados)}")
log_content.append(f"Errores encontrados: {len(errores)}")
log_content.append("Estado: ✓ ANÁLISIS COMPLETADO EXITOSAMENTE" if len(errores) == 0 else "Estado: ✗ ANÁLISIS CON ERRORES")
log_content.append("-" * 80)
log_content.append(f"Generado: {ahora.strftime('%d de %B de %Y a las %H:%M:%S')}")
log_content.append("=" * 80)

# Escribir el log
contenido_log = "\n".join(log_content)

try:
    with open(archivo_log, 'w', encoding='utf-8') as f:
        f.write(contenido_log)
    
    print(f"\n✓ Log generado exitosamente: {archivo_log}\n")
    print(contenido_log)
    
except IOError as e:
    print(f"Error al escribir el archivo log: {e}")
    sys.exit(1)
