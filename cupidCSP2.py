from constraint import Problem, AllDifferentConstraint
from typing import Dict, List, Tuple
from agent import Agent
from belief import Belief
class Cupid:
    def __init__(self, agent_graph, match_percentage):
        self._agent_graph = agent_graph
        self._match_percentage = match_percentage
        self._agent_beliefs = self._obtener_creencias_agentes()
        self._matches = self._encontrar_emparejamientos()

    def _obtener_creencias_agentes(self):
        """Obtiene dict {nombre : beliefs} para cada nodo del grafo."""

        creencias_agentes = {}
        for nodo in self._agent_graph.nodes:
            agente:Agent = self._agent_graph.nodes[nodo]['agent']  # Obtiene el agente asociado al nodo
            creencias = agente.beliefs  # Obtiene las creencias del agente
            creencias_agentes[nodo] = creencias

        return creencias_agentes

    def _encontrar_emparejamientos(self):
        problem = Problem()
        agents = list(self._agent_graph.nodes)
        problem.addVariables(agents, agents)

        # Add constraints
        problem.addConstraint(AllDifferentConstraint())
        problem.addConstraint(self.match_constraint_func, agents)
        # Solve the problem
        solution = problem.getSolution()

        # Update matches
        for match in solution:
            agent1, agent2 = match
            self._matches[agent1] = agent2
            self._matches[agent2] = agent1

    def match_constraint(self, agent1, agent2):
        # Calculate similarity between agent beliefs
        similarity = self.calcular_similitud(agent1, agent2)
        return similarity >= self._match_percentage

    def calcular_similitud(self,creencias_agente1, creencias_agente2):
        coincidencias = 0
        total_temas = 0
        creencias_agente1 = self._agent_beliefs.get(creencias_agente1)
        creencias_agente2 = self._agent_beliefs.get(creencias_agente2)
        for valor1 in creencias_agente1:
            for valor2 in creencias_agente2:
                if valor1.topic == valor2.topic:
                    if abs(valor1.opinion - valor2.opinion) <= 1:
                        coincidencias += 1
                    total_temas += 1
        similitud = coincidencias / max(len(creencias_agente1), len(creencias_agente2))
        return similitud

