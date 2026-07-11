import ply.lex as lex

# 1. Palabras reservadas de Java
reserved = {
    'public': 'PUBLIC',
    'private': 'PRIVATE',
    'protected': 'PROTECTED',
    'class': 'CLASS',
    'static': 'STATIC',
    'void': 'VOID',
    'main': 'MAIN',
    'int': 'INT_TYPE',
    'double': 'DOUBLE_TYPE',
    'boolean': 'BOOLEAN_TYPE',
    'String': 'STRING_TYPE',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'true': 'TRUE',
    'false': 'FALSE'
}



# 2. Lista completa de nombres de tokens
tokens = [
    'ID', 'INT_LITERAL', 'DOUBLE_LITERAL', 'STRING_LITERAL',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN',
    'EQUALS', 'NE', 'GREATER', 'LESS', 'GE', 'LE',
    'AND', 'OR', 'NOT',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACK', 'RBRACK',
    'SEMI', 'COMMA'
] + list(reserved.values())

# 3. Expresiones regulares para operadores y puntuación simple
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_EQUALS = r'=='
t_NE = r'!='
t_GREATER = r'>'
t_LESS = r'<'
t_GE = r'>='
t_LE = r'<='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_SEMI = r';'
t_COMMA = r','

# Codigo Cesar Delgado

# 4. Reglas léxicas para Literales complejos
def t_DOUBLE_LITERAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Extrae el texto quitando las comillas
    return t

# Codigo Jonathan Pacalla

# 5. Identificadores y enlace con palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Si es reservada cambia el tipo, si no, se queda como ID
    return t

# 6. IGNORAR COMENTARIOS (No generan tokens)
def t_SINGLE_COMMENT(t):
    r'//.*'
    pass  # Se descarta la línea del comentario

def t_MULTILINE_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    # Contamos los saltos de línea internos para no perder el rastro de la línea actual
    t.lexer.lineno += t.value.count('\n')
    pass  # Se descarta el bloque del comentario

# Codigo Jose Salazar
# 7. Rastreo de números de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar espacios en blanco y tabulaciones
t_ignore = ' \t'

# Lista global para capturar y reportar los errores de esta fase
lex_errors = []

def t_error(t):
    error_msg = f"Línea {t.lexer.lineno}: Carácter ilegal '{t.value[0]}'"
    lex_errors.append(error_msg)
    t.lexer.skip(1)

# Constructor del Lexer
lexer = lex.lex()