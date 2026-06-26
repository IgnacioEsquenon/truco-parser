# micro-truco/main.py
# Punto de entrada para probar el analizador Micro‑Truco.
# Uso:
#   python main.py "truco quiero"
# Si no se pasa argumento, ejecuta casos predefinidos.

import sys
from lexer import Scanner
from parser import Parser, print_ast


def analizar(codigo: str) -> None:
    """Ejecuta el lexer y el parser sobre una cadena y muestra resultados."""
    print(f"\n{'='*50}")
    print(f"Entrada: {codigo!r}")
    
    # --- Fase léxica ---
    scanner = Scanner(codigo)
    tokens = scanner.scan_tokens()

    # Mostrar tokens generados (solo los que no son EOF ni ERROR)
    print("Tokens:")
    for token in tokens[:-1]:  # excluye EOF
        if token.type == 'ERROR':
            print(f"  ⚠️  Error léxico: lexema '{token.lexeme}' (línea {token.line})")
        else:
            print(f"  {token}")

    # Verificar si hubo errores léxicos
    tokens_error = [t for t in tokens if t.type == 'ERROR']
    if tokens_error:
        print(f"\n❌ Se encontraron {len(tokens_error)} error(es) léxico(s). No se puede continuar con el análisis sintáctico.")
        return

    # --- Fase sintáctica ---
    parser = Parser(tokens)
    ast, errores = parser.parse()

    if ast:
        print("\nAST:")
        print_ast(ast)
    
    if errores:
        print("\nErrores sintácticos:")
        for error in errores:
            print(f"  ⚠️  {error}")
    
    if not errores:
        print("\n✅ Análisis sintáctico exitoso.")


def main() -> None:
    if len(sys.argv) > 1:
        # Modo línea de comandos: acepta la cadena como argumento
        analizar(sys.argv[1])
    else:
        # Modo automático: prueba con varios casos predefinidos
        pruebas = [
            "truco quiero",
            "truco no_quiero",
            "truco truco",
            "truco",                    # falta respuesta
            "truco quiero no_quiero",   # secuencia más larga
            "truco x",                  # error léxico
            "traco quiero",             # error léxico
            "quiero",                   # falta truco
        ]
        for codigo in pruebas:
            analizar(codigo)


if __name__ == '__main__':
    main()