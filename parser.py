import ply.yacc as yacc
from javalex import tokens

# Clase contenedora del Árbol de Sintaxis Abstracta (AST)
class ASTNode:
    def __init__(self, type_node, children=None, value=None, lineno=None):
        self.type = type_node
        self.children = children if children else []
        self.value = value
        self.lineno = lineno

    def print_tree(self, level=0):
        indent = "    " * level
        val_str = f" ({self.value})" if self.value is not None else ""
        line_str = f" [Línea {self.lineno}]" if self.lineno is not None else ""
        print(f"{indent}└── {self.type}{val_str}{line_str}")
        for child in self.children:
            if isinstance(child, ASTNode):
                child.print_tree(level + 1)
            elif isinstance(child, list):
                for sub_child in child:
                    if isinstance(sub_child, ASTNode):
                        sub_child.print_tree(level + 1)

# Lista global de errores sintácticos
parser_errors = []

# Precedencia de operaciones actualizada (de menor a mayor precedencia)
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUALS', 'NE', 'GREATER', 'LESS', 'GE', 'LE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'NOT'),  # Operador unario prefijo
)

# --- REGLAS DE GRAMÁTICA DE JAVA ---

def p_program(p):
    '''program : modifier CLASS ID LBRACE main_method RBRACE'''
    p[0] = ASTNode("CLASE", [p[5]], value=f"{p[1]} {p[3]}", lineno=p.lineno(2))

def p_modifier(p):
    '''modifier : PUBLIC
                | PRIVATE
                | PROTECTED'''
    p[0] = p[1]

def p_main_method(p):
    '''main_method : PUBLIC STATIC VOID MAIN LPAREN STRING_TYPE LBRACK RBRACK ID RPAREN block'''
    p[0] = ASTNode("METODO_MAIN", [p[11]], value=p[9], lineno=p.lineno(4))

def p_block(p):
    '''block : LBRACE statements RBRACE'''
    p[0] = ASTNode("BLOQUE", p[2])

def p_statements(p):
    '''statements : statement statements
                  | empty'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_statement(p):
    '''statement : declaration
                 | assignment
                 | if_statement
                 | while_statement
                 | for_statement'''
    p[0] = p[1]

def p_declaration(p):
    '''declaration : type ID ASSIGN expression SEMI
                   | type ID SEMI'''
    if len(p) == 6:
        p[0] = ASTNode("DECLARACION_ASIGNACION", [p[4]], value={'type': p[1], 'id': p[2]}, lineno=p.lineno(2))
    else:
        p[0] = ASTNode("DECLARACION", value={'type': p[1], 'id': p[2]}, lineno=p.lineno(2))

def p_type(p):
    '''type : INT_TYPE
            | DOUBLE_TYPE
            | BOOLEAN_TYPE
            | STRING_TYPE'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : ID ASSIGN expression SEMI'''
    p[0] = ASTNode("ASIGNACION", [p[3]], value=p[1], lineno=p.lineno(1))

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN block
                    | IF LPAREN expression RPAREN block ELSE block'''
    if len(p) == 6:
        p[0] = ASTNode("IF", [p[3], p[5]], lineno=p.lineno(1))
    else:
        p[0] = ASTNode("IF_ELSE", [p[3], p[5], p[7]], lineno=p.lineno(1))

def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN block'''
    p[0] = ASTNode("WHILE", [p[3], p[5]], lineno=p.lineno(1))

def p_for_statement(p):
    '''for_statement : FOR LPAREN for_init SEMI expression SEMI for_update RPAREN block'''
    p[0] = ASTNode("FOR", [p[3], p[5], p[7], p[9]], lineno=p.lineno(1))

def p_for_init(p):
    '''for_init : type ID ASSIGN expression
                | ID ASSIGN expression
                | empty'''
    if len(p) == 5:
        p[0] = ASTNode("FOR_INIT_DECL", [p[4]], value={'type': p[1], 'id': p[2]}, lineno=p.lineno(2))
    elif len(p) == 4:
        p[0] = ASTNode("FOR_INIT_ASSIGN", [p[3]], value=p[1], lineno=p.lineno(1))
    else:
        p[0] = ASTNode("VACIO")

def p_for_update(p):
    '''for_update : ID ASSIGN expression
                  | empty'''
    if len(p) == 4:
        p[0] = ASTNode("FOR_UPDATE", [p[3]], value=p[1], lineno=p.lineno(1))
    else:
        p[0] = ASTNode("VACIO")

# --- MANEJO DE EXPRESIONES (Binarias, Unarias y Literales) ---

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EQUALS expression
                  | expression NE expression
                  | expression GREATER expression
                  | expression LESS expression
                  | expression GE expression
                  | expression LE expression
                  | expression AND expression
                  | expression OR expression'''
    p[0] = ASTNode("OPERACION_BINARIA", [p[1], p[3]], value=p[2], lineno=p.lineno(2))

def p_expression_unop(p):
    '''expression : NOT expression'''
    p[0] = ASTNode("OPERACION_UNARIA", [p[2]], value=p[1], lineno=p.lineno(1))

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_literal(p):
    '''expression : INT_LITERAL
                  | DOUBLE_LITERAL
                  | STRING_LITERAL'''
    t_type = "int" if isinstance(p[1], int) else "double" if isinstance(p[1], float) else "String"
    p[0] = ASTNode("LITERAL", value={'type': t_type, 'val': p[1]}, lineno=p.lineno(1))

def p_expression_boolean(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = ASTNode("LITERAL", value={'type': 'boolean', 'val': p[1]}, lineno=p.lineno(1))

def p_expression_id(p):
    '''expression : ID'''
    p[0] = ASTNode("VARIABLE", value=p[1], lineno=p.lineno(1))

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    if p:
        error_msg = f"Línea {p.lineno}: Token inesperado '{p.value}' de tipo {p.type}"
    else:
        error_msg = "Fin de archivo inesperado (posible falta de una llave '}' o punto y coma ';')"
    parser_errors.append(error_msg)

# Constructor del Parser
parser = yacc.yacc()