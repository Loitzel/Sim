from message import Message
from enviroment import Environment
from graph import generate_agents_from_graph
from save import dividir_y_guardar_texto
from metaheuristic import algoritmo_genetico, Simulation
from genetic import genetic_algorithm
from belief import Belief
from community_detector import get_highly_endorsed_messages 
from API import MessageGenerator
num_agents = 20  # Número de agentes
num_neighbors = 4  # Número de vecinos por agente
probability = 0.2  # Probabilidad de reconexión en el grafo

agents, graph = generate_agents_from_graph(num_agents, num_neighbors, probability)

list_agents = [agent.to_dict() for agent in agents]
graph_dict = {}
for node in graph.nodes:
    agent_name = graph.nodes[node]['agent'].name
    neighbors = [graph.nodes[neighbor]['agent'].name for neighbor in graph.neighbors(node)]
    graph_dict[agent_name] = neighbors

environment = Environment.get_instance()  # Obtener la instancia del entorno (singleton)


for a in agents:
    environment.register_agent(a)
    
# initial_agent_indices = random.sample(range(num_agents), 3)  # Selecciona 3 agentes al azar
initial_agent_indices = [1,2,3] 
initial_agents = [agents[i] for i in initial_agent_indices]
text, msg = dividir_y_guardar_texto("prompt.txt")



initial_message = Message(strength=5, beliefs=msg, source=None, destination=None) 
sim_result = Simulation(msg)
sim_result.resultado = environment.run_simulation(initial_message, initial_agents)
best, evol_list = genetic_algorithm(population_size=30,graph=graph,num_parents=5,num_generations=80,mutation_rate=0.4,initial_agents=[agents[1],agents[2],agents[3]])
msg_gen = MessageGenerator()

print(msg)
print(text)
print("-------------------------------------------------")
print(best)
#print(msg_gen.generate_message_given_topics(best.beliefs+msg))
print(msg_gen.generate_message(text,msg,best.beliefs))

