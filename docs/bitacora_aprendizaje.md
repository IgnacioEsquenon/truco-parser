# Bitácora de Aprendizaje y Actas de Reunión

Este documento registra las actividades, decisiones y aprendizajes del equipo
durante el desarrollo del proyecto. Cada entrada incluye los datos de la reunión
o jornada de trabajo, seguida de los aportes individuales de cada integrante.

---

## 14/06/2026 – Jornada 1: Organización y planificación inicial

**Temas tratados:**
- Selección de fuentes bibliográficas: *Crafting Interpreters* (Nystrom) como
  guía de implementación y *Introduction to the Theory of Computation* (Sipser)
  como referencia teórica.
- Definición de la estructura del repositorio y del documento académico.
- Asignación de roles: Ignacio Esquenón (líder), Andrés Barberan (arquitecto de
  gramática), Geremias Castillo (desarrollador del lexer), Sebastián Gómez
  (desarrollador del parser), Juan Cruz Senicen Acosta (documentador/tester).
- Estrategia de trabajo: los desarrolladores crearán archivos separados
  (`lexer.py` y `parser.py`) y se integrarán con `main.py`.

**Decisiones tomadas:**
- El lenguaje de implementación será Python 3, con el módulo `re` para el lexer.
- Se posterga la codificación hasta que la gramática esté consolidada.
- Se organiza el desarrollo en dos fases: una de aprendizaje (Micro-Truco) y
  otra de implementación completa.

---

### Ignacio Esquenón (Líder)

**Tareas realizadas:**
- Creación del repositorio en GitHub (`truco-parser`) con la estructura inicial
  de carpetas.
- Redacción del README.md con la descripción del proyecto.
- Delegación formal de responsabilidades:
  - Al arquitecto de gramática, la construcción de una gramática preliminar
    (sugiriendo el Capítulo 2 de Sipser).
  - A los desarrolladores, la lectura de los Capítulos 4, 5 y 6 de Nystrom y la
    planificación del lexer y parser.
  - Al documentador, la redacción inicial del documento de la segunda entrega
    parcial siguiendo el formato del Anexo A.

**Aprendizajes:**
- La lectura del Capítulo 2 de Nystrom (metáfora de la montaña) resultó
  fundamental para entender el alcance del proyecto: nuestro sistema abarca
  únicamente el frente del compilador (scanning + parsing) y el AST es la cima
  que debemos alcanzar.

---

### Andrés León Barberan (Arquitecto de gramática)

**Tareas realizadas:**
- Definición de la primera versión de la GLC para el lenguaje de rondas de
  Truco.
- Formalización de la 4-tupla (V, Σ, R, S) y escritura de las producciones.

**Aprendizajes:**
- Se identificaron las limitaciones iniciales de la gramática (terminación
  temprana por `no_quiero`, orden fijo envido-truco) que deberán revisarse
  antes de la implementación.

---

### Geremias Castillo (Desarrollador del lexer)

**Tareas realizadas:**
- Planificación de la estructura del lexer en Python con el módulo `re`.
- Previsión del manejo de espacios, comentarios, conteo de líneas y detección
  de caracteres inesperados.

**Dificultades:**
- La codificación se postergó para asegurar que la gramática estuviera
  revisada y estable antes de escribir el escáner.

**Aprendizajes:**
- La lectura del Capítulo 4 de Nystrom introdujo los conceptos de lexema,
  token y el funcionamiento de un escáner basado en expresiones regulares.

---

### Sebastián Gómez (Desarrollador del parser)

**Tareas realizadas:**
- Planificación de la arquitectura del parser descendente recursivo a partir
  de la gramática diseñada.

**Dificultades:**
- Al igual que con el lexer, se esperó a que la gramática estuviera
  consolidada para comenzar la codificación.

**Aprendizajes:**
- El Capítulo 6 de Nystrom mostró cómo transformar una gramática LL(1) en
  código y cómo aplicar el modo pánico para continuar el análisis tras un
  error.

---

### Juan Cruz Senicen Acosta (Documentador / Tester)

**Tareas realizadas:**
- Redacción del documento de la segunda entrega parcial según el formato del
  Anexo A.
- Integración en el informe de la gramática formal, la planificación de la
  implementación y las secciones pendientes.
- Redacción del resumen y de la introducción, incluyendo objetivos y
  organización del equipo.

**Aprendizajes:**
- El uso de un formato académico estandarizado facilitó la organización del
  contenido y la comunicación clara del estado del proyecto.

---

## 17/06/2026 – Jornada 2: Diseño de la gramática y prototipo Micro‑Truco

**Temas tratados:**
- Presentación de la gramática formal por parte del arquitecto.
- Puesta en común de los resultados del prototipo Micro‑Truco.
- Revisión del esqueleto del informe final y del Marco Teórico.

---

### Ignacio Esquenón (Líder)

**Tareas realizadas:**
- Coordinación de la reunión de puesta en común.
- Actualización de la bitácora con los aprendizajes de la jornada.
- Ajuste del cronograma para la fase de implementación final.

**Aprendizajes:**
- La separación en dos fases (Micro‑Truco + Truco completo) redujo la fricción
  inicial y permitió que los desarrolladores llegaran a la implementación final
  con mayor confianza.

---

### Andrés León Barberan (Arquitecto de gramática)

**Tareas realizadas:**
- Transición y adaptación de las reglas iniciales hacia EBNF, incorporando
  operadores de opcionalidad (`?`) para optimizar el diseño.
- Estratificación de los no terminales en niveles jerárquicos (separando las
  fases de Envido y Truco) para asegurar la no ambigüedad y el orden de los
  cantos.
- Explicación al equipo de la estructura formal de la gramática y de las
  decisiones de diseño.

**Aprendizajes:**
- Se comprendió que una gramática no debe contemplar la generación de jugadas
  ilegales para luego manejarlas, sino restringirse a generar únicamente
  secuencias válidas.
- Se logró modelar la terminación temprana de una ronda sin introducir
  ambigüedad, utilizando bifurcaciones estrictas que cierran el árbol de
  derivación ante un rechazo.

---

### Geremias Castillo (Desarrollador del lexer)

**Tareas realizadas:**
- Diseño del DFA para el lenguaje Micro‑Truco.
- Implementación del DFA en Python utilizando exclusivamente estructuras
  `if‑elif` y los métodos auxiliares del escáner.
- Desarrollo de pruebas para verificar el funcionamiento del lexer con los
  lexemas `truco`, `quiero` y `no_quiero`.

**Dificultades:**
- Traslado de la teoría de autómatas finitos al desarrollo de código
  concreto.

**Aprendizajes:**
- Es indispensable tener un DFA definido antes de comenzar a implementar el
  lexer.
- Los métodos auxiliares (`advance`, `peek`, `add_token`) permiten implementar
  el lexer de manera clara y ordenada.

---

### Sebastián Gómez (Desarrollador del parser)

**Tareas realizadas:**
- Implementación de un parser descendente recursivo para la gramática del
  Micro‑Truco.
- Integración con el lexer desarrollado por Geremias y generación de un AST
  simple.
- Verificación de que el parser rechaza correctamente entradas inválidas.

**Aprendizajes:**
- La experiencia permitió dominar los métodos auxiliares (`match`, `check`,
  `peek`) y visualizar el parser como un autómata de pila determinista.
- Comprender la traducción directa de reglas gramaticales a métodos de una
  clase facilitó el posterior desarrollo del parser completo.

---

### Juan Cruz Senicen Acosta (Documentador / Tester)

**Tareas realizadas:**
- Redacción del Marco Teórico del informe final, con referencias a Sipser,
  Nystrom y el Dragon Book.
- Elaboración de la justificación del prototipo Micro‑Truco como estrategia de
  aprendizaje.
- Preparación de los archivos iniciales de casos de prueba.

**Aprendizajes:**
- Documentar el proceso de aprendizaje mientras se desarrolla evita que se
  pierdan detalles relevantes para el informe final.

---

## 24‑25/06/2026 – Jornada 3: Implementación final, pruebas y ajustes

**Temas tratados:**
- Integración del lexer y parser finales.
- Ejecución de la batería completa de 55 casos de prueba.
- Corrección de errores en el modo pánico y en los mensajes de error.
- Redacción de las secciones finales del informe.

---

### Ignacio Esquenón (Líder)

**Tareas realizadas:**
- Supervisión de la integración entre `lexer.py`, `parser.py` y `main.py`.
- Revisión del informe final y verificación del cumplimiento del formato del
  Anexo A.
- Preparación del archivo `.zip` para la entrega final.

**Aprendizajes:**
- La integración del modo pánico con el separador de rondas fue la parte más
  delicada del proyecto; fue necesario iterar varias veces para lograr que el
  parser continuara correctamente tras cada error.
- La bitácora de aprendizaje sirvió como registro útil para retomar decisiones
  durante la escritura del informe final.

---

### Andrés León Barberan (Arquitecto de gramática)

**Tareas realizadas:**
- Redacción de la sección "Diseño de la Gramática" del informe final,
  incluyendo las tablas de FIRST/FOLLOW y la verificación LL(1).
- Verificación de que el parser implementado respetara fielmente las
  producciones de la gramática BNF.

**Aprendizajes:**
- La verificación formal con FIRST/FOLLOW (Dragon Book) fue fundamental para
  tener la certeza de que la gramática era LL(1) y que el descenso recursivo
  no requeriría retroceso.

---

### Geremias Castillo (Desarrollador del lexer)

**Tareas realizadas:**
- Implementación del lexer final (`src/lexer.py`) con una tabla de patrones
  basada en el módulo `re`, ordenada por especificidad.
- Incorporación del manejo de comentarios (`#`), conteo de líneas y emisión de
  tokens `ERROR` para caracteres no reconocidos.

**Aprendizajes:**
- La experiencia previa con el DFA manual permitió comprender qué hace el
  módulo `re` internamente, usándolo con pleno conocimiento de su mecanismo.

---

### Sebastián Gómez (Desarrollador del parser)

**Tareas realizadas:**
- Codificación de los once métodos correspondientes a los no terminales de la
  gramática BNF final, incluyendo la producción recursiva `resto_partida()`.
- Implementación del modo pánico en el método `error()`: ante un token
  inesperado, se descartan tokens hasta encontrar `;` o `EOF` sin consumirlos.
- Refinamiento de los mensajes de error para que cada método indique las
  alternativas esperadas y el token encontrado.

**Dificultades:**
- Fue necesario iterar sobre la interacción entre `match()`, `check()` y
  `error()` para evitar que los tokens de error léxico activaran el modo
  pánico de forma innecesaria.

**Aprendizajes:**
- La integración del modo pánico con el separador de rondas requirió un ajuste
  cuidadoso, pero una vez logrado permitió que el parser reportara todos los
  errores de una partida larga sin detenerse.

---

### Juan Cruz Senicen Acosta (Documentador / Tester)

**Tareas realizadas:**
- Ejecución de la batería de 55 casos de prueba (38 válidos y 17 inválidos) y
  comparación de salidas esperadas con obtenidas.
- Ajuste de los mensajes de error en la tabla de pruebas para reflejar
  fielmente los resultados del sistema.
- Redacción de las secciones "Casos de Prueba y Resultados", "Discusión y
  Análisis" y "Conclusiones" del informe final.

**Aprendizajes:**
- La tabla de pruebas resultó una herramienta esencial para detectar
  comportamientos inconsistentes del parser y guiar las correcciones de la
  última jornada.
