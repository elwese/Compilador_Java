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
] + list(reserved.values())

#Inicio tokens Cesar Delgado
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_FLOAT_LITERAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t
def t_INTEGER_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t
def t_CHAR_LITERAL(t):
    r"'.'"
    return t
def t_STRING_LITERAL(t):
    r'"([^\\\n]|(\\.))*?"'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_INCREMENT(t):
    r'\+\+'
    return t
def t_DECREMENT(t):
    r'--'
    return t
def t_PLUS_ASSIGN(t):
    r'\+='
    return t
def t_EQ(t):
    r'=='
    return t
def t_GE(t):
    r'>='
    return t
def t_MINUS_ASSIGN(t):
    r'-='
    return t
def t_LE(t):
    r'<='
    return t
def t_NE(t):
    r'!='
    return t

t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_MOD    = r'%'

# Fin tokens Cesar Delgado

t_ASSIGN       = r'='
t_TIMES_ASSIGN = r'\*='
t_DIVIDE_ASSIGN = r'/='
t_MOD_ASSIGN   = r'%='

t_LT = r'<'
t_GT = r'>'

t_AND = r'&&'
t_OR  = r'\|\|'
t_NOT = r'!'


t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_LBRACE   = r'\{'
t_RBRACE   = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

t_SEMICOLON = r';'
t_COMMA     = r','
t_DOT       = r'\.'
t_COLON     = r':'

t_ignore = ' \t'

def t_COMMENT(t):
    r'//.*'
    return t

def t_MULTILINE_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    return t

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}' en linea {t.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()