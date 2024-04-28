from constraint import Problem, AllDifferentConstraint
from typing import Dict, List, Tuple
from agent import Agent
from belief import Belief
class Cupid:
    def __init__(self, agent_graph, match_percentage):
        self._agent_graph = agent_graph
        self._match_percentage = match_percentage
        self._agent_beliefs = self._obtener_creencias_agentes()
        self.solution = None
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
        for i, agent_1 in enumerate(agents[:-1]):
            for agent_2 in agents[i + 1:]:
                problem.addVariable((agent_1, agent_2), [0, 1])

        # Add constraints
        self.addContraints(problem, agents)
        # for agent_1 in agents:
        #     for agent_2 in agents:
        #         problem.addConstraint(self.match_constraint, [agent_1, agent_2])
        
        # Solve the problem
        self.solution = problem.getSolution()

        # Update matches
        if self.solution is not None:
            for match in self.solution:
                agent1, agent2 = match
                self._matches[agent1] = agent2
                self._matches[agent2] = agent1
        else:
            print('No existe solucion')
            
    def addContraints(self, problem: Problem, agents):
        for agent_1 in agents:
            for agent_2 in agents:
                if agent_1 != agent_2:
                    # Define a custom constraint function that takes agent1, agent2, and potentially another variable (e.g., preferred_agent
                    def custom_constraint_percentage(var):
                        a1, a2 = var 
                        # Calculate similarity between agent beliefs
                        return self.calcular_similitud(a1, a2) >= self._match_percentage
                    
                    # Add the constraint with the custom function
                    problem.addConstraint(custom_constraint_percentage, [agent_1, agent_2])  # Pass agent_1 as the "preferred_agent"
            
            # def custom_constraint_singularity(var):
            #     a1, a2 = var
            #     if preferred_agent is not None and self.solution is not None:
            #         for current_agent in agents: 
            #             if preferred_agent == self.solution.get(current_agent):
            #                 taked += 1
            #     return taked <= 1        
            
            # problem.addConstraint(custom_constraint_singularity, [agent_1])  # Pass agent_1 as the "preferred_agent"


            
    # def addContraints(self, problem: Problem, agents):
    #     for agent_1 in agents:
    #         for agent_2 in agents:
    #             if agent_1 != agent_2:
    #                 problem.addConstraint(self.match_constraint, [agent_1, agent_2])

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

