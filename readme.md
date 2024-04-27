# Simulación de Agentes con Intercambio de Mensajes

Este proyecto simula un sistema de agentes que interactúan entre sí mediante el intercambio de mensajes. Cada agente tiene creencias sobre diferentes temas y reglas de decisión que determinan cómo procesan los mensajes y si los transmiten a sus vecinos.

## Estructura del Proyecto

El proyecto está organizado en los siguientes archivos:

* **`topics.py`:** Define una enumeración (`Enum`) que representa los diferentes temas sobre los que los agentes pueden tener creencias.
* **`belief.py`:** Define la clase `Belief` que representa una creencia de un agente sobre un tema específico.
* **`message.py`:** Define la clase `Message` que representa un mensaje que se transmite entre agentes.
* **`agent.py`:** Define la clase `Agent` que representa un agente con sus creencias, reglas de decisión y vecinos.
* **`decision_rule.py`:** Define varias reglas de decisión que los agentes pueden usar para determinar cómo procesar los mensajes.
* **`enviroment.py`:** Define la clase `Environment` (singleton) que representa el entorno de la simulación y gestiona la interacción entre agentes.
* **`graph.py`:** Contiene funciones para generar un grafo de conexiones entre agentes y crear agentes a partir de este grafo.
* **`reporter.py`:** Define la clase `Reporter` (singleton) que se encarga de registrar información sobre la simulación en un archivo.

## Cómo Ejecutar la Simulación

**Requisitos:**

* Python 3.x
* Librería `networkx`: Instalar con `pip install networkx`

**Pasos:**

1. **Abrir el Notebook:** Abre el notebook Jupyter proporcionado.
2. **Ejecutar las Celdas:** Ejecuta las celdas del notebook en orden. Las celdas ya están configuradas para:
    * Importar las clases necesarias.
    * Definir los parámetros de la simulación.
    * Generar agentes y el grafo de conexiones.
    * Crear un mensaje inicial.
    * Seleccionar agentes iniciales.
    * Ejecutar la simulación.
3. **Analizar Resultados:** El archivo `simulation_report.txt` contendrá información sobre cómo se propagaron las creencias y cómo cambiaron las opiniones de los agentes.
