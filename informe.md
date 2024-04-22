# ``Informe del proyecto de IA con Simulación: Propagación de mensajes entre agentes``

### **Introducción**

El proyecto de IA que se presenta simula la propagación de mensajes entre agentes que poseen creencias y reglas de decisión. Cada mensaje está compuesto por un tema y una valoración numérica entre -2 y 2, que indica si se habla bien o mal del tema en cuestión. El objetivo del proyecto es analizar cómo las creencias y las reglas de decisión de los agentes influyen en la propagación de los mensajes.

### **Representación de problema**
Representación de una red social, donde los nodos son personas y los enlaces son la relación entre ellos.
- ``Grafo de mundo pequeño``:  Grafo para el que la mayoría de los nodos no son vecinos entre sí y sin embargo la mayoría de los nodos pueden ser alcanzados desde cualquier nodo origen a través de un número relativamente corto de saltos entre ellos.

### **Modelo de simulación**

El proyecto simula un entorno donde los agentes interactúan entre sí intercambiando mensajes. Cada mensaje tiene un tema y una valoración numérica que indica la opinión sobre el tema. Los agentes poseen creencias sobre los temas y reglas de decisión que determinan cómo reaccionan a los mensajes recibidos; siendo la clase `Enviroment` el centro de la simulación. Esta clase representa el entorno en el que se desarrolla la interacción entre los agentes. Su diseño utilizando el patrón Singleton garantiza que exista una única instancia de la simulación en todo el programa, asegurando una ejecución controlada y consistente (algo similar pasa con la clase `Report`). 

### **Representacionde los agentes: `class Agent`**

La clase Agent define la estructura y el comportamiento de los agentes individuales en la simulación. Cada agente posee un conjunto de creencias, reglas de decisión y una red de vecinos con los que interactúa. Al recibir un mensaje, el agente lo analiza mediante la deliberación, utilizando sus creencias, interés en el tema y acuerdo con el mensaje para decidir si transmitirlo, alterarlo o descartarlo. La acción elegida se ejecuta enviando el mensaje modificado (o un nuevo mensaje) a sus vecinos y reportando el resultado. Esta clase permite modelar agentes con diversos comportamientos y explorar cómo estos influyen en la propagación de información en la red.

### **Representacion de un mensaje: `class Message`**

- ``Composición del Mensaje:``

    -`` Fuerza:`` Valor numérico que indica aproximadamente cuánto baja en DFS un mensaje en el grafo.
    - ``Creencias:`` Lista de objetos `Belief` que representan los temas abordados en el mensaje y las opiniones asociadas a cada uno (ej.: positivo, negativo, neutral representado numéricamnete en el rango discreto de -2 a 2).
    - ``Origen y Destino:`` Identificadores que indican el emisor y receptor del mensaje, respectivamente.

- ``Funcionalidades:``
Permite modificar el valor numérico que representa la importancia del mensaje y proporciona métodos para cambiar la opinión sobre un tema específico o fortalecer/debilitar la intensidad de dicha opinión. Habilita la generación de una réplica exacta del mensaje original para preservar información o crear variaciones.

### **Modificacion de un mensaje: `class DecisionRule`** 
- ``Reglas de decision:``

    - ``AgreementWithMessageRule ``(Transmitir sin Alterar): Transmite el mensaje sin cambios si hay un alto acuerdo e interés en los temas.
    - ``DisagreementWithMessageRule`` (No Transmitir): No transmite el mensaje si hay un alto desacuerdo en los temas y el interés es alto (evita propagar información con la que   no están de acuerdo los agentes).
    - ``AdjustMessageRule`` (Ajustar Mensaje): Ajusta el mensaje en función del acuerdo moderado en los temas y el interés. Aumenta la intensidad de las opiniones con las que hay acuerdo y disminuye la intensidad de las que generan desacuerdo.

### **Ejecución de la simulación**

La simulación comienza con un mensaje inicial que se propaga entre los agentes. A medida que los agentes reciben mensajes, actualizan sus creencias y envían respuestas de acuerdo a sus reglas de decisión. La simulación termina cuando el mensaje ya no tiene suficiente fuerza para seguir propagándose o cuando se alcanza un criterio de parada predefinido.

### **Resultados de la simulación**

- Cantidad de agentes que recibieron el mensaje.
- Opinión final promedio sobre el tema.
- Velocidad de propagación del mensaje


### **Componente de procesamiento de lenguage natural:**

- `Libreria google.generativeai`: Permite la creación de aplicaciones de IA generativa basada en modelos de última generación como Gemini, de Google AI.
- ``Uso``: Obtención de un mensaje estructurado a partir de un mensaje en lenguaje natural y viceversa (con un mensaje alterado obtención de un mensaje en lenguaje natural).

### **Componente de búsqueda: `class Cupid`**

El objetivo del agente es encontrar parejas compatibles entre los demás agentes presentes en la simulación basado en la creencias de los mismos. Para ello se utiliza un algoritmo de programación lineal entera para resolver un problema de satisfacción de restricciones.