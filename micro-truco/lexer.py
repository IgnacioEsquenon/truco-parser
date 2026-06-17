# micro_lexer.py
# Analizador léxico para el lenguaje "Micro-Truco"
# Gramática: <jugada> ::= <canto> <respuesta>
#            <canto> ::= "truco"
#            <respuesta> ::= "quiero" | "no_quiero"
#
# Basado en el Capítulo 4 de Crafting Interpreters (Nystrom, 2021).
# Implementa un Autómata Finito Determinista (DFA) que reconoce
# los lexemas "truco", "quiero" y "no_quiero", ignorando espacios.

from typing import List, NoReturn

# ---------------------------------------------------------------------------
# Clase Token
# ---------------------------------------------------------------------------

class Token:
    """Representa un token generado por el lexer.

    Atributos:
        type (str): Tipo del token. Valores posibles:
                    'TRUCO', 'QUIERO', 'NO_QUIERO', 'EOF'.
        lexeme (str): La subcadena exacta de la entrada que forma el token.
        line (int): Número de línea donde se encontró el token.
    """

    def __init__(self, type_: str, lexeme: str, line: int) -> None:
        """Crea un nuevo token.

        Args:
            type_: Tipo de token (ej. 'TRUCO').
            lexeme: Subcadena del código fuente (ej. 'truco').
            line: Número de línea (1 en el Micro-Truco).
        """
        self.type: str = type_
        self.lexeme: str = lexeme
        self.line: int = line

    def __repr__(self) -> str:
        """Representación legible del token para depuración."""
        return f"Token({self.type}, '{self.lexeme}', line={self.line})"


# ---------------------------------------------------------------------------
# Clase Scanner (Lexer)
# ---------------------------------------------------------------------------

class Scanner:
    """Escáner que convierte una cadena de entrada en una lista de tokens.

    Atributos:
        source (str): Código fuente completo a analizar.
        tokens (List[Token]): Lista donde se acumulan los tokens generados.
        start (int): Posición de inicio del lexema actual.
        current (int): Posición actual del cursor sobre la cadena.
        line (int): Contador de líneas (fijo en 1 para el Micro-Truco).
    """

    def __init__(self, source: str) -> None:
        """Inicializa el escáner con el código fuente.

        Args:
            source: Cadena de texto con la jugada a analizar.
        """
        self.source: str = source
        self.tokens: List[Token] = []
        self.start: int = 0       # inicio del lexema actual
        self.current: int = 0     # posición actual del cursor
        self.line: int = 1        # simplificado: todo en línea 1

    # ------------------------------------------------------------------
    # Métodos auxiliares
    # ------------------------------------------------------------------

    def is_at_end(self) -> bool:
        """Indica si se ha consumido toda la entrada.

        Returns:
            True si el cursor llegó al final de source, False en caso contrario.
        """
        return self.current >= len(self.source)

    def advance(self) -> str:
        """Avanza una posición y retorna el carácter consumido.

        Equivale a leer el siguiente carácter y mover la cabeza lectora hacia adelante.

        Returns:
            El carácter que se encontraba en la posición actual antes de avanzar.
        """
        c: str = self.source[self.current]
        self.current += 1
        return c

    def peek(self) -> str:
        """Observa el carácter actual sin consumirlo.

        Si el cursor está al final, retorna el carácter nulo como centinela.

        Returns:
            El carácter en la posición actual, o '\\0' si es el final.
        """
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def consume_error(self) -> None:
        """Consume caracteres hasta encontrar un espacio o el final de la cadena,
        y registra un único token de tipo ERROR.
        """
        while not self.is_at_end() and self.peek() != ' ' and self.peek() != '\0':
            self.advance()
        self.add_token('ERROR')
    
    def add_token(self, type_: str) -> None:
        """Crea un token del tipo dado y lo agrega a la lista de tokens.

        El lexema se extrae como la subcadena entre self.start y self.current.

        Args:
            type_: Tipo de token (ej. 'TRUCO').
        """
        lexeme: str = self.source[self.start:self.current]
        self.tokens.append(Token(type_, lexeme, self.line))

    # ------------------------------------------------------------------
    # Lógica de escaneo (a completar por el desarrollador)
    # ------------------------------------------------------------------

    def scan_token(self) -> None:
        char = self.advance()
        
        if char == ' ' or char == '\0':       
            return
        
        # --- Caso TRUCO ---
        elif char == 't':
            if self.peek() == 'r':
                self.advance() 
                if self.peek() == 'u':
                    self.advance() 
                    if self.peek() == 'c':
                        self.advance() 
                        if self.peek() == 'o':
                            self.advance() 
                            return self.add_token('TRUCO')
            
            
            return self.consume_error()
        
        elif char == 'q':
            if self.peek() == 'u':
                self.advance()
                if self.peek() == 'i':
                    self.advance()
                    if self.peek() == 'e':
                        self.advance()
                        if self.peek() == 'r':
                            self.advance()
                            if self.peek() == 'o':
                                self.advance()
                                return self.add_token('QUIERO')
            
            return self.consume_error()
        
        elif char == 'n':
            if self.peek() == 'o':
                self.advance()
                if self.peek() == '_':
                    self.advance()
                    if self.peek() == 'q':
                        self.advance()
                        if self.peek() == 'u':
                            self.advance()
                            if self.peek() == 'i':
                                self.advance()
                                if self.peek() == 'e':
                                    self.advance()
                                    if self.peek() == 'r':
                                        self.advance()
                                        if self.peek() == 'o':
                                            self.advance()
                                            return self.add_token('NO_QUIERO')
            
            return self.consume_error()

        else: 
            return self.consume_error()

    def scan_tokens(self) -> List[Token]:
        """Bucle principal que escanea todos los tokens de la entrada.

        Se ejecuta hasta consumir toda la cadena. Al finalizar, agrega
        el token especial EOF (End Of File).

        Returns:
            Lista de tokens reconocidos, incluyendo el token EOF al final.
        """
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token('EOF', '', self.line))
        return self.tokens


# ---------------------------------------------------------------------------
# Pruebas manuales
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    pruebas: List[str] = [
        " truco quiero ",
        "truco no_quiero",
        "truco truco",
        "truco",                    # falta respuesta, pero el lexer lo acepta
        "truco quiero no_quiero",   # secuencia más larga
        "truco x",                  # error léxico
        "traco quiero"              # error léxico
    ]
    for codigo in pruebas:
        print(f"\nEntrada: '{codigo}'")
        scanner: Scanner = Scanner(codigo)
        tokens: List[Token] = scanner.scan_tokens()
        for token in tokens:
            if "ERROR" in token.type:
                print("Error lexico detectado!")
            else:
                print(f"  {token}")
            
            
        
