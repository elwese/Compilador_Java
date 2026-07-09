from parser import parser
from javalex import lexer

# Codigo Cesar Delgado

# ==========================================================
# 1. CLASE PARA LOS SÍMBOLOS 
# ==========================================================

class Symbol:

    """
    Representa una variable almacenada en la tabla
    de símbolos.
    """

    def __init__(self, name, data_type, value=None):

        self.name = name
        self.type = data_type
        self.value = value

    def __repr__(self):

        return f"{self.name} : {self.type} = {self.value}"


# ==========================================================
# 2. CLASE DEL ANALIZADOR SEMÁNTICO
# ==========================================================

class SemanticAnalyzer:

    def __init__(self):

        # -----------------------------
        # Tabla de símbolos
        # Cada elemento representa un scope.
        # -----------------------------

        self.symbol_table = [{}]

        # -----------------------------
        # Lista de errores encontrados
        # -----------------------------

        self.errors = []


# ==========================================================
# 3. MANEJO DE SCOPES
# ==========================================================

    def enter_scope(self):

        """
        Crea un nuevo ámbito.
        """

        self.symbol_table.append({})



    def exit_scope(self):

        """
        Sale del ámbito actual.
        """

        if len(self.symbol_table) > 1:

            self.symbol_table.pop()


# ==========================================================
# 4. MANEJO DE ERRORES
# ==========================================================

    def semantic_error(self, message):

        self.errors.append(message)



    def print_errors(self):

        print("\n========== ERRORES SEMÁNTICOS ==========\n")

        if len(self.errors) == 0:

            print("No se encontraron errores.")

        else:

            for error in self.errors:

                print("•", error)


# ==========================================================
# 5. TABLA DE SÍMBOLOS
# ==========================================================

    def declare_variable(self, name, data_type, value=None):

        """
        Declara una variable dentro del scope actual.
        """

        current_scope = self.symbol_table[-1]

        if name in current_scope:

            self.semantic_error(

                f"La variable '{name}' ya fue declarada."

            )

            return

        current_scope[name] = Symbol(

            name,
            data_type,
            value

        )



    def lookup_variable(self, name):

        """
        Busca una variable desde el scope más interno
        hasta el global.
        """

        for scope in reversed(self.symbol_table):

            if name in scope:

                return scope[name]

        return None


# ==========================================================
# 6. MÉTODO PRINCIPAL
# ==========================================================

    def analyze(self, ast):

        """
        Inicia el recorrido del AST.
        """

        self.visit(ast)


# ==========================================================
# 7. RECORRIDO DEL AST
# ==========================================================

    def visit(self, node):

        if node is None:

            return

        # -----------------------------
        # Lista de sentencias
        # -----------------------------

        if isinstance(node, list):

            for statement in node:

                self.visit(statement)

            return

        # -----------------------------
        # Nodo simple
        # -----------------------------

        if not isinstance(node, tuple):

            return

        node_type = node[0]

        if node_type == "var_decl":

            self.visit_var_decl(node)

        elif node_type == "assign":

            self.visit_assignment(node)

        elif node_type == "binop":

            self.visit_binop(node)

        elif node_type == "unary":

            self.visit_unary(node)

        elif node_type == "if":

            self.visit_if(node)

        elif node_type == "if_else":

            self.visit_if_else(node)

        elif node_type == "while":

            self.visit_while(node)

        elif node_type == "for":

            self.visit_for(node)

        elif node_type == "method":

            self.visit_method(node)

        elif node_type == "print":

            self.visit_print(node)


#Codigo Jonathan Pacalla

# ==========================================================
# 8. MÉTODOS IMPLEMENTADOS
# =========================================================

    def infer_type(self, value):
        """Determina el tipo de una expresión."""
        if isinstance(value, int):
            return "int"
        if isinstance(value, float):
            return "float"
        if isinstance(value, str):
            if value == "true" or value == "false":
                return "boolean"
            if value.startswith('"'):
                return "String"
            if value.startswith("'") and value.endswith("'"):
                return "char"
            symbol = self.lookup_variable(value)
            if symbol is not None:
                return symbol.type
            self.semantic_error(f"La variable '{value}' no ha sido declarada.")
            return "error"
        if isinstance(value, tuple):
            if value[0] == "binop":
                return self.visit_binop(value)
            if value[0] == "unary":
                return self.visit_unary(value)
        return "error"

    def compatible_types(self, left, right):
        """Comprueba si dos tipos son compatibles."""
        if left == right:
            return True
        numeric = ["byte", "short", "int", "long", "float", "double"]
        if left in numeric and right in numeric:
            return True
        return False

    def visit_var_decl(self, node):
        _, data_type, variable_name, value = node
        if self.lookup_variable(variable_name):
            self.semantic_error(f"La variable '{variable_name}' ya existe.")
            return
        if value is None:
            self.declare_variable(variable_name, data_type)
            return
        value_type = self.infer_type(value)
        if not self.compatible_types(data_type, value_type):
            self.semantic_error(f"No se puede asignar un valor '{value_type}' a una variable de tipo '{data_type}'.")
            return
        self.declare_variable(variable_name, data_type, value)

    def visit_assignment(self, node):
        _, operator, variable_name, value = node
        variable = self.lookup_variable(variable_name)
        if variable is None:
            self.semantic_error(f"La variable '{variable_name}' no existe.")
            return
        value_type = self.infer_type(value)
        if not self.compatible_types(variable.type, value_type):
            self.semantic_error(f"No se puede asignar '{value_type}' a '{variable.type}'.")
            return
        variable.value = value

    def visit_binop(self, node):
        _, operator, left, right = node
        left_type = self.infer_type(left)
        right_type = self.infer_type(right)
        if operator in ['+', '-', '*', '/', '%']:
            if not self.compatible_types(left_type, right_type):
                self.semantic_error(f"Operación inválida entre '{left_type}' y '{right_type}'.")
                return "error"
            if "double" in [left_type, right_type]:
                return "double"
            if "float" in [left_type, right_type]:
                return "float"
            return "int"
        if operator in ['==', '!=', '<', '>', '<=', '>=']:
            if not self.compatible_types(left_type, right_type):
                self.semantic_error(f"No se puede comparar '{left_type}' con '{right_type}'.")
            return "boolean"
        if operator in ['&&', '||']:
            if left_type != "boolean":
                self.semantic_error("El operando izquierdo debe ser boolean.")
            if right_type != "boolean":
                self.semantic_error("El operando derecho debe ser boolean.")
            return "boolean"
        return "error"

    def visit_unary(self, node):
        _, operator, value = node
        value_type = self.infer_type(value)
        if operator == "!":
            if value_type != "boolean":
                self.semantic_error("El operador ! solo acepta boolean.")
            return "boolean"
        if operator == "-":
            if value_type not in ["byte", "short", "int", "long", "float", "double"]:
                self.semantic_error("El operador - requiere un número.")
            return value_type
        return "error"

    def visit_if(self, node):
        _, condition, body = node
        condition_type = self.infer_type(condition)
        if condition_type != "boolean":
            self.semantic_error("La condición del IF debe ser de tipo boolean.")
        self.enter_scope()
        self.visit(body)
        self.exit_scope()

    def visit_if_else(self, node):
        _, condition, if_body, else_body = node
        condition_type = self.infer_type(condition)
        if condition_type != "boolean":
            self.semantic_error("La condición del IF debe ser de tipo boolean.")
        self.enter_scope()
        self.visit(if_body)
        self.exit_scope()
        self.enter_scope()
        self.visit(else_body)
        self.exit_scope()

    def visit_while(self, node):
        _, condition, body = node
        condition_type = self.infer_type(condition)
        if condition_type != "boolean":
            self.semantic_error("La condición del WHILE debe ser boolean.")
        self.enter_scope()
        self.visit(body)
        self.exit_scope()

    def visit_for(self, node):
        _, initialization, condition, update, body = node
        self.enter_scope()
        self.visit(initialization)
        condition_type = self.infer_type(condition)
        if condition_type != "boolean":
            self.semantic_error("La condición del FOR debe ser boolean.")
        self.visit(update)
        self.visit(body)
        self.exit_scope()

    def visit_method(self, node):
        _, modifier, return_type, name, parameters, body = node
        print(f"\n[SEMÁNTICO] Analizando método: {name}")
        self.enter_scope()
        self.visit(body)
        self.exit_scope()

    def visit_print(self, node):
        _, expression = node
        expression_type = self.infer_type(expression)
        if expression_type == "error":
            self.semantic_error("La expresión enviada a println es inválida.")


    def report(self):

        self.print_errors()

        print("\n========== TABLA DE SÍMBOLOS ==========\n")

        for i, scope in enumerate(self.symbol_table):

            print(f"Scope {i}")

            for variable in scope.values():

                print(variable)

            print()





#Prueba
if __name__ == "__main__":

    from parser import parser

    with open("pruebaCesarDelgado.java", "r", encoding="utf-8") as archivo:
        codigo = archivo.read()

    ast = parser.parse(codigo)

    print("===== AST =====")
    print(ast)

    print()

    analizador = SemanticAnalyzer()
    analizador.visit(ast)

    print()

    if analizador.errors:
        print("===== ERRORES SEMÁNTICOS =====")
        for error in analizador.errors:
            print(error)
    else:
        print("No se encontraron errores semánticos.")