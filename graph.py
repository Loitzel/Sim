import random
import networkx as nx
from agent import Agent
from belief import Belief
from decision_rule import *
from topics import Topics
from enviroment import Environment
import matplotlib.pyplot as plt

def draw_graph(graph, node_color_property='degree'):
    # Prepara los datos para el gráfico
    node_colors = []
    for node in graph.nodes:
        if node_color_property == 'importance':
            # Asume que el grado ya está normalizado y almacenado como 'importance'
            node_colors.append(graph.nodes[node]['agent'].importance)
        elif node_color_property == 'degree':
            node_colors.append(graph.degree[node])
        else:
            raise ValueError(f"Invalid node_color_property: {node_color_property}")
    
    # Dibuja el grafo
    plt.figure(figsize=(10, 10))
    nx.draw(graph, with_labels=True, node_color=node_colors, cmap=plt.cm.Blues)
    plt.title("Grafo de Agentes")
    plt.show()

# Ejemplo de uso


def generate_agents_from_graph(num_agents, num_neighbors, probability):
    # Create a small-world graph
    graph = nx.watts_strogatz_graph(n=num_agents, k=num_neighbors, p=probability)

    # Generate agents and assign neighbors
    agents = []

    enviroment = Environment.get_instance()

    for node in graph.nodes:
        all_topics = list(Topics)
        num_beliefs = random.randint(1, 10)
        selected_topics = random.sample(all_topics, num_beliefs)
        beliefs = [Belief(topic.value, random.randint(-2, 2)) for topic in selected_topics]
        
        # Nueva variable para almacenar el grado del agente (número de vecinos)
        degree = graph.degree[node]

        
        agree_rule = AgreementWithMessageRule()
        disagree_rule = DisagreementWithMessageRule()
        adjust_rule = AdjustMessageRule()
        random_rule = RandomDecisionRule()
        decision_rules = [agree_rule, adjust_rule, disagree_rule]
        
        # Crea el agente con la importancia basada en el grado
        importance = degree / num_agents  # Normaliza la importancia entre 0 y 1
        
        agent = Agent(beliefs, decision_rules, [], name=f"Agent_{node}")  # Empty neighbors list for now
        enviroment.register_agent(agent)
        agents.append(agent)
        
        graph.nodes[node]['agent'] = agent  # Associate agent with the node

    # Now, iterate again to populate neighbor agents
    for node in graph.nodes:
        agent = graph.nodes[node]['agent']
        neighbors = [graph.nodes[neighbor]['agent'].name for neighbor in graph.neighbors(node)]
        agent.neighbors = neighbors
    
    #draw_graph(graph)
    return agents, graph