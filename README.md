# Analizador Sintáctico para Rondas de Truco

Proyecto integrador de Teoría de la Computación - FaCENA UNNE.

## Equipo

- Líder: Ignacio Agustín Esquenón
- Arquitecto de gramática: Andres Leon Barberan
- Desarrollador del lexer: Geremias Benjamin Castillo
- Desarrollador del parser: Sebastian Exequiel Gomez
- Documentador / Tester: Juan Cruz Senicen Acosta

## Descripción

Este proyecto implementa un analizador léxico-sintáctico para un lenguaje formal
de dominio específico que describe rondas válidas del juego de cartas Truco. El
sistema recibe una cadena de texto con la secuencia de cantos y resultados de una
ronda, y determina si es sintácticamente válida, generando un árbol sintáctico
abstracto (AST) en caso afirmativo o reportando errores en caso contrario. La
gramática del lenguaje está definida formalmente como una Gramática Libre de
Contexto (GLC) no ambigua y de clase LL(1), lo que permite su análisis mediante
un parser descendente recursivo. El desarrollo se organizó en dos fases: una
primera de aprendizaje sobre un prototipo mínimo (Micro-Truco) y una segunda
donde se implementó el analizador completo utilizando el módulo `re` de Python
para el lexer y descenso recursivo con recuperación de errores en modo pánico
para el parser.

## Estructura del proyecto

- `src/` - Código fuente del proyecto final (lexer, parser, punto de entrada)
- `micro-truco/` - Prototipo de práctica para la Fase 1 (lexer y parser mínimos)
- `tests/` - Casos de prueba válidos e inválidos
- `docs/` - Documentación e informes
- `presentacion/` - Presentación para la exposición oral

## Ejecución

1. Clonar el repositorio.
3. Ejecutar `python src/main.py` para el modo interactivo.
   - Escribir la partida, se puede presionar Enter para escribir la partida en varias líneas, presionar Enter con una línea vacía ejecuta el programa.
4. Opciones adicionales:
   - `python src/main.py "truco quiero ; envido no_quiero"` (modo cadena directa).
   - `python src/main.py --file tests/casos_validos.txt` (modo archivo).
