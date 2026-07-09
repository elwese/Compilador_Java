#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
COMPILADOR JAVA - ORQUESTADOR
Integra: Lexer (javalex.py) -> Parser (parser.py) -> Semántico (semantic.py)
Imprime todo el proceso en consola
"""

import sys
import os
from pathlib import Path
from javalex import lexer
from parser import parser
from semantic import SemanticAnalyzer

def print_section(title):
    """Imprime un encabezado de sección"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def print_step(step):
    """Imprime un paso del proceso"""
    print(f"\n[PASO] {step}")
    print("-" * 60)

def analyze_code(codigo, filename="entrada"):
    """
    Analiza código Java a través de los 3 componentes
    
    Args:
        codigo: String con código Java
        filename: Nombre del archivo (para referencia)
    """
    
    print_section("COMPILADOR JAVA - ANÁLISIS COMPLETO")
    print(f"Analizando: {filename}")
    print(f"Líneas de código: {len(codigo.split(chr(10)))}")
    
    # ==================== PASO 1: LEXER ====================
    print_step("1. ANÁLISIS LÉXICO (Lexer)")
    print("Código a tokenizar:")
    print(codigo)
    
    try:
        lexer.input(codigo)
        tokens_list = []
        
        print("\nTokens generados:")
        print(f"{'Tipo':<20} {'Valor':<30} {'Línea':<5}")
        print("-" * 55)
        
        for tok in lexer:
            tokens_list.append(tok)
            valor_str = str(tok.value)[:28] if tok.value else "N/A"
            print(f"{tok.type:<20} {valor_str:<30} {tok.lineno:<5}")
        
        print(f"\n✓ Total de tokens: {len(tokens_list)}")
        
    except Exception as e:
        print(f"✗ ERROR EN LEXER: {e}")
        return False
    
    # ==================== PASO 2: PARSER ====================
    print_step("2. ANÁLISIS SINTÁCTICO (Parser)")
    print("Generando Árbol de Sintaxis Abstracta (AST)...")
    
    try:
        ast = parser.parse(codigo)
        
        if ast is None:
            print("✗ ERROR: Parser retornó None")
            return False
        
        print("\n✓ AST generado exitosamente:")
        print(f"\n{ast}")
        
    except Exception as e:
        print(f"✗ ERROR EN PARSER: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # ==================== PASO 3: ANÁLISIS SEMÁNTICO ====================
    print_step("3. ANÁLISIS SEMÁNTICO (Semantic Analyzer)")
    print("Validando tipos y estructura...")
    
    try:
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        print("\n✓ Análisis completado")
        
        # Mostrar tabla de símbolos
        print("\nTabla de Símbolos:")
        print("-" * 60)
        if analyzer.symbol_table and analyzer.symbol_table[0]:
            print(f"{'Variable':<20} {'Tipo':<15} {'Valor':<25}")
            print("-" * 60)
            for scope_idx, scope in enumerate(analyzer.symbol_table):
                for var_name, var_obj in scope.items():
                    print(f"{var_name:<20} {var_obj.type:<15} {str(var_obj.value):<25}")
        else:
            print("(Vacía)")
        
        # Mostrar errores semánticos
        if analyzer.errors:
            print("\n✗ ERRORES SEMÁNTICOS ENCONTRADOS:")
            print("-" * 60)
            for idx, error in enumerate(analyzer.errors, 1):
                print(f"  {idx}. {error}")
            return False
        else:
            print("\n✓ No se encontraron errores semánticos")
        
        return True
        
    except Exception as e:
        print(f"✗ ERROR EN ANÁLISIS SEMÁNTICO: {e}")
        import traceback
        traceback.print_exc()
        return False

def find_java_files(directory="."):
    """Busca todos los archivos .java en el directorio"""
    java_files = []
    try:
        for file in Path(directory).glob("*.java"):
            java_files.append(file.name)
    except Exception as e:
        print(f"Error al buscar archivos: {e}")
    return sorted(java_files)

def show_menu():
    """Muestra un menú interactivo para seleccionar la entrada"""
    print_section("COMPILADOR JAVA - SELECTOR DE ENTRADA")
    
    # Buscar archivos .java disponibles
    java_files = find_java_files()
    
    print("Opciones disponibles:\n")
    print("  0) Usar código de prueba (por defecto)")
    
    if java_files:
        print(f"  1) Seleccionar de archivos .java disponibles ({len(java_files)} archivos)")
        for idx, file in enumerate(java_files, start=1):
            print(f"     {idx}) {file}")
    
    print("  2) Escribir ruta personalizada")
    print("  3) Salir")
    print()
    
    choice = input("Selecciona una opción (0-3): ").strip()
    
    if choice == "0":
        return "prueba"
    elif choice == "1" and java_files:
        try:
            file_idx = int(input("\nNúmero del archivo: ").strip())
            if 1 <= file_idx <= len(java_files):
                return java_files[file_idx - 1]
            else:
                print("Índice inválido. Usando código de prueba.")
                return "prueba"
        except ValueError:
            print("Entrada inválida. Usando código de prueba.")
            return "prueba"
    elif choice == "2":
        path = input("\nRuta del archivo: ").strip()
        if os.path.exists(path):
            return path
        else:
            print(f"Archivo no encontrado: {path}")
            print("Usando código de prueba.")
            return "prueba"
    elif choice == "3":
        print("Saliendo...")
        sys.exit(0)
    else:
        print("Opción inválida. Usando código de prueba.")
        return "prueba"

def load_code(entrada):
    """Carga el código desde archivo o usa código de prueba"""
    if entrada == "prueba":
        # Código de prueba por defecto
        codigo = """
    int edad = 25;
    float nota = 8.5;
    if (edad >= 18) {
        edad = edad + 1;
    }
    """
        return codigo, "PRUEBA (por defecto)"
    else:
        # Cargar desde archivo
        try:
            with open(entrada, "r", encoding="utf-8") as f:
                codigo = f.read()
            return codigo, entrada
        except Exception as e:
            print(f"Error al leer archivo: {e}")
            print("Usando código de prueba.")
            codigo = """
    int edad = 25;
    float nota = 8.5;
    if (edad >= 18) {
        edad = edad + 1;
    }
    """
            return codigo, "PRUEBA (fallback)"

def main():
    """Función principal"""
    
    # Mostrar menú y obtener entrada del usuario
    entrada = show_menu()
    
    # Cargar código
    codigo, filename = load_code(entrada)
    
    # Ejecutar análisis
    resultado = analyze_code(codigo, filename)
    
    # Resumen final
    print_section("RESUMEN FINAL")
    if resultado:
        print("✓ COMPILACIÓN EXITOSA")
        print("  - Lexer: OK")
        print("  - Parser: OK")
        print("  - Semántico: OK")
    else:
        print("✗ COMPILACIÓN FALLIDA")
        print("  Revisa los errores arriba")
    
    return 0 if resultado else 1

if __name__ == "__main__":
    sys.exit(main())
