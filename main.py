import sys
import os
from javalex import lexer, lex_errors
from parser import parser, parser_errors
from semantic import AnalizadorSemantico

def ejecutar_compilador(ruta_archivo):
    # Verificamos que el archivo realmente exista en la ruta indicada
    if not os.path.exists(ruta_archivo):
        print(f"❌ Error: El archivo '{ruta_archivo}' no se encuentra en este directorio.")
        return

    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        codigo_fuente = f.read()

    print("=" * 60)
    print(f" PROCESANDO EL ARCHIVO: {ruta_archivo} ")
    print("=" * 60)

    # -----------------------------------------------------------------
    # FASE 1: ANÁLISIS LÉXICO
    # -----------------------------------------------------------------
    print("\n--- [1] COMPONENTE LÉXICO ---")
    lexer.input(codigo_fuente)
    lexer.lineno = 1  # Reset de contador por archivo
    
    print("Tokens detectados en el archivo:")
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"  [Línea {tok.lineno}] Token: {tok.type:16} -> Valor: '{tok.value}'")

    if lex_errors:
        print("\n❌ ERRORES LÉXICOS DETECTADOS:")
        for err in lex_errors:
            print(f"  • {err}")
        lex_errors.clear()
        return
    else:
        print("  Análisis léxico impecable. Cero errores.")

    # -----------------------------------------------------------------
    # FASE 2: ANÁLISIS SINTÁCTICO
    # -----------------------------------------------------------------
    print("\n--- [2] COMPONENTE SINTÁCTICO ---")
    parser_errors.clear()
    
    ast_raiz = parser.parse(codigo_fuente, lexer=lexer)

    if parser_errors:
        print("\n❌ ERRORES SINTÁCTICOS DETECTADOS:")
        for err in parser_errors:
            print(f"  • {err}")
        parser_errors.clear()
        return
    else:
        print(" Estructura sintáctica válida. Representación visual del AST:")
        if ast_raiz:
            ast_raiz.print_tree()

    # -----------------------------------------------------------------
    # FASE 3: ANÁLISIS SEMÁNTICO
    # -----------------------------------------------------------------
    print("\n--- [3] COMPONENTE SEMÁNTICO ---")
    analizador = AnalizadorSemantico()
    analizador.analizar(ast_raiz)

    if analizador.errores:
        print("\n❌ ERRORES SEMÁNTICOS DETECTADOS:")
        for err in analizador.errores:
            print(f"  • {err}")
    else:
        print(" ¡Compilación Semántica Exitosa! Toda la lógica de tipos y variables está en orden.")
        print("\n Tabla de Símbolos final registrada:")
        for var, tipo in analizador.tabla_simbolos.items():
            print(f"  • Variable: '{var}' de tipo -> {tipo}")
            
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    # 1. Validamos que se haya pasado exactamente un argumento (el archivo .java)
    if len(sys.argv) != 2:
        print("❌ Error: Argumentos inválidos.")
        print("👉 Uso correcto: python main.py <nombre_archivo.java>")
        sys.exit(1)

    archivo_entrada = sys.argv[1]

    # 2. Validamos que tenga la extensión .java
    if not archivo_entrada.endswith(".java"):
        print("❌ Error: El archivo especificado debe ser de extensión '.java'")
        sys.exit(1)

    # 3. Al estar en la misma carpeta, lo procesamos directamente
    ejecutar_compilador(archivo_entrada)