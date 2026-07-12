import ply.yacc as yacc
from javalex import tokens

# 1. Definición de Precedencia de Operadores
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NE'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'NOT', 'INCREMENT', 'DECREMENT'),
)

# 2. Regla inicial (El programa principal)
def p_program(p):
    '''program : statements'''
    p[0] = p[1]

def p_statements(p):
    '''statements : statements statement
                  | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# 3. Tipos de Sentencias Soportadas
def p_statement(p):
    '''statement : var_declaration
                 | assignment
                 | if_statement
                 | while_statement
                 | for_statement
                 | method_declaration
                 | print_statement'''
    p[0] = p[1]

# 4. Declaración de Variables (Ej: int contador = 10;)
def p_var_declaration(p):
    '''var_declaration : type IDENTIFIER ASSIGN expression SEMICOLON
                       | type IDENTIFIER SEMICOLON'''
    if len(p) == 6:
        p[0] = ('var_decl', p[1], p[2], p[4])
    else:
        p[0] = ('var_decl', p[1], p[2], None)

# Tipos de datos primitivos
def p_type(p):
    '''type : INT
            | FLOAT
            | DOUBLE
            | BOOLEAN
            | CHAR
            | IDENTIFIER''' # IDENTIFIER cubre "String" y clases
    p[0] = p[1]

# 5. Declaración de Arreglos (Ej: int[] calificaciones = new int[5];)
def p_var_declaration_array(p):
    '''var_declaration : type LBRACKET RBRACKET IDENTIFIER ASSIGN IDENTIFIER type LBRACKET expression RBRACKET SEMICOLON
                       | type LBRACKET RBRACKET IDENTIFIER ASSIGN LBRACE expression_list RBRACE SEMICOLON'''
    p[0] = ('array_decl', p[2]) # Simplificado para el AST

# 6. Asignaciones simples (Ej: suma = suma + i;)
def p_assignment(p):
    '''assignment : IDENTIFIER ASSIGN expression SEMICOLON
                  | IDENTIFIER PLUS_ASSIGN expression SEMICOLON
                  | IDENTIFIER MINUS_ASSIGN expression SEMICOLON'''
    p[0] = ('assign', p[2], p[1], p[3])

# 7. Expresiones Matemáticas, Lógicas y Literales
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MOD expression
                  | expression EQ expression
                  | expression NE expression
                  | expression LT expression
                  | expression GT expression
                  | expression LE expression
                  | expression GE expression
                  | expression AND expression
                  | expression OR expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_unary(p):
    '''expression : NOT expression
                  | MINUS expression %prec TIMES'''
    p[0] = ('unary', p[1], p[2])

def p_expression_literal(p):
    '''expression : INTEGER_LITERAL
                  | FLOAT_LITERAL
                  | STRING_LITERAL
                  | BOOLEAN_LITERAL
                  | CHAR_LITERAL
                  | IDENTIFIER'''
    p[0] = p[1]

def p_expression_list(p):
    '''expression_list : expression_list COMMA expression
                       | expression'''
    pass # Lógica de concatenación omitida para brevedad

# 8. Estructuras de Control (If / Else)
def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN LBRACE statements RBRACE
                    | IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE'''
    if len(p) == 8:
        p[0] = ('if', p[3], p[6])
    else:
        p[0] = ('if_else', p[3], p[6], p[10])

# 9. Bucles (While y For)
def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN LBRACE statements RBRACE'''
    p[0] = ('while', p[3], p[6])

def p_for_statement(p):
    '''for_statement : FOR LPAREN var_declaration expression SEMICOLON assignment_no_semi RPAREN LBRACE statements RBRACE'''
    p[0] = ('for', p[3], p[4], p[6], p[9])

def p_assignment_no_semi(p):
    '''assignment_no_semi : IDENTIFIER ASSIGN expression'''
    p[0] = ('assign', p[2], p[1], p[3])

# 10. Métodos (Ej: public int calcularSuma(int a, int b) { ... })
def p_method_declaration(p):
    '''method_declaration : modifier type IDENTIFIER LPAREN parameters RPAREN LBRACE statements RBRACE'''
    p[0] = ('method', p[1], p[2], p[3], p[5], p[8])

def p_modifier(p):
    '''modifier : PUBLIC
                | PRIVATE
                | empty'''
    p[0] = p[1]

def p_parameters(p):
    '''parameters : parameters COMMA type IDENTIFIER
                  | type IDENTIFIER
                  | empty'''
    pass 

# 11. Impresión de consola (System.out.println)
def p_print_statement(p):
    '''print_statement : IDENTIFIER DOT IDENTIFIER DOT IDENTIFIER LPAREN expression RPAREN SEMICOLON'''
    # Validar semánticamente después si es "System.out.println"
    p[0] = ('print', p[7])

# Regla de manejo de errores sintácticos
def p_error(p):
    if p:
        print(f"Error de sintaxis en el token '{p.value}', línea {p.lineno}")
    else:
        print("Error de sintaxis: Fin de archivo inesperado (EOF)")

def p_empty(p):
    '''empty :'''
    pass

# Instanciación del parser
parser = yacc.yacc()

# Bloque de prueba simple
if __name__ == '__main__':
    data = '''
    int contador = 10;
    if (contador > 0) {
        System.out.println("Es positivo");
    }
    '''
    result = parser.parse(data)
    print("Árbol de Sintaxis Abstracta (AST):")
    print(result)

 

# Del 1 al 3 (documentacion) José, del 4 al 7 Jonathan y del 8 al 10 incluyendo comentarios con instansiacion del parser Cesar