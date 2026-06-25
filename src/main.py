# main.py
# Punto de entrada del analizador léxico-sintáctico de partidas de Truco.
# Uso:
#   python main.py                       → modo interactivo (multilínea)
#   python main.py "truco quiero ; ..."   → analiza la cadena pasada como argumento
#   python main.py --file casos.txt       → analiza cada línea del archivo

import sys
from lexer import Scanner
from parser import Parser, print_ast


def analizar(codigo: str) -> None:
    """Ejecuta el lexer y el parser sobre una cadena y muestra los resultados."""
    print(f"\n{'='*60}")
    print(f"ENTRADA: {codigo!r}")

    # Fase léxica
    scanner = Scanner(codigo)
    tokens = scanner.tokenize()

    # Mostrar tokens generados (solo los que no son EOF)
    print("TOKENS:")
    for token in tokens[:-1]:  # excluye EOF
        if token.type == 'ERROR':
            print(f"  ⚠️  Error léxico: lexema '{token.lexeme}' (línea {token.line})")
        else:
            print(f"  {token}")

    # Verificar si hubo errores léxicos
    tokens_con_error = [t for t in tokens if t.type == 'ERROR']
    if tokens_con_error:
        print(f"\n⚠️  Se encontraron {len(tokens_con_error)} error(es) léxico(s).")
        print("El análisis sintáctico continuará, pero los tokens inválidos serán ignorados.\n")

    # Fase sintáctica
    parser = Parser(tokens)
    ast, errores = parser.parse()

    if ast:
        print("\nAST:")
        print_ast(ast)

    if errores:
        print("\nERRORES:")
        for error in errores:
            print(f"  ⚠️  {error}")
    else:
        print("\n✅ Análisis sintáctico exitoso.")


def main() -> None:
    if len(sys.argv) > 1:
        if sys.argv[1] == '--file':
            # Leer desde archivo
            try:
                with open(sys.argv[2], 'r', encoding='utf-8') as f:
                    contenido = f.read()
                # El archivo ya contiene saltos de línea, lo analizamos directamente
                analizar(contenido)
            except FileNotFoundError:
                print(f"Error: No se encontró el archivo '{sys.argv[2]}'")
                sys.exit(1)
        else:
            # Argumento directo
            analizar(sys.argv[1])
    else:
        # Modo interactivo mejorado
        print("=" * 60)
        print("Analizador de partidas de Truco")
        print("=" * 60)
        print("Escribe una partida y presiona Enter.")
        print("Puedes escribir varias líneas (Enter vacío para terminar).")
        print("Comandos especiales: ':q' para salir, ':h' para ayuda.")
        print("-" * 60)

        try:
            while True:
                lineas = []
                print("\n> ", end='')
                sys.stdout.flush()
                while True:
                    linea = input()
                    if linea.strip() == '':
                        break
                    if linea.strip() == ':q':
                        print("Saliendo...")
                        return
                    if linea.strip() == ':h':
                        print("\nAyuda:")
                        print("  Escribe una partida de Truco y presiona Enter.")
                        print("  Puedes escribir varias líneas (Enter vacío para terminar).")
                        print("  ':q' para salir, ':h' para esta ayuda.")
                        print("\n> ", end='')
                        sys.stdout.flush()
                        continue
                    lineas.append(linea.strip())

                if not lineas:
                    continue

                # Unir las líneas con '\n' preserva los saltos de línea para el lexer
                codigo = '\n'.join(lineas)
                analizar(codigo)

        except KeyboardInterrupt:
            print("\n\nSaliendo...")


if __name__ == '__main__':
    main()