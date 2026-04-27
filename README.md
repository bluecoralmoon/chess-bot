# Flujo de trabajo

## Asignación de tareas

Para cada tarea se creará un _issue_ con una lista de subtareas y quienquiera podrá asignarse el _issue_. Para empezar a trabajar en un _issue_ deben crear una _branch_ basada en _main_, y para las subtareas podrán crear _branches_ basadas en la _branch_ principal de esa tarea. Cuando terminen de trabajar en una tarea, deberán crear una _pull request_ para revisar el trabajo hecho antes de hacerle _merge_ con la _branch_ principal.

## Convención de commits

Los commits deberán tener el siguiente formato para mayor claridad:

```
<tipo>/<descripción corta>
```

* `feat`: → nueva funcionalidad (feature)
* `fix`: → corrección de errores
* `chore`: → tareas de mantenimiento (config, deps)
* `refactor`: → reestructuración de código sin cambiar comportamiento
* `docs`: → cambios en documentación
* `hotfix`: → correcciones urgentes en producción

# Idea general

La creación de un bot de ajedrez se divide en las siguientes grandes áreas:

1. Representación del tablero: crear una representación del tablero libre de bugs y que siga las reglas del ajedrez.
    - Board: se necesita una clase que represente el tablero con todas las reglas (esto incluye mantener constancia de repetición de movimientos para el empate por 3 repeticiones, la cantidad de movimientos para el empate por 50 turnos sin captura, el último peón que se movió doble para el _en passant_, los derecho de enroque, el turno, etc.)
    - Bitboards: las piezas se representan como una colección de bits, en particular, un int de 64 bits, donde el bit menos significativo es la esquina inferior derecha del tablero y el más significativo es la esquina superior izquierda. Un 1 implica la presencia de una pieza en esa posición y un 0, lo contrario.
    - make_move(move)/unmake_move(move): una función que haga y deshaga movimientos. Se debe mantener un stack de todos los movimientos hechos en Board para poder deshacerlos uno a uno.
    - Una función que determine si el rey de cierto color está en jaque (para revisar legalidad).
2. Generación de movimientos: es necesaria para que el bot elija un movimiento y pueda analizar movimientos futuros.
    - Generar todos los movimientos pseudolegales a partir de una posición.
    - Generar todos los movimientos legales a partir de una posición.
    - Funciones para obtener los movimientos de piezas específicas en tiempo constante.
3. Evaluación: Debemos ser capaces de evaluar la ventaja o desventaja de cierta posición. Esto se divide en una gran cantidad de subtareas, ya que la ventaja de una posición se determina a partir de muchas variables.
4. Búsqueda: Se hace con un tipo de _backtracking_ conocido como _negamax search_ o _alpha beta pruning_ que consiste en recorrer todas las posibles jugadas hasta cierta profundidad y evaluarlas, podando las ramas que son peores que las que ya visitamos. Lo importante aquí es optimizar lo más posible, ya que para profundidades altas este algoritmo llega a ser O(n^n). Hay varias maneras de hacer esto.

### Extra

5. UCI + Manejo de tiempo: UCI es el formato estándar para que un bot de ajedrez se comunique con otras interfaces. Esto nos serviría para enfrentarlo a otros bots y medir su Elo, entre otras cosas.
6. Testing científico: Simular partidas contra Stockfish u otros bots para determinar si un cambio realmente mejora el Elo del bot. Incluye otras cosas, como el análisis estadístico de bases de datos de partidas y el uso de Machine Learning para el aprendizaje y testeo del bot.
