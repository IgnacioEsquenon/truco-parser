# Bitácora de Aprendizaje y Actas de Reunión

Este documento registra las actividades, decisiones y aprendizajes del equipo durante el desarrollo del proyecto. Cada entrada incluye los datos de la reunión o jornada de trabajo, seguida de los aportes individuales de cada integrante.

---

## 14/06/2026 – Reunión 01: Jornada inicial de organización

**Temas tratados:**
- Evaluación y selección de fuentes bibliográficas para el proyecto.
- Definición de la estructura del repositorio y del documento académico.
- Planificación de tareas para la primera semana de desarrollo.
- Estrategia de colaboración en par entre los desarrolladores del lexer y del parser.
- Elección de roles del equipo:
    - Líder: Ignacio Esquenón
    - Arquitecto de Gramática: Andrés León Barberan
    - Desarrollador de Lexer: Geremias Benjamín Castillo
    - Desarrollador de Parser: Sebastián Exequiel Gómez
    - Documentador/Tester: Juan Cruz Senicen Acosta

**Decisiones tomadas:**
- Se adopta como guía práctica de implementación el libro "*Crafting Interpreters*" de Robert Nystrom [1].
- Se adopta como guía teórica principal el libro "*Introduction to the Theory of Computation*" de Michael Sipser [2].
- El lenguaje de implementación será Python 3, utilizando el módulo `re` de la biblioteca estándar para el analizador léxico.
- Los desarrolladores trabajarán en archivos separados (`lexer.py` y `parser.py`) y se integrarán mediante `main.py`.

---

### Ignacio Esquenón

**Tareas realizadas:**
- Creación del repositorio en GitHub (`truco-parser`) con la estructura de carpetas y archivos iniciales.
- Redacción del README.md con la descripción del proyecto.
- Delegación formal de responsabilidades:
    - Delegar la construcción de una gramática preliminar al arquitecto de gramática, sugiriendo el Capítulo 2 de [2].
    - Planificar la construcción del lexer y el parser por parte de los desarrolladores, sugiriendo las lecturas de los Capítulos 4 (scanning) 5 y 6 (Representing Code y Parsing) de [1].
    - Redacción inicial del documento de la segunda entrega parcial al documentador, siguiendo el formato del Anexo A.

**Aprendizajes:**
- La lectura del Capítulo 2 de [1] resultó fundamental para comprender el alcance del proyecto dentro del "mapa de la montaña": nuestro sistema abarca únicamente el frente (scanning + parsing), finalizando en la generación del AST.


---

### Andrés León Barberan (Arquitecto de gramática)

**Tareas realizadas:**
- Definición de la primera versión de la gramática libre de contexto para el lenguaje de rondas de Truco.
- Formalización de la 4-tupla (V, Σ, R, S) y escritura de las producciones.

**Aprendizajes:**
- Se identificaron las limitaciones iniciales de la gramática (terminación temprana, orden fijo envido-truco) que deberán revisarse antes de la implementación.

**Tareas realizadas:**
- Transición y adaptación de las reglas matemáticas clásicas hacia EBNF, incorporando operadores de opcionalidad (?) para optimizar y limpiar el diseño.
- Estratificación de los no terminales en niveles jerárquicos (separando las fases de Envido y Truco) para asegurar que la gramática sea no ambigua y respete el orden de los cantos.

**Aprendizajes:**
- Se comprendió el principio de diseño por el cual una gramática no debe contemplar la generación de jugadas ilegales para manejarlas; por el contrario, debe restringirse a generar únicamente secuencias válidas, permitiendo que el analizador sintáctico rechace naturalmente las entradas incorrectas.
- Se logró modelar con éxito la terminación temprana de una ronda sin introducir ambigüedad sintáctica, utilizando bifurcaciones estrictas que cierran el árbol de derivación de manera segura ante un rechazo.
---

### Geremias Castillo (Desarrollador del lexer)

**Tareas realizadas:**
- Planificación de la estructura del lexer en Python con el módulo `re`.
- Previsión del manejo de espacios, comentarios, conteo de líneas y detección de caracteres inesperados.

**Dificultades:**
- No se inició la implementación del lexer. La codificación se postergó para asegurar que la gramática estuviera revisada y estable antes de escribir el escáner.

**Aprendizajes:**
- La lectura del Capítulo 4 de [1] introdujo los conceptos de lexema, token y el funcionamiento de un escáner basado en expresiones regulares.

**Tareas realizadas:**
- Diseño de DFA para el Micro-Truco.
- Implementación de DFA en Python.
- Desarrollo de pruebas para verificar el funcionamiento del lexer.

**Dificultades:**
- Traslado de la teoría y lo aprendido a clase al desarrollo de código.

**Aprendizajes:**
- Comprensión de la necesidad de tener un DFA definido antes de comenzar a implementar el lexer.
- Utilizar los metodos auxiliares para implementar el lexer correctamente.
---

### Sebastián Gómez (Desarrollador del parser)

**Tareas realizadas:**
- Planificación de la arquitectura del parser descendente recursivo a partir de la gramática diseñada.

**Dificultades:**
- No se inició la implementación del parser. Al igual que con el lexer, se espera a que la gramática esté consolidada para comenzar la codificación.

**Aprendizajes:**
- El Capítulo 6 de [1] mostró cómo transformar una gramática LL(1) en código y cómo aplicar el modo pánico para continuar el análisis tras un error.

---

### Juan Cruz Senicen Acosta (Documentador / Tester)

**Tareas realizadas:**
- Redacción del documento de la segunda entrega parcial según el formato del Anexo A.
- Integración en el informe de la gramática formal, la planificación de la implementación y las secciones pendientes.
- Redacción del resumen y de la introducción, incluyendo objetivos y organización del equipo.

**Aprendizajes:**
- El uso de un formato académico estandarizado facilitó la organización del contenido y la comunicación clara del estado del proyecto.
