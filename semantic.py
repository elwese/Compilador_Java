from parser import ASTNode

class AnalizadorSemantico:
    # Codigo Cesar Delgado

    def __init__(self):
        # Almacena las variables del contexto: {nombre_variable: tipo}
        self.tabla_simbolos = {}
        self.errores = []

    def analizar(self, node):
        if node is None:
            return None
        
        # Procesamiento estructurado según el tipo de nodo del AST
        if node.type in ["CLASE", "METODO_MAIN", "BLOQUE"]:
            for child in node.children:
                if isinstance(child, list):
                    for sub_child in child:
                        self.analizar(sub_child)
                else:
                    self.analizar(child)

        elif node.type == "DECLARACION":
            var_type = node.value['type']
            var_name = node.value['id']
            if var_name in self.tabla_simbolos:
                self.errores.append(f"Línea {node.lineno}: La variable '{var_name}' ya ha sido declarada anteriormente.")
            else:
                self.tabla_simbolos[var_name] = var_type

        elif node.type == "DECLARACION_ASIGNACION":
            var_type = node.value['type']
            var_name = node.value['id']
            if var_name in self.tabla_simbolos:
                self.errores.append(f"Línea {node.lineno}: La variable '{var_name}' ya ha sido declarada.")
            else:
                self.tabla_simbolos[var_name] = var_type
                expr_type = self.obtener_tipo_expresion(node.children[0])
                if expr_type and expr_type != var_type:
                    self.errores.append(f"Línea {node.lineno}: Tipos incompatibles. No se puede asignar '{expr_type}' a una variable '{var_type}'.")

        elif node.type == "ASIGNACION":
            var_name = node.value
            if var_name not in self.tabla_simbolos:
                self.errores.append(f"Línea {node.lineno}: La variable '{var_name}' no ha sido declarada.")
            else:
                var_type = self.tabla_simbolos[var_name]
                expr_type = self.obtener_tipo_expresion(node.children[0])
                if expr_type and expr_type != var_type:
                    self.errores.append(f"Línea {node.lineno}: Tipos incompatibles en asignación de '{var_name}'. Se esperaba '{var_type}', se obtuvo '{expr_type}'.")

        elif node.type in ["IF", "IF_ELSE", "WHILE"]:
            cond_type = self.obtener_tipo_expresion(node.children[0])
            if cond_type and cond_type != "boolean":
                self.errores.append(f"Línea {node.lineno}: La condición de la estructura '{node.type}' debe resolver a un tipo 'boolean' (se detectó '{cond_type}').")
            
            for child in node.children[1:]:
                self.analizar(child)

        elif node.type == "FOR":
            self.analizar(node.children[0])  # Inicialización del for
            cond_type = self.obtener_tipo_expresion(node.children[1])  # Condición del for
            if cond_type and cond_type != "boolean":
                self.errores.append(f"Línea {node.lineno}: La condición del ciclo 'FOR' debe ser de tipo 'boolean' (se detectó '{cond_type}').")
            self.analizar(node.children[2])  # Incremento / Update
            self.analizar(node.children[3])  # Cuerpo

        elif node.type in ["FOR_INIT_DECL", "FOR_INIT_ASSIGN", "FOR_UPDATE"]:
            if node.type == "FOR_INIT_DECL":
                var_type = node.value['type']
                var_name = node.value['id']
                if var_name in self.tabla_simbolos:
                    self.errores.append(f"Línea {node.lineno}: Variable de control '{var_name}' ya declarada.")
                else:
                    self.tabla_simbolos[var_name] = var_type
                    expr_type = self.obtener_tipo_expresion(node.children[0])
                    if expr_type and expr_type != var_type:
                        self.errores.append(f"Línea {node.lineno}: Tipo incompatible en inicialización de FOR para '{var_name}'.")
            else:
                var_name = node.value
                if var_name not in self.tabla_simbolos:
                    self.errores.append(f"Línea {node.lineno}: Variable '{var_name}' en el ciclo FOR no declarada.")
                else:
                    var_type = self.tabla_simbolos[var_name]
                    expr_type = self.obtener_tipo_expresion(node.children[0])
                    if expr_type and expr_type != var_type:
                        self.errores.append(f"Línea {node.lineno}: Incompatibilidad de tipos en actualización de FOR.")

    # Codigo Jonathan Pacalla
    # Codigo Jose Salazar
    def obtener_tipo_expresion(self, node):
        if node is None:
            return None
        
        if node.type == "LITERAL":
            return node.value['type']
        
        elif node.type == "VARIABLE":
            var_name = node.value
            if var_name not in self.tabla_simbolos:
                self.errores.append(f"Línea {node.lineno}: Uso de variable no declarada '{var_name}' dentro de una expresión.")
                return None
            return self.tabla_simbolos[var_name]
        
        elif node.type == "OPERACION_UNARIA":
            if node.value == "!":
                expr_type = self.obtener_tipo_expresion(node.children[0])
                if expr_type and expr_type != "boolean":
                    self.errores.append(f"Línea {node.lineno}: El operador lógico '!' solo se puede aplicar a expresiones lógicas (se obtuvo '{expr_type}').")
                    return None
                return "boolean"

        elif node.type == "OPERACION_BINARIA":
            izq = self.obtener_tipo_expresion(node.children[0])
            der = self.obtener_tipo_expresion(node.children[1])
            op = node.value

            if not izq or not der:
                return None

            # Operadores lógicos compuestos (&&, ||)
            if op in ["&&", "||"]:
                if izq != "boolean" or der != "boolean":
                    self.errores.append(f"Línea {node.lineno}: El operador lógico '{op}' requiere operandos estrictamente booleanos (se obtuvo '{izq}' y '{der}').")
                    return None
                return "boolean"

            # Operadores de igualdad relacional (==, !=)
            if op in ["==", "!="]:
                if izq != der:
                    self.errores.append(f"Línea {node.lineno}: Tipos incompatibles para comparación de igualdad: '{izq}' no coincide con '{der}'.")
                    return None
                return "boolean"
            
            # Operadores de comparación matemática (>, <, >=, <=)
            if op in [">", "<", ">=", "<="]:
                if izq not in ["int", "double"] or der not in ["int", "double"]:
                    self.errores.append(f"Línea {node.lineno}: El operador '{op}' solo puede usarse entre valores numéricos (int o double).")
                    return None
                if izq != der:
                    self.errores.append(f"Línea {node.lineno}: Comparación inconsistente de tipos numéricos: '{izq}' contra '{der}'.")
                    return None
                return "boolean"
            
            # Operadores aritméticos estándar (+, -, *, /)
            if op in ["+", "-", "*", "/"]:
                if izq == "String" or der == "String":
                    if op == "+":
                        return "String"  # Concatenación
                    else:
                        self.errores.append(f"Línea {node.lineno}: Operador aritmético '{op}' no válido para cadenas de texto.")
                        return None
                
                if izq == "boolean" or der == "boolean":
                    self.errores.append(f"Línea {node.lineno}: No se permiten operaciones matemáticas con tipos lógicos 'boolean'.")
                    return None

                if izq == "double" or der == "double":
                    return "double"
                
                return "int"
        return None