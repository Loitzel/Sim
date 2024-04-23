from message import Message
from enviroment import Environment
from graph import generate_agents_from_graph
from cupidAgent import Cupid
from save import dividir_y_guardar_textos
from metaheuristic import algoritmo_genetico, Simulation
from belief import Belief
import json,joblib

num_agents = 20  # Número de agentes
num_neighbors = 4  # Número de vecinos por agente
probability = 0.2  # Probabilidad de reconexión en el grafo

agents, graph = generate_agents_from_graph(num_agents, num_neighbors, probability)
# data_to_save = {'agents': agents, 'graph': graph}
# joblib.dump(data_to_save, 'data.joblib')

list_agents = [agent.to_dict() for agent in agents]
graph_dict = {}
for node in graph.nodes:
    agent_name = graph.nodes[node]['agent'].name
    neighbors = [graph.nodes[neighbor]['agent'].name for neighbor in graph.neighbors(node)]
    graph_dict[agent_name] = neighbors

datos = {
    "agents": list_agents,
    "graph": graph_dict
}

datos_json = json.dumps(datos, indent=2)
with open('datos.json', 'w') as archivo:
    archivo.write(datos_json)

# data_loaded = joblib.load('data.joblib')
# agents = data_loaded['agents']
# graph = data_loaded['graph']

environment = Environment.get_instance()  # Obtener la instancia del entorno (singleton)


for a in agents:
    environment.register_agent(a)
    
# initial_agent_indices = random.sample(range(num_agents), 3)  # Selecciona 3 agentes al azar
initial_agent_indices = [1,2,3] 
initial_agents = [agents[i] for i in initial_agent_indices]
result_msgs = dividir_y_guardar_textos("prompt.txt")

sim_results = []
for text, msg in result_msgs:
    initial_message = Message(strength=5, beliefs=msg, source=None, destination=None) 

    sim_result = Simulation(msg)
    sim_result.resultado = environment.run_simulation(initial_message, initial_agents)
    sim_results.append(sim_result)
    print("-----------------------------------------------------C")
#algoritmo_genetico(sim_results,10,5,10,0.25) 
cupid = Cupid(graph,0.2)
print(cupid.solucion_emparejamientos)