import random
import networkx as nx
from agent import Agent
from belief import Belief
from beliefs_rule import *
from decision_rule import *
from communication_rules import *
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

        confirmation_belief_rule = ConfirmationBiasRule()
        correlation_belief_rule = CorrelationRule()
        denial_belief_rule = DenialRule()

        beliefs_rules = [confirmation_belief_rule, correlation_belief_rule, denial_belief_rule]

        talkative_rule = TalkativeAgentRule()
        shy_rule = ShyAgentRule()
        excited_rule = ExcitedAgentRule()
        gossip_rule = GossipAgentRule()

        communication_rules = [talkative_rule, shy_rule, excited_rule, gossip_rule, gossip_rule, talkative_rule, talkative_rule]

        #Elegimos una regla de comunicacion al azar para este agente
        comm_rule = random.choice(communication_rules)
        # comm_rule = gossip_rule

        
        # Crea el agente con la importancia basada en el grado
        importance = degree / num_agents  # Normaliza la importancia entre 0 y 1
        
        agent = Agent(beliefs, decision_rules, beliefs_rules, comm_rule, [], name=f"Agent_{node}")  # Empty neighbors list for now
        agents.append(agent)
        
        graph.nodes[node]['agent'] = agent  # Associate agent with the node

    # Now, iterate again to populate neighbor agents
    for node in graph.nodes:
        agent = graph.nodes[node]['agent']
        neighbors = [graph.nodes[neighbor]['agent'].name for neighbor in graph.neighbors(node)]
        agent.neighbors = neighbors
        agent.instantiate_neighbor_hypothesis()
        enviroment.register_agent(agent)


    # Ajusta las conexiones del grafo para asegurar que los vecinos tengan creencias similares
    # print_agent_and_neighbors(0, graph)
    adjust_graph(graph)
    # print_agent_and_neighbors(0, graph)
    #draw_graph(graph)
    return agents, graph

def adjust_graph(graph):
    """Ajusta las conexiones del grafo para asegurar que los vecinos tengan creencias similares."""
    for node1, node2 in list(graph.edges):
        agent1 = graph.nodes[node1]['agent']
        agent2 = graph.nodes[node2]['agent']

        # Verificar si los agentes cumplen la condición de similitud
        while not have_similar_beliefs(agent1.beliefs, agent2.beliefs, num_common_topics=2, max_opinion_diff=2):
            # Elegir un agente al azar para recibir una creencia del otro
            if random.random() < 0.5:
                giver, receiver = agent1, agent2
            else:
                giver, receiver = agent2, agent1

            
            # Elegir una creencia al azar del agente que da
            belief_to_transfer = random.choice(giver.beliefs)

            belief_index = next((i for i, b in enumerate(receiver.beliefs) if b.topic == belief_to_transfer.topic), None) 

            if belief_index is not None:
                # Sobrescribir la creencia existente
                receiver.beliefs[belief_index] = belief_to_transfer
            else:
                # Agregar la creencia si no existe
                receiver.beliefs.append(belief_to_transfer)

def have_similar_beliefs(beliefs1, beliefs2, num_common_topics, max_opinion_diff):
    """Verifica si dos conjuntos de creencias tienen suficientes tópicos en común con opiniones similares."""
    common_topics = 0
    for belief1 in beliefs1:
        for belief2 in beliefs2:
            if belief1.topic == belief2.topic and abs(belief1.opinion - belief2.opinion) <= max_opinion_diff:
                common_topics += 1
                if common_topics >= num_common_topics:
                    return True
    return False


def print_agent_and_neighbors(node, graph, distance=2):
    """Imprime las creencias del agente y sus vecinos hasta una distancia dada."""
    agent = graph.nodes[node]['agent']
    print(f"Agente {agent.name}: {agent.beliefs}")
    for dist in range(1, distance + 1):
        neighbors = nx.single_source_shortest_path_length(graph, node, cutoff=dist)
        for neighbor, d in neighbors.items():
            if d == dist:
                neighbor_agent = graph.nodes[neighbor]['agent']
                print(f"  Vecino (distancia {d}): {neighbor_agent.name} - {neighbor_agent.beliefs}")

