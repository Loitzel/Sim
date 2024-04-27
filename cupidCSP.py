from constraint import Problem
import numpy as np
from typing import Dict, List
import pulp
from typing import Dict, List, Tuple

# Asumiendo que las clases personalizadas están definidas en otro archivo
from agent import Agent
from message import Message
from belief import Belief
from enviroment import Environment
from reporter import Reporter
from typing import Dict
class Cupid:
    # _creencias_de_todos_agentes: Dict[Agent, List[Belief]]
    # solucion_emparejamientos: str
    # _matches: Dict[int, int] # New dictionary to track matches

    def __init__(self, grafo_agentes,porcentajeEmparejamiento):
        self._matches = dict() # Initialize the matches dictionary
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

    def _encontrar_emparejamientos(self,porcentaje_emparejamiento):
        
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

        problem = Problem()
        for agent in self._creencias_de_todos_agentes.keys():
            problem.addVariable(agent, range(len(self._creencias_de_todos_agentes.keys())))

        def match_constraint(agent1, agent2):
            if agent1 == agent2:
                return False
            # Verifica si el agente1 ya tiene un emparejamiento
            if agent1 in self._matches and self._matches[agent1] is not None or agent1 in self._matches.values():
                return False
            # Verifica si el agente2 ya tiene un emparejamiento
            if agent2 in self._matches and self._matches[agent2] is not None or agent2 in self._matches.values():
                return False
            # Calcula la similitud y verifica si es mayor o igual al umbral
            similitud = calcular_similitud(self._creencias_de_todos_agentes[agent1], self._creencias_de_todos_agentes[agent2]) 
            if similitud >= porcentaje_emparejamiento:
                print(f"{agent1} - {agent2} similitud = {similitud}")
            return similitud >= porcentaje_emparejamiento

        for agent1 in self._creencias_de_todos_agentes.keys():
            for agent2 in self._creencias_de_todos_agentes.keys():
                if agent1 != agent2:
                    problem.addConstraint(match_constraint, [agent1, agent2])

        
        solution = problem.getSolution()
        for agent1, agent2 in solution.items():
            if agent1 != agent2 and (agent1, agent2) not in self._matches.items():
                self._matches[agent1] = agent2
                self._matches[agent2] = agent1

        return self._matches



