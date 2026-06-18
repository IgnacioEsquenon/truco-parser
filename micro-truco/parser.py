# micro_parser.py
# Parser descendente recursivo para el lenguaje "Micro-Truco"
# Gramática:
#   <jugada>    ::= <canto> <respuesta>
#   <canto>     ::= "truco"
#   <respuesta> ::= "quiero" | "no_quiero"
#
# Basado en el Capítulo 6 de Crafting Interpreters (Nystrom, 2021).
# El parser traduce cada no terminal de la gramática en un método.
# Construye un AST como tuplas anidadas.

from typing import List, Any, Optional

# ---------------------------------------------------------------------------
# Clase Parser
# ---------------------------------------------------------------------------

class Parser:
    """Analizador sintáctico descendente recursivo para el Micro-Truco."""

    def __init__(self, tokens: List[Any]) -> None:
        """Inicializa el parser con la lista de tokens del lexer.

        Args:
            tokens: Lista de tokens generada por el lexer.
                    Cada token es un objeto con atributos type, lexeme, line.
        """
        self.tokens = tokens
        self.current = 0          # índice del token actual
        self.errors: List[str] = []  # lista de mensajes de error

    # ------------------------------------------------------------------
    # Métodos auxiliares (ya implementados, tal cual el libro)
    # ------------------------------------------------------------------

    def peek(self) -> str:
        """Devuelve el tipo del token actual sin consumirlo."""
        return self.tokens[self.current].type

    def is_at_end(self) -> bool:
        """Verifica si llegamos al token EOF."""
        return self.peek() == 'EOF'

    def advance(self) -> Any:
        """Consume el token actual y avanza al siguiente."""
        tok = self.tokens[self.current]
        self.current += 1
        return tok

    def check(self, type_: str) -> bool:
        """Devuelve True si el token actual es del tipo dado, sin consumirlo."""
        if self.is_at_end():
            return False
        return self.peek() == type_

    def match(self, *types: str) -> Optional[Any]:
        """Si el token actual coincide con alguno de los tipos dados, lo consume y lo devuelve.
        Si no coincide, devuelve None y no consume nada.
        """
        for type_ in types:
            if self.check(type_):
                return self.advance()
        return None

    def error(self, message: str) -> None:
        """Registra un error sintáctico con la línea del token actual."""
        line = self.tokens[self.current].line
        self.errors.append(f"[línea {line}] Error: {message}")
        # En el Micro-Truco no hay sincronizador complejo; simplemente avanzamos
        # para evitar bucles infinitos (modo pánico simplificado).
        if not self.is_at_end():
            self.advance()

    # ------------------------------------------------------------------
    # Métodos por cada no terminal de la gramática (a completar)
    # ------------------------------------------------------------------

    def jugada(self) -> tuple:
        """Implementa <jugada> ::= <canto> <respuesta>.

        Returns:
            Una tupla ('jugada', canto, respuesta) que representa el AST.
        """
        canto = self.canto()
        respuesta = self.respuesta()
        return ('jugada', canto, respuesta)

    def canto(self) -> str:
        """Implementa <canto> ::= "truco".
        
        Returns:
            El lexema del token TRUCO consumido.
        """
        tok = self.match('TRUCO')
        if tok is not None: 
            return tok.lexeme
        self.error('Se esperaba "truco"')
        return None
        # TODO: Intentar consumir un token TRUCO con match().
        # Si no está, reportar error con self.error().
        # Devolver el lexema del token consumido, o None en caso de error.

    def respuesta(self) -> str:
        """Implementa <respuesta> ::= "quiero" | "no_quiero".

        Returns:
            El lexema del token QUIERO o NO_QUIERO consumido.
        """
        tok = self.match('QUIERO', 'NO_QUIERO')
        if tok is not None:
            return tok.lexeme
        self.error('Se esperaba "quiero" o "no_quiero"')
        return None
        # TODO: Intentar consumir QUIERO o NO_QUIERO con match().
        # Si no está ninguno, reportar error con self.error().
        # Devolver el lexema del token consumido, o None en caso de error.

    # ------------------------------------------------------------------
    # Método principal
    # ------------------------------------------------------------------

    def parse(self) -> tuple:
        """Inicia el análisis sintáctico y devuelve el AST con los errores.

        Returns:
            Una tupla (ast, errores) donde ast es el árbol sintáctico
            y errores es una lista de mensajes de error.
        """
        ast = self.jugada()
        if not self.is_at_end():
            self.error('Se esperaba fin de entrada pero hay tokens sobrantes')
        return ast, self.errors


# ---------------------------------------------------------------------------
# Función auxiliar para imprimir el AST
# ---------------------------------------------------------------------------

def print_ast(node: Any, indent: int = 0) -> None:
    """Recorre recursivamente el AST y lo imprime con indentación.

    Args:
        node: Nodo del AST (tupla, lista, str o None).
        indent: Nivel de indentación actual.
    """
    prefix = '  ' * indent
    if isinstance(node, tuple):
        print(prefix + node[0])
        for child in node[1:]:
            print_ast(child, indent + 1)
    elif isinstance(node, list):
        for item in node:
            print_ast(item, indent)
    elif node is not None:
        print(prefix + str(node))


# ---------------------------------------------------------------------------
# Pruebas manuales
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    # Simulamos tokens como objetos simples para probar (sin depender del lexer)
    class Token:
        def __init__(self, type_, lexeme, line=1):
            self.type = type_
            self.lexeme = lexeme
            self.line = line

    pruebas = [
        # (cadena, tokens simulados)
        ("truco quiero", [
            Token('TRUCO', 'truco'),
            Token('QUIERO', 'quiero'),
            Token('EOF', ''),
        ]),
        ("truco no_quiero", [
            Token('TRUCO', 'truco'),
            Token('NO_QUIERO', 'no_quiero'),
            Token('EOF', ''),
        ]),
        ("truco", [  # falta respuesta
            Token('TRUCO', 'truco'),
            Token('EOF', ''),
        ]),
        ("truco truco", [  # tokens sobrantes
            Token('TRUCO', 'truco'),
            Token('TRUCO', 'truco'),
            Token('EOF', ''),
        ]),
    ]

    for nombre, tokens in pruebas:
        print(f"\nEntrada: '{nombre}'")
        parser = Parser(tokens)
        ast, errores = parser.parse()
        if ast:
            print("AST:")
            print_ast(ast)
        if errores:
            print("Errores:")
            for e in errores:
                print(f"  {e}")
