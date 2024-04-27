import numpy as np
from random import choice, sample
from belief import Belief
from topics import Topics
from API import MessageGenerator
class Simulation():
    beliefs = []
    resultado = 0
    def __init__(self,beliefs:[Belief]):
        self.beliefs = beliefs
    
    def set_resultado(self, resultado):
        self.resultado = resultado


def seleccionar_padres(poblacion: [Simulation], K: int) -> [Simulation]:
    """Selecciona los K mejores resultados de la población como padres."""
    sorted_population = sorted(poblacion, key=lambda x: x.resultado, reverse=True)
    return sorted_population[:K]

def cruce(padre1:Simulation, padre2:Simulation):
    """Realiza el cruce aleatorio por tópico entre dos padres y genera una nueva solución."""
    beliefs1 = padre1.beliefs
    beliefs2 = padre2.beliefs

    # Crear una nueva lista de tópicos
    nuevos_topicos = []
    
    topicos = min(len(beliefs1),len(beliefs2))

    # Recorrer los tópicos de ambos padres
    for i in range(topicos):
        # Seleccionar aleatoriamente de cuál padre se toma el valor
        random = np.random.random()
        if random < 0.50:
            nuevos_topicos.append(beliefs1[i])
        else:
            nuevos_topicos.append(beliefs2[i])
 
    result = Simulation(nuevos_topicos)
    result.set_resultado((padre1.resultado + padre2.resultado) /2)
    return result

def mutacion(solucion:Simulation):    
    result = []
    for belief in solucion.beliefs:
        if np.random.random() > 0.4:
            result.append(Belief(Topics.select_random_topics(1),np.random.randint(-2,2)))
        else:
            result.append(belief)
    
    mutacion_result = Simulation(result)
    mutacion_result.set_resultado(solucion.resultado)
    return mutacion_result

def algoritmo_genetico(list_messages_as_topics, no_padres, cant_escoger, no_iter_max, tasa_mutacion):
    # 1. Simulación inicial
    poblacion_inicial = []
    mejores_soluciones = []
    for i, message in enumerate(list_messages_as_topics):
        beliefs = message.beliefs  
        resultado = message.resultado
        sim_init = Simulation(beliefs)
        sim_init.set_resultado(resultado)
        poblacion_inicial.append(sim_init)

    poblacion_actual = poblacion_inicial
    # 2. Bucle principal
    for iteracion in range(no_iter_max):
        # 2.1 Seleccion de padres
        padres = seleccionar_padres(poblacion_actual, no_padres)

        # 2.2 Cruce
        hijos = []
        for padre1, padre2 in zip(padres[::2], padres[1::2]):
            hijo = cruce(padre1, padre2)
            
            hijos.append(hijo)

        # 2.3 Mutación
        for hijo in hijos:
            if np.random.random() < tasa_mutacion:
                mutacion(hijo)

        # 2.4 Nuevas soluciones
        nueva_poblacion = []
        for solucion in poblacion_actual + hijos:
            nueva_poblacion.append(solucion)

        # 2.5 Selección de la mejor solución
        mejor_solucion = max(nueva_poblacion, key=lambda x: x.resultado)

        # 2.6 Actualización de la población
        poblacion_actual = sorted(nueva_poblacion, key=lambda x: x.resultado, reverse=True)[:cant_escoger]

        # 2.7 Guardar la mejor solución de cada iteración
        mejores_soluciones.append(mejor_solucion)

    # 3. Selección final
    mejor_solucion_final = max(mejores_soluciones, key=lambda x: x.resultado)
    # Impresión de la mejor solución
    msg_gen = MessageGenerator()
    
    send_to_API = []
    for elem in mejor_solucion_final.beliefs:
        send_to_API.append((elem.topic,elem.opinion))
    best_sol = msg_gen.generate_message_given_topics(send_to_API)
    print("Mejor mensaje: " +best_sol)

    return mejor_solucion_final


