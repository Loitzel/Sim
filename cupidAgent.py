from pulp import *
from message import Message  # Cambiado a Mensaje para reflejar el español
from reporter import Reporter
from agent import Agent
from enviroment import Environment
from belief import Belief
from typing import List

class Cupid():
    """Clase de agente que puede resolver problemas de satisfacción de restricciones (CSP) para emparejamientos."""
    _creencias_de_todos_agentes:{int:[Belief]}  =  {} # type: ignore
    solucion_emparejamientos = ""
    
    def __init__(self,graph,porcentaje_emparejamiento):
        # Atributo adicional para almacenar todas las creencias de los agentes
        self._creencias_de_todos_agentes:{int,[Belief]} = self._obtener_creencias_agentes(graph) # Método obtener_creencias
        self.solucion_emparejamientos = self._encontrar_emparejamientos(porcentaje_emparejamiento)
        
    def _obtener_creencias_agentes(self,grafo):
        """Obtiene dict {nombre : beliefs} para cada nodo del grafo."""

        creencias_agentes = {}
        for nodo in grafo.nodes:
            agente:Agent = grafo.nodes[nodo]['agent']  # Obtiene el agente asociado al nodo
            creencias = agente.beliefs  # Obtiene las creencias del agente
            creencias_agentes[nodo] = creencias

        return creencias_agentes
    
    def _encontrar_emparejamientos(self, porcentaje_emparejamiento):
        """Resuelve el problema de satisfacción de restricciones (CSP) para emparejar agentes."""

        # Extrae las creencias de los agentes
        creencias_agentes :{int:[Belief]} = self._creencias_de_todos_agentes

        def calcular_similitud(creencias_agente1: List[Belief], creencias_agente2: List[Belief]):
            # Calcula la similitud basada en la coincidencia de opiniones de los temas
            coincidencias = sum(1 if abs(valor1.opinion - valor2.opinion) <= 1 else 0 # Ajuste aquí para usar la diferencia absoluta
                                for valor1, valor2 in zip(creencias_agente1, creencias_agente2) 
                                if valor1.topic == valor2.topic)
            similitud = coincidencias / max(len(creencias_agente1),len(creencias_agente2))
            return similitud

        # Crea un modelo de programación lineal entera (MILP) con `pulp`
        pulp.LpSolverDefault.msg = False
        
        prob = LpProblem("ProblemaEmparejamiento",LpMaximize)

        variables_emparejamiento = {}
        # Variables binarias para representar si un agente está emparejado con otro
        for i, agente1 in enumerate(creencias_agentes):
            for j, agente2 in enumerate(creencias_agentes):
                if i < j:
                    variables_emparejamiento[(i,j)] = LpVariable(name=f"Agente_{i}-Agente_{j}", cat=LpInteger, lowBound=0,upBound=1)

        # Función objetivo: maximizar el número de parejas
        prob += lpSum(variables_emparejamiento[(agente1, agente2)] for agente1, agente2 in variables_emparejamiento)
        
        # Restricciones: cada agente solo puede estar emparejado con un máximo de un agente
        for agente,creencias in creencias_agentes.items():
            prob += lpSum(variables_emparejamiento[(agente1, agente2)] for agente1, agente2 in variables_emparejamiento if agente1 == agente or agente2 == agente) <= 1
            
        # Restricciones: solo se emparejan agentes con similitud superior al porcentaje_emparejamiento%
        for agente1, agente2 in variables_emparejamiento:
            similitud = calcular_similitud(creencias_agentes[agente1], creencias_agentes[agente2])
            # Ajusta la restricción para que solo permita emparejamientos con similitud superior al umbral
            #print(f"({agente1}, {agente2}) varValue = {variables_emparejamiento[(agente1, agente2)].varValue}")
            if similitud >= porcentaje_emparejamiento:
                prob += lpSum(variables_emparejamiento[(agente1, agente2)]) <= 1

        
        # Resuelve el problema de programación lineal entera
        prob.solve()
       
        # Obtiene la solución
        if LpStatus[prob.status] == "Optimal":
            # Obtiene los pares emparejados
            pares_emparejados = [(agente1, agente2) for agente1, agente2 in variables_emparejamiento if variables_emparejamiento[(agente1, agente2)].varValue == 1]
        
            # Convierte los pares emparejados a una cadena de representación
            cadena_emparejamientos = "\n".join([f"Agente {agente1} - Agente {agente2}" for agente1, agente2 in pares_emparejados])
            return f"Emparejamientos: {cadena_emparejamientos}"
        else:
            return "No se encontró una solución óptima para el problema de emparejamiento."