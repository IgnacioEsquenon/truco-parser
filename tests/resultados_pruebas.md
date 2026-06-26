# Resultados de las Pruebas del Analizador de Truco

| Cadena de Entrada | Salida Esperada | Salida Obtenida | Estado |
| :--- | :--- | :--- | :--- |
| (cadena vacía) | AST de ronda vacía y mensaje de éxito | Coincide | Éxito |
| `envido quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `envido no_quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `envido envido quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `envido envido no_quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `envido real_envido quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `envido real_envido no_quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `envido real_envido falta_envido quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `envido real_envido falta_envido no_quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `real_envido quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `real_envido no_quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `real_envido falta_envido quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `real_envido falta_envido no_quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `falta_envido quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `falta_envido no_quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `truco quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `truco no_quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `truco retruco quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `truco retruco no_quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `truco retruco vale_cuatro quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `truco retruco vale_cuatro no_quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `envido quiero truco quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `envido no_quiero truco retruco no_quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `envido envido real_envido falta_envido no_quiero truco retruco vale_cuatro quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `truco quiero ; envido no_quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `envido quiero ; truco retruco no_quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `truco no_quiero ; envido envido real_envido falta_envido quiero truco quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `truco quiero ; envido no_quiero ; truco retruco vale_cuatro quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `envido quiero ; truco no_quiero ; envido envido quiero truco retruco no_quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `truco quiero ; ; envido no_quiero` | AST generado con ronda vacía y mensaje de éxito | Coincide | Éxito |
| `# Esto es un comentario \n truco quiero` | AST generado y mensaje de éxito (comentario ignorado) | Coincide | Éxito |
| `envido    quiero    ;    truco    no_quiero` | AST generado y mensaje de éxito | Coincide | Éxito |
| `envido quiero ; # otra ronda \n truco no_quiero` | AST generado y mensaje de éxito (comentario ignorado) | Coincide | Éxito |
| `;` | AST de dos rondas vacías y mensaje de éxito | Coincide | Éxito |
| `; ;` | AST de tres rondas vacías y mensaje de éxito | Coincide | Éxito |
| `truco quiero ;` | AST con ronda vacía final y mensaje de éxito | Coincide | Éxito |
| `; truco quiero` | AST con ronda vacía inicial y mensaje de éxito | Coincide | Éxito |
| `truco quiero ; ; envido quiero` | AST con ronda vacía intermedia y mensaje de éxito | Coincide | Éxito |
| `turco quiero` | Error léxico: 'turco' no reconocido | `[línea 1] Error léxico: Carácter o palabra no reconocida 'turco'` | Éxito |
| `truco quierox` | Error léxico: 'x' no reconocido | `[línea 1] Error léxico: Carácter o palabra no reconocida 'x'` | Éxito |
| `truco_quiero` | Error léxico: '_quiero' no reconocido | `[línea 1] Error léxico: Carácter o palabra no reconocida '_quiero'` | Éxito |
| `real_envido envido quiero` | Error sintáctico: se esperaba `falta_envido` o respuesta | `[línea 1] Error sintáctico: Se esperaba falta_envido o respuesta ('quiero'/'no_quiero') (encontrado 'envido')` | Éxito |
| `envido envido envido quiero` | Error sintáctico: se esperaba `real_envido`, `falta_envido` o respuesta | `[línea 1] Error sintáctico: Se esperaba real_envido, falta_envido o respuesta ('quiero'/'no_quiero') (encontrado 'envido')` | Éxito |
| `falta_envido real_envido no_quiero` | Error sintáctico: se esperaba respuesta | `[línea 1] Error sintáctico: Se esperaba 'quiero' o 'no_quiero' (encontrado 'real_envido')` | Éxito |
| `envido real_envido envido quiero` | Error sintáctico: se esperaba `falta_envido` o respuesta | `[línea 1] Error sintáctico: Se esperaba falta_envido o respuesta ('quiero'/'no_quiero') (encontrado 'envido')` | Éxito |
| `retruco quiero` | Error sintáctico: tokens sobrantes | `[línea 1] Error sintáctico: Se esperaba fin de entrada pero hay tokens sobrantes (encontrado 'retruco')` | Éxito |
| `vale_cuatro no_quiero` | Error sintáctico: tokens sobrantes | `[línea 1] Error sintáctico: Se esperaba fin de entrada pero hay tokens sobrantes (encontrado 'vale_cuatro')` | Éxito |
| `truco vale_cuatro quiero` | Error sintáctico: se esperaba `retruco` o respuesta | `[línea 1] Error sintáctico: Se esperaba 'retruco' o respuesta ('quiero'/'no_quiero') (encontrado 'vale_cuatro')` | Éxito |
| `truco retruco vale_cuatro vale_cuatro quiero` | Error sintáctico: se esperaba respuesta | `[línea 1] Error sintáctico: Se esperaba 'quiero' o 'no_quiero' (encontrado 'vale_cuatro')` | Éxito |
| `truco truco quiero` | Error sintáctico: se esperaba `retruco` o respuesta | `[línea 1] Error sintáctico: Se esperaba 'retruco' o respuesta ('quiero'/'no_quiero') (encontrado 'truco')` | Éxito |
| `truco retruco truco` | Error sintáctico: se esperaba `vale_cuatro` o respuesta | `[línea 1] Error sintáctico: Se esperaba 'vale_cuatro' o respuesta ('quiero'/'no_quiero') (encontrado 'truco')` | Éxito |
| `truco` | Error sintáctico: se esperaba `retruco` o respuesta | `[línea 1] Error sintáctico: Se esperaba 'retruco' o respuesta ('quiero'/'no_quiero') (encontrado 'EOF')` | Éxito |
| `envido` | Error sintáctico: se esperaba continuación o respuesta | `[línea 1] Error sintáctico: Se esperaba envido, real_envido, falta_envido o respuesta ('quiero'/'no_quiero') (encontrado 'EOF')` | Éxito |
| `truco retruco` | Error sintáctico: se esperaba `vale_cuatro` o respuesta | `[línea 1] Error sintáctico: Se esperaba 'vale_cuatro' o respuesta ('quiero'/'no_quiero') (encontrado 'EOF')` | Éxito |
| `envido envido` | Error sintáctico: se esperaba `real_envido`, `falta_envido` o respuesta | `[línea 1] Error sintáctico: Se esperaba real_envido, falta_envido o respuesta ('quiero'/'no_quiero') (encontrado 'EOF')` | Éxito |

*Nota 1: El 'Estado' indica 'Éxito' si el analizador se comportó exactamente como se esperaba (aceptando entradas válidas y rechazando e identificando errores en las inválidas).*

*Nota 2: Los errores léxicos para `truco quierox` y `truco_quiero` se reportan como `'x'` y `'_quiero'` respectivamente, ya que el lexer reconoce los tokens válidos (`QUIERO` y `TRUCO`) y deja el resto del lexema como error. En la ejecución de los casos de `retruco quiero` y `vale_cuatro no_quiero` aparecen como "Se esperaba inicio de ronda", debido a que retruco y vale_cuatro no son tokens válidos para iniciar una ronda.
