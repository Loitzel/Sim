import pulp
from typing import Dict, List, Tuple

# Asumiendo que las clases personalizadas están definidas en otro archivo
from agent import Agent
from message import Message
from belief import Belief
from enviroment import Environment
from reporter import Reporter
class Cupid:
    _creencias_de_todos_agentes: Dict[int, List[Belief]]
    solucion_emparejamientos: str

    def __init__(self, grafo_agentes,porcentajeEmparejamiento):
        self._creencias_de_todos_agentes: Dict[int, List[Belief]] = self._obtener_creencias_agentes(grafo_agentes)
        self.solucion_emparejamientos = self._encontrar_emparejamientos(porcentajeEmparejamiento)

    def _obtener_creencias_agentes(self,grafo):
        """Obtiene dict {nombre : beliefs} para cada nodo del grafo."""

        creencias_agentes = {}
        for nodo in grafo.nodes:
            agente:Agent = grafo.nodes[nodo]['agent']  # Obtiene el agente asociado al nodo
            creencias = agente.beliefs  # Obtiene las creencias del agente
            creencias_agentes[nodo] = creencias

        return creencias_agentes

    def _encontrar_emparejamientos(self,porcentaje_emparejamiento) -> str:
        
        def calcular_similitud(creencias_agente1, creencias_agente2):
            coincidencias = 0
            total_temas = 0
            for valor1 in creencias_agente1:
                for valor2 in creencias_agente2:
                    if valor1.topic == valor2.topic:
                        if abs(valor1.opinion - valor2.opinion) <= 1:
                            coincidencias += 1
                        total_temas += 1
            similitud = coincidencias / max(len(creencias_agente1), len(creencias_agente2))
            return similitud

        # Crear el problema de programación lineal entera
        problema = pulp.LpProblem("Emparejamiento", pulp.LpMaximize)
        pulp.LpSolverDefault.msg = False

        # Variables de decisión
        emparejamientos = pulp.LpVariable.dicts("Emparejamiento",
                                               ((agente1, agente2) 
                                                for agente1 in self._creencias_de_todos_agentes 
                                                for agente2 in self._creencias_de_todos_agentes 
                                                #if agente1 < agente2
                                                ),
                                               cat='Binary')
        
        # Introducir una variable de decisión adicional para la similitud
        similitud = pulp.LpVariable.dicts("Similitud",
                                          ((agente1, agente2)
                                           for agente1 in self._creencias_de_todos_agentes
                                           for agente2 in self._creencias_de_todos_agentes
                                           if agente1 < agente2),
                                          cat='Binary')
        # Función objetivo
        problema += pulp.lpSum(emparejamientos[agente1, agente2]
                           for agente1 in self._creencias_de_todos_agentes 
                           for agente2 in self._creencias_de_todos_agentes
                           if agente1 != agente2
                           )
        
        # Restricciones
        
        # Unicidad de Emparejamiento
        for agente in self._creencias_de_todos_agentes:
            restriccion = pulp.lpSum(emparejamientos[agente, otro_agente] + emparejamientos[otro_agente, agente]
                             for otro_agente in self._creencias_de_todos_agentes
                             if otro_agente != agente) <= 1
            problema += restriccion    
       
       #Similitud
        for agente1 in self._creencias_de_todos_agentes:
            for agente2 in self._creencias_de_todos_agentes:
                if agente1 != agente2:
                    sim = calcular_similitud(self._creencias_de_todos_agentes[agente1],self._creencias_de_todos_agentes[agente2])
                    # y luego establecer una restricción basada en esta similitud y la variable de decisión similitud
                    # Por ejemplo, si la similitud es mayor que un umbral, entonces similitud[agente1, agente2] = 1
                    # Esto es solo un esquema y necesitarás ajustarlo según tu lógica de similitud
                    if sim < porcentaje_emparejamiento:
                        problema+= emparejamientos[agente1, agente2] == 0

        # Resolver el problema
        problema.solve()

        # Representación de la solución
        if pulp.LpStatus[problema.status] == 'Optimal':
            print("Optimo")
            # Si se encuentra una solución óptima, devolverla como antes
            parejas_logradas = sum(1 for valor in emparejamientos.values() if valor.varValue == 1)
            solucion = [f"Agente_{agente1} - Agente_{agente2} {calcular_similitud(self._creencias_de_todos_agentes[agente1], self._creencias_de_todos_agentes[agente2])}" for (agente1, agente2), valor in emparejamientos.items() if valor.varValue == 1]
            print("\n".join(solucion))
            return parejas_logradas
