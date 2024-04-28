# Informe
### Campos:
- IA 
- Simulación 
### Tema: Detección de un mensaje óptimo en el proceso de propagación de la información.

### **Introducción**
En el ámbito de la comunicación y la toma de decisiones, la eficacia de los mensajes es un factor crítico que puede influir significativamente en el éxito de una campaña o en la adopción de una idea.

El objetivo principal de este proyecto es desarrollar un sistema que, a través de la simulación de la propagación de un mensaje, permita evaluar y mejorar la estructura de los mensajes de comunicación. Este enfoque se basa en la premisa de que la simulación puede proporcionar una plataforma para experimentar con diferentes estructuras de mensajes y analizar cómo estas afectan la adopción del mensaje por parte de los agentes en un sistema. Al hacerlo, este proyecto busca contribuir a la comprensión de cómo los mensajes pueden ser diseñados para ser más efectivos en términos de consenso y adopción.

### **Representación de problema**

Representación de una red social a través de un grafo de mundo pequeño, donde los nodos emulan personas y los enlaces la relación entre las mismas.

Las redes sociales suelen exhibir propiedades de mundo pequeño, como alta conectividad, breves distancias medias y alto agrupamiento local. Estas propiedades se reflejan en la estructura de un grafo de mundo pequeño, lo que lo convierte en una representación adecuada de la red social real.

- ``Grafo de mundo pequeño``:  Grafo para el que la mayoría de los nodos no son vecinos entre sí y sin embargo la mayoría de los nodos pueden ser alcanzados desde cualquier nodo origen a través de un número relativamente corto de saltos entre ellos. 

### **Representacionde las persona como agentes:**

#### Estructura Belief-Desire-Intention (BDI):
La estructura BDI permite modelar de forma certera las interacciones sociales y la colaboración en un colectivo de personas.
Permite el intercambio de información, negociación y creación de alianzas basadas en creencias, deseos e intenciones compartidas entre los agentes dando lugar a la simulación de comportamientos sociales complejos. De ahi su selección para simular una red social realista, pues hace posible comprender la dinámica de la colaboración y el conflicto en entornos sociales. Los agentes con esta estructura poseen la capacidad de adaptarse dinámicamente a cambios en su entorno mediante la actualización de sus creencias e intenciones.

#### Cada agente esta compuesto por:
- Un conjunto de ``creencias`` que engloban:
    - Tema: Tema del mensaje que prepresenta.
    - Opinion: Valor numérico que representa, en el caso de los agentes, si tiene una opinión favorable o desfavorable respecto al tema (ej.: positivo, negativo, neutral, representado numéricamnete en el rango discreto de -2 a 2).

- ``Reglas de decisión:`` Cada regla de decisión define de forma única la manera de actuar ante la lleada de un mensaje y la decisión de alterarlo en dependencia del comportamineto que define la regla (de acuerdo, en desacuerdo, intermedio).

    - ``AgreementWithMessageRule ``(Transmitir sin Alterar): Transmite el mensaje sin cambios si hay un alto acuerdo e interés en los temas.
    - ``DisagreementWithMessageRule`` (No Transmitir): No transmite el mensaje si hay un alto desacuerdo en los temas y el interés es alto (evita propagar información con la que   no están de acuerdo los agentes).
    - ``AdjustMessageRule`` (Ajustar Mensaje): Ajusta el mensaje en función del acuerdo moderado en los temas y el interés. Aumenta la intensidad de las opiniones con las que hay acuerdo y disminuye la intensidad de las que generan desacuerdo.
- Red de ``vecinos`` con los que interactúa. 

Al recibir un mensaje, el agente lo analiza mediante la deliberación, utilizando sus creencias, interés en el tema y acuerdo con el mensaje para decidir si transmitirlo tal y como está, alterarlo y transmitirlo o descartarlo. La acción elegida se ejecuta enviando el mensaje modificado (o un nuevo mensaje) a sus vecinos y reportando el resultado; de esta forma es posible modelar agentes con diversos comportamientos y explorar cómo estos influyen en la propagación de información en la red.

### **Modelación de un mensaje:**

#### Cada mensaje esta compuesto por:
- ``Fuerza:`` Valor numérico que indica aproximadamente cuánto baja en DFS un mensajeen el grafo.
- ``Creencias:`` Conjunto de `Belief` que representan los temas abordados en el mensaje y las opiniones asociadas a cada uno (ej.: positivo, negativo, neutral, representadonuméricamnete en el rango discreto de -2 a 2).
- ``Origen y Destino:`` Identificadores que indican el emisor y receptor del mensaje,respectivamente.

### **Modelo de simulación: Determinista**
El comportamiento del sistema está completamente determinado por las condiciones iniciales y las reglas de la simulación. Representa la red social, los agentes, sus interacciones y la propagación de mensajes.
<!-- El proyecto simula un entorno donde los agentes interactúan entre sí intercambiando mensajes. Cada mensaje tiene un tema y una valoración numérica que indica la opinión sobre el tema. Los agentes poseen creencias sobre los temas y reglas de decisión que determinan cómo reaccionan a los mensajes recibidos; siendo la clase `Enviroment` el centro de la simulación. Esta clase representa el entorno en el que se desarrolla la interacción entre los agentes. Su diseño utilizando el patrón *Singleton* garantiza que exista una única instancia del entorno de la simulación en todo el programa, asegurando una ejecución controlada y consistente (algo similar pasa con la clase `Report`). -->

### **Ejecución de la simulación**

La simulación se inicia seleccionando aleatoriamente un conjunto de n agentes para recibir el mensaje de apertura, que puede variar en función del tema que se desee evaluar. A medida que los agentes reciben mensajes, actualizan sus creencias y envían respuestas de acuerdo a sus reglas de decisión. La simulación termina cuando el mensaje ya no tiene suficiente fuerza para seguir propagándose, cuando no existen agentes para transmitirlo o cuando se alcanza un criterio de parada predefinido.

### **Resultados de la simulación**
Interrogantes a las que dan respuesta los resultados de la simulación:
- Grado de propagación del mensaje: A cuantos agentes llega el mensaje.
- Nivel de aceptación del mensaje: Que cantidad de agentes estan de acuerdo con el mensaje.
- Cantidad de emparejamientos excluyentes que se pueden formar con los agentes: Grupos de a dos con intersección vacía.
- Cantidad de comunidades que se pueden formar en la red social: En función de las creencias de los agentes.

### **Componente de procesamiento de lenguage natural:**

- `Libreria google.generativeai`: Permite la creación de aplicaciones de IA generativa basada en modelos de última generación como Gemini, de Google AI.
- ``Uso``: Obtención de un mensaje estructurado a partir de un mensaje en lenguaje natural y viceversa (con un mensaje alterado obtención de un mensaje en lenguaje natural).

### **Componente de conocimiento: `class Cupid`**
Nuestro objetivo es, a través de un problema de optimización lineal, buscar la cantidad máxima de emparejamientos excluyentes que podemos formar con los agentes una vez terminada la simulación siendo esta la función objetivo. Cada agente puede estar en un único emparejamineto y su similitud debe tener un umbral predefinido que podemos variar en dependencia de las interrogantes que tengamos.
Este enfoque nos sirve para definar una métrica más que luego usamos para evaluar los resultados de la simulación a través de un CSP (Contraint-Solution-Problem) resuelto con un algoritmo de programación lineal brindado por la librería `pulp` de Python.

### **Componente de búsqueda: ``Algoritmo Genético``**
Partiendo de la hipótesis de que la combinación de dos mensajes cercanos al "óptimo" genera un mensaje aún mas eficienfe, se optó por emplear el algoritmo genético debido a su capacidad de aprendizaje y adaptación a lo largo del proceso de búsqueda. Mediante la evaluación de la aptitud de los mensajes y la selección de los más adecuados para generar nuevas soluciones, el algoritmo genético evoluciona iterativamente hacia mensajes más eficientes en la propagación y aceptación por parte de los agentes. Fue seleccionado además por brindar la posibilidad de explorar en espacios de soluciones extensos y complejos de manera eficiente, a diferencia de métodos de búsqueda heurísticos como el Hill Climbing, que pueden quedar atrapados en soluciones locales óptimas.

#### Flujo:
- El algoritmo genético comienza generando una población de mensajes de manera aleatoria.
- En cada generación, el algoritmo evalúa la aptitud de cada mensaje en la población basado en el grado de propagación o en el nivel de aceptación del mismo. 
- De forma cìclica selecciona los mejores mensajes como padres y crea una nueva generación de mensajes a través de un proceso que incluye:
    - Cruce: Cada creencia del padre se selecciona con una probabilidad p.
    - Mutación: Cada creencia del padre se modifica con una probabilidad p.

Este proceso se repite durante un número específico de generaciones, permitiendo que los mensajes evolucionen y se ajusten para mejorar su capacidad de ser adoptados por la mayoría de los agentes en el sistema. Al final del proceso, el algoritmo retorna el mejor mensaje encontrado y una lista de los mejores resultados a lo largo de las generaciones. 

![](./Examples/Figure_1.png)
![](./Examples/Figure_2_parents.png)
![](./Examples/Figure_3_mutation_rate.png)
![](./Examples/Figure_4_probability.png)
![](./Examples/Figure_5_num_neighborgs.png)