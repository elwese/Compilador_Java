import ply.lex as lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'class': 'CLASS',
    'public': 'PUBLIC',
    'private': 'PRIVATE',
    'return': 'RETURN',

    'int': 'INT',
    'float': 'FLOAT',
    'double': 'DOUBLE',
    'long': 'LONG',
    'short': 'SHORT',
    'byte': 'BYTE',
    'char': 'CHAR',
    'boolean': 'BOOLEAN',

    'true': 'BOOLEAN_LITERAL',
    'false': 'BOOLEAN_LITERAL'
}

tokens = [
    'IDENTIFIER',

    'INTEGER_LITERAL',
    'FLOAT_LITERAL',
    'CHAR_LITERAL',
    'STRING_LITERAL',

    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MOD',

    'ASSIGN',
    'PLUS_ASSIGN',
    'MINUS_ASSIGN',
    'TIMES_ASSIGN',
    'DIVIDE_ASSIGN',
    'MOD_ASSIGN',

    'EQ',
    'NE',
    'LT',
    'GT',
    'LE',
    'GE',

    'AND',
    'OR',
    'NOT',

    'INCREMENT',
    'DECREMENT',

    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',

    'SEMICOLON',
    'COMMA',
    'DOT',
    'COLON',

    'COMMENT',
    'MULTILINE_COMMENT'
    ,
    # Tokens añadidos por Jonathan Pacalla
    'BIT_AND',
    'BIT_OR',
    'BIT_XOR',
    'LSHIFT',
    'RSHIFT',
    'BIT_NOT',
    'QUESTION'
] + list(reserved.values())

# Comentarios generales de los tokens:
# - Identificadores y literales: representan nombres y valores primitivos.
# - Operadores aritméticos, lógicos y bitwise: símbolos que realizan operaciones.
# - Asignaciones: operadores = y variantes compuestas (+=, -=, ...).
# - Comparadores: ==, !=, <, >, <=, >=.
# - Delimitadores: paréntesis, llaves, corchetes, punto y coma, coma, punto.
# - Comentarios: tokens para comentarios de línea y multilínea.

#Inicio tokens Cesar Delgado
# IDENTIFIER: identificadores (variables, métodos); mapea palabras reservadas
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

# FLOAT_LITERAL: números con punto decimal (ej. 3.14)
def t_FLOAT_LITERAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t
# INTEGER_LITERAL: números enteros (ej. 42)
def t_INTEGER_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t
# CHAR_LITERAL: carácter entre comillas simples (ej. 'a')
def t_CHAR_LITERAL(t):
    r"'.'"
    return t
# STRING_LITERAL: cadena entre comillas dobles; permite escapes
def t_STRING_LITERAL(t):
    r'"([^\\\n]|(\\.))*?"'
    return t

def t_newline(t):
    r'\n+'
    # Actualiza número de línea para el lexer
    t.lexer.lineno += len(t.value)


# INCREMENT / DECREMENT: operadores ++ y --
def t_INCREMENT(t):
    r'\+\+'
    return t
def t_DECREMENT(t):
    r'--'
    return t

# ASSIGNMENTS compuestas: +=, -=, etc. (PLUS_ASSIGN, MINUS_ASSIGN...)
def t_PLUS_ASSIGN(t):
    r'\+='
    return t
def t_MINUS_ASSIGN(t):
    r'-='
    return t

# EQ / NE / LE / GE: comparadores de igualdad y orden
def t_EQ(t):
    r'=='
    return t
def t_NE(t):
    r'!='
    return t
def t_LE(t):
    r'<='
    return t
def t_GE(t):
    r'>='
    return t

# Operadores aritméticos básicos
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_MOD    = r'%'

# Fin tokens Cesar Delgado


# Inicio tokens Jose Salazar


# Asignación y asignaciones compuestas
t_ASSIGN       = r'='
t_TIMES_ASSIGN = r'\*='
t_DIVIDE_ASSIGN = r'/='
t_MOD_ASSIGN   = r'%='

# Comparadores simples
t_LT = r'<'
t_GT = r'>'

# Operadores lógicos
t_AND = r'&&'
t_OR  = r'\|\|'
t_NOT = r'!'



# Delimitadores: paréntesis, llaves y corchetes
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_LBRACE   = r'\{'
t_RBRACE   = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

# Puntuación y separadores
t_SEMICOLON = r';'
t_COMMA     = r','
t_DOT       = r'\.'
t_COLON     = r':'

# Ignorar espacios y tabulaciones
t_ignore = ' \t'


def t_COMMENT(t):
    r'//.*'
    # Comentario de línea (// ...). Se devuelve en caso de querer procesarlo.
    return t

def t_MULTILINE_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    # Comentario multilínea (/* ... */)
    return t

# Fin tokens Jose Salazar 


def t_error(t):
    # Manejo de error léxico: reporta carácter ilegal y avanza 1 posición
    print(f"Caracter ilegal '{t.value[0]}' en linea {t.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()

# Inicio tokens Jonathan Pacalla
t_BIT_AND = r'&'
t_BIT_OR = r'\|'
t_BIT_XOR = r'\^'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_BIT_NOT = r'~'
t_QUESTION = r'\?'
# Fin tokens Jonathan Pacalla
