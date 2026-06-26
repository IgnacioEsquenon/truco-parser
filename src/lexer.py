# lexer.py
# Analizador léxico para el lenguaje de partidas de Truco.
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
# Terminales (Σ): envido, real_envido, falta_envido, truco, retruco,
#                 vale_cuatro, quiero, no_quiero, ";", EOF.
#
# Basado en el Capítulo 4 de Crafting Interpreters (Nystrom, 2021).
# Utiliza el módulo re para el escaneo.

import re
from typing import List

class Token:
    """Representa un token generado por el lexer."""
    def __init__(self, type_: str, lexeme: str, line: int) -> None:
        self.type = type_
        self.lexeme = lexeme
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, '{self.lexeme}', line={self.line})"


class Scanner:
    """Escáner que convierte código fuente en una lista de tokens."""

    # Tabla de patrones ordenados por especificidad (más largos primero)
    TOKEN_PATTERNS = [
        ('REAL_ENVIDO',  r'real_envido'),
        ('FALTA_ENVIDO', r'falta_envido'),
        ('ENVIDO',       r'envido'),
        ('VALE_CUATRO',  r'vale_cuatro'),
        ('RETRUCO',      r'retruco'),
        ('TRUCO',        r'truco'),
        ('QUIERO',       r'quiero'),
        ('NO_QUIERO',    r'no_quiero'),
        ('PUNTO_Y_COMA', r';'),
        ('SKIP',         r'[ \t]+'),      # espacios y tabs
        ('NEWLINE',      r'\n'),          # saltos de línea
        ('COMMENT',      r'#.*'),         # comentarios hasta fin de línea
        # Secuencia de caracteres no esperados (fallback)
        ('ERROR',        r'[^\s;]+'),
    ]

    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.pos = 0
        self.line = 1

    def is_at_end(self) -> bool:
        return self.pos >= len(self.source)

    def tokenize(self) -> List[Token]:
        while not self.is_at_end():
            matched = False
            for token_type, pattern in self.TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.source, self.pos)
                if match:
                    lexeme = match.group()

                    if token_type == 'COMMENT' or token_type == 'SKIP':
                        pass
                    elif token_type == 'NEWLINE' :
                        self.line += 1
                    elif token_type == 'ERROR':
                        self.tokens.append(
                            Token('ERROR', lexeme, self.line)
                        )
                    else:
                        self.tokens.append(
                            Token(token_type, lexeme, self.line)
                        )

                    self.pos = match.end()
                    matched = True
                    break

            if not matched:
                self.tokens.append(
                    Token('ERROR', self.source[self.pos], self.line)
                )
                self.pos += 1

        self.tokens.append(Token('EOF', '', self.line))
        return self.tokens


# ---------------------------------------------------------------------------
# Pruebas manuales
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    pruebas = [
        "envido quiero",
        "truco quiero",
        "envido no_quiero truco retruco no_quiero",
        "envido quiero ; truco no_quiero",
        "# esto es un comentario\ntruco quiero",
        "truco quiero turco",
        "envido real_envido envido quiero",
        "truco quiero truco quiero"
    ]

    for codigo in pruebas:
        print(f"\nEntrada: {repr(codigo)}")
        scanner = Scanner(codigo)
        tokens = scanner.tokenize()
        for token in tokens:
            if token.type == 'ERROR':
                print(f"  ⚠️  ERROR léxico: lexema '{token.lexeme}' en línea {token.line}")
            else:
                print(f"  {token}")