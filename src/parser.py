# parser.py
# Parser descendente recursivo para el lenguaje de partidas de Truco.
# Gramática final (BNF, versión verificada con FIRST/FOLLOW):
#   PARTIDA        → RONDA RESTO_PARTIDA
#   RESTO_PARTIDA  → ";" RONDA RESTO_PARTIDA | ε
#   RONDA          → ENVIDO TRUCO | TRUCO
#   ENVIDO         → "envido" R1 | "real_envido" R3 | "falta_envido" RE
#   R1             → "envido" R2 | "real_envido" R3 | "falta_envido" RE | RE
#   R2             → "real_envido" R3 | "falta_envido" RE | RE
#   R3             → "falta_envido" RE | RE
#   RE             → "quiero" | "no_quiero"
#   TRUCO          → "truco" RT | ε
#   RT             → "retruco" RT1 | RE
#   RT1            → "vale_cuatro" RE | RE
#
# Basado en el Capítulo 6 de Crafting Interpreters (Nystrom, 2021)
# y en las definiciones de FIRST/FOLLOW del Dragon Book (Aho et al., 2006).
# Construye un AST como tuplas anidadas.
# Implementa modo pánico: sincroniza en ";" y EOF tras un error sintáctico.

from typing import List, Tuple, Optional, Any


class Parser:
    """Analizador sintáctico descendente recursivo para el lenguaje de Truco."""

    def __init__(self, tokens: List[Any]) -> None:
        self.tokens = tokens
        self.current = 0
        self.errors: List[str] = []

    # ------------------------------------------------------------------
    # Métodos auxiliares
    # ------------------------------------------------------------------

    def peek(self) -> str:
        """Devuelve el tipo del token actual sin consumirlo."""
        return self.tokens[self.current].type

    def is_at_end(self) -> bool:
        """Verifica si se alcanzó el token EOF."""
        return self.peek() == 'EOF'

    def advance(self) -> Any:
        """Consume el token actual y avanza al siguiente."""
        tok = self.tokens[self.current]
        self.current += 1
        return tok

    def previous(self) -> Any:
        """Devuelve el token que se acaba de consumir."""
        return self.tokens[self.current - 1]

    def check(self, type_: str) -> bool:
        """Devuelve True si el token actual es del tipo dado, sin consumirlo.
        Los tokens de error léxico se tratan como un caso especial.
        """
        if self.is_at_end():
            return False
        if self.peek() == 'ERROR':
            self._handle_lexical_error()
            return False
        return self.peek() == type_

    def match(self, *types: str) -> Optional[Any]:
        """Si el token actual coincide con alguno de los tipos, lo consume y lo devuelve.
        Si no coincide, devuelve None y no consume nada.
        """
        for type_ in types:
            if self.check(type_):
                return self.advance()
        return None

    def _handle_lexical_error(self) -> None:
        """Reporta un error léxico y descarta el token problemático."""
        token = self.tokens[self.current]
        self.errors.append(
            f"[línea {token.line}] Error léxico: Carácter o palabra no reconocida '{token.lexeme}'."
        )
        self.advance()

    def error(self, message: str) -> None:
        """Registra un error sintáctico y aplica modo pánico."""
        token_error = self.tokens[self.current]
        line = token_error.line if token_error else '?'
        found = token_error.lexeme if token_error and token_error.type != 'EOF' else 'EOF'
        self.errors.append(
            f"[línea {line}] Error sintáctico: {message} (encontrado '{found}')"
        )

        # Modo pánico: descartar tokens hasta encontrar un sincronizador,
        # pero sin consumirlo (se deja disponible para resto_partida)
        while not self.is_at_end() and self.peek() not in ('PUNTO_Y_COMA', 'EOF'):
            self.advance()
        # No consumir el sincronizador

    # ------------------------------------------------------------------
    # Métodos por cada no terminal de la gramática
    # ------------------------------------------------------------------

    def partida(self) -> Tuple[str, Any]:
        """PARTIDA → RONDA RESTO_PARTIDA."""
        ronda = self.ronda()
        resto = self.resto_partida()
        return ('PARTIDA', ronda, resto)

    def resto_partida(self) -> Optional[Any]:
        """RESTO_PARTIDA → ";" RONDA RESTO_PARTIDA | ε."""
        if self.match('PUNTO_Y_COMA'):
            ronda = self.ronda()
            resto = self.resto_partida()
            return ('RESTO_PARTIDA', ronda, resto)
        return None

    def ronda(self) -> Tuple[str, Any, Any]:
        """RONDA → ENVIDO TRUCO | TRUCO."""
        # Si el token actual no puede iniciar una ronda, es un error
        if not self.is_at_end() and self.peek() not in (
            'ENVIDO', 'REAL_ENVIDO', 'FALTA_ENVIDO', 'TRUCO',
            'PUNTO_Y_COMA', 'EOF'
        ):
            self.error("Se esperaba inicio de ronda (envido, real_envido, falta_envido, truco)")
            return ('RONDA', None, None)

        env = self.envido()
        tru = self.truco()
        return ('RONDA', env, tru)

    # ---- Envido ----

    def envido(self) -> Optional[Any]:
        """ENVIDO → 'envido' R1 | 'real_envido' R3 | 'falta_envido' RE | ε."""
        if self.match('ENVIDO'):
            return ('ENVIDO', 'envido', self.r1())
        elif self.match('REAL_ENVIDO'):
            return ('ENVIDO', 'real_envido', self.r3())
        elif self.match('FALTA_ENVIDO'):
            return ('ENVIDO', 'falta_envido', self.re())
        return None

    def r1(self) -> Any:
        """R1 → 'envido' R2 | 'real_envido' R3 | 'falta_envido' RE | RE."""
        if self.match('ENVIDO'):
            return ('R1', 'envido', self.r2())
        elif self.match('REAL_ENVIDO'):
            return ('R1', 'real_envido', self.r3())
        elif self.match('FALTA_ENVIDO'):
            return ('R1', 'falta_envido', self.re())
        elif self.match('QUIERO', 'NO_QUIERO'):
            return ('R1', self.previous().lexeme)
        else:
            self.error("Se esperaba envido, real_envido, falta_envido o respuesta ('quiero'/'no_quiero')")
            return ('R1', None)

    def r2(self) -> Any:
        """R2 → 'real_envido' R3 | 'falta_envido' RE | RE."""
        if self.match('REAL_ENVIDO'):
            return ('R2', 'real_envido', self.r3())
        elif self.match('FALTA_ENVIDO'):
            return ('R2', 'falta_envido', self.re())
        elif self.match('QUIERO', 'NO_QUIERO'):
            return ('R2', self.previous().lexeme)
        else:
            self.error("Se esperaba real_envido, falta_envido o respuesta ('quiero'/'no_quiero')")
            return ('R2', None)

    def r3(self) -> Any:
        """R3 → 'falta_envido' RE | RE."""
        if self.match('FALTA_ENVIDO'):
            return ('R3', 'falta_envido', self.re())
        elif self.match('QUIERO', 'NO_QUIERO'):
            return ('R3', self.previous().lexeme)
        else:
            self.error("Se esperaba falta_envido o respuesta ('quiero'/'no_quiero')")
            return ('R3', None)

    def re(self) -> Optional[str]:
        """RE → 'quiero' | 'no_quiero'."""
        if self.is_at_end():
            self.error("Se esperaba 'quiero' o 'no_quiero'")
            return None
        if self.match('QUIERO', 'NO_QUIERO'):
            return self.previous().lexeme
        self.error("Se esperaba 'quiero' o 'no_quiero'")
        return None

    # ---- Truco ----

    def truco(self) -> Optional[Any]:
        """TRUCO → 'truco' RT | ε."""
        if self.match('TRUCO'):
            return ('TRUCO', 'truco', self.rt())
        return None

    def rt(self) -> Any:
        """RT → 'retruco' RT1 | RE."""
        if self.is_at_end():
            self.error("Se esperaba 'retruco' o respuesta ('quiero'/'no_quiero')")
            return ('RT', None)
        if self.match('RETRUCO'):
            return ('RT', 'retruco', self.rt1())
        elif self.match('QUIERO', 'NO_QUIERO'):
            return ('RT', self.previous().lexeme)
        else:
            self.error("Se esperaba 'retruco' o respuesta ('quiero'/'no_quiero')")
            return ('RT', None)

    def rt1(self) -> Any:
        """RT1 → 'vale_cuatro' RE | RE."""
        if self.is_at_end():
            self.error("Se esperaba 'vale_cuatro' o respuesta ('quiero'/'no_quiero')")
            return ('RT1', None)
        if self.match('VALE_CUATRO'):
            return ('RT1', 'vale_cuatro', self.re())
        elif self.match('QUIERO', 'NO_QUIERO'):
            return ('RT1', self.previous().lexeme)
        else:
            self.error("Se esperaba 'vale_cuatro' o respuesta ('quiero'/'no_quiero')")
            return ('RT1', None)

    # ------------------------------------------------------------------
    # Método principal
    # ------------------------------------------------------------------

    def parse(self) -> Tuple[Optional[Tuple], List[str]]:
        """Inicia el análisis sintáctico y devuelve el AST con los errores."""
        ast = self.partida()
        if not self.is_at_end():
            # Buscar el primer token sobrante relevante
            primer_sobrante = None
            temp_current = self.current
            while temp_current < len(self.tokens) and self.tokens[temp_current].type != 'EOF':
                if self.tokens[temp_current].type != 'ERROR':
                    primer_sobrante = self.tokens[temp_current]
                    break
                temp_current += 1
            if primer_sobrante:
                self.errors.append(
                    f"[línea {primer_sobrante.line}] Error sintáctico: Se esperaba fin de entrada pero hay tokens sobrantes (encontrado '{primer_sobrante.lexeme}')"
                )
            else:
                self.errors.append(
                    f"[línea {self.previous().line}] Error sintáctico: Se esperaba fin de entrada pero hay tokens sobrantes"
                )
        return ast, self.errors


# ---------------------------------------------------------------------------
# Impresión del AST (estilo "tree" de Unix)
# ---------------------------------------------------------------------------

def print_ast(node: Any, indent: str = "", is_last: bool = True) -> None:
    """Imprime el AST con conectores de árbol (estilo 'tree' de Unix).

    Args:
        node: Nodo del AST (tupla, lista, str o None).
        indent: Cadena de indentación acumulada.
        is_last: Indica si el nodo actual es el último hijo de su padre.
    """
    if node is None:
        return

    branch = "└── " if is_last else "├── "
    pipe = "    " if is_last else "│   "

    if isinstance(node, tuple):
        print(indent + branch + str(node[0]))
        children = [c for c in node[1:] if c is not None]
        for i, child in enumerate(children):
            last_child = (i == len(children) - 1)
            print_ast(child, indent + pipe, last_child)

    elif isinstance(node, list):
        for i, item in enumerate(node):
            last_item = (i == len(node) - 1)
            print_ast(item, indent, last_item)

    elif node is not None:
        print(indent + branch + str(node))


# ---------------------------------------------------------------------------
# Pruebas autónomas (sin dependencia del lexer)
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    class Token:
        def __init__(self, type_: str, lexeme: str = '', line: int = 1):
            self.type = type_
            self.lexeme = lexeme
            self.line = line

    def probar(entrada: str, tokens: List[Token]) -> None:
        print(f"\n{'='*60}")
        print(f"ENTRADA: {entrada}")
        parser = Parser(tokens)
        ast, errores = parser.parse()
        if ast:
            print("AST:")
            print_ast(ast)
        if errores:
            print("ERRORES:")
            for err in errores:
                print(f"  {err}")

    # Casos válidos
    probar("envido quiero", [
        Token('ENVIDO', 'envido'), Token('QUIERO', 'quiero'), Token('EOF')])
    probar("truco quiero", [
        Token('TRUCO', 'truco'), Token('QUIERO', 'quiero'), Token('EOF')])
    probar("envido no_quiero truco retruco no_quiero", [
        Token('ENVIDO', 'envido'), Token('NO_QUIERO', 'no_quiero'),
        Token('TRUCO', 'truco'), Token('RETRUCO', 'retruco'),
        Token('NO_QUIERO', 'no_quiero'), Token('EOF')])
    probar("envido quiero ; truco no_quiero", [
        Token('ENVIDO', 'envido'), Token('QUIERO', 'quiero'),
        Token('PUNTO_Y_COMA', ';'),
        Token('TRUCO', 'truco'), Token('NO_QUIERO', 'no_quiero'), Token('EOF')])
    probar("envido envido real_envido falta_envido no_quiero truco retruco vale_cuatro quiero ; truco no_quiero", [
        Token('ENVIDO', 'envido'), Token('ENVIDO', 'envido'),
        Token('REAL_ENVIDO', 'real_envido'), Token('FALTA_ENVIDO', 'falta_envido'),
        Token('NO_QUIERO', 'no_quiero'),
        Token('TRUCO', 'truco'), Token('RETRUCO', 'retruco'),
        Token('VALE_CUATRO', 'vale_cuatro'), Token('QUIERO', 'quiero'),
        Token('PUNTO_Y_COMA', ';'),
        Token('TRUCO', 'truco'), Token('NO_QUIERO', 'no_quiero'), Token('EOF')])

    # Casos inválidos
    probar("retruco quiero", [
        Token('RETRUCO', 'retruco'), Token('QUIERO', 'quiero'), Token('EOF')])
    probar("envido real_envido envido quiero", [
        Token('ENVIDO', 'envido'), Token('REAL_ENVIDO', 'real_envido'),
        Token('ENVIDO', 'envido'), Token('QUIERO', 'quiero'), Token('EOF')])
    probar("truco", [
        Token('TRUCO', 'truco'), Token('EOF')])
    probar("truco vale_cuatro quiero", [
        Token('TRUCO', 'truco'), Token('VALE_CUATRO', 'vale_cuatro'),
        Token('QUIERO', 'quiero'), Token('EOF')])
    probar(";", [
        Token('PUNTO_Y_COMA', ';'), Token('EOF')])
    probar("truco quiero ;", [
        Token('TRUCO', 'truco'), Token('QUIERO', 'quiero'),
        Token('PUNTO_Y_COMA', ';'), Token('EOF')])