from message import Message
from enviroment import Environment
from graph import generate_agents_from_graph
from cupidAgent import Cupid
from save import dividir_y_guardar_textos
from metaheuristic import algoritmo_genetico, Simulation
from belief import Belief
num_agents = 20  # Número de agentes
num_neighbors = 4  # Número de vecinos por agente
probability = 0.2  # Probabilidad de reconexión en el grafo

agents, graph = generate_agents_from_graph(num_agents, num_neighbors, probability)
environment = Environment.get_instance()  # Obtener la instancia del entorno (singleton)


for a in agents:
    environment.register_agent(a)
    

  
# initial_agent_indices = random.sample(range(num_agents), 3)  # Selecciona 3 agentes al azar
initial_agent_indices = [1,2,3] 
initial_agents = [agents[i] for i in initial_agent_indices]
messages = dividir_y_guardar_textos("prompt.txt")

sim_results = []
for msg in messages:
    initial_message = Message(strength=5, beliefs=msg, source=None, destination=None) 

    sim_result = Simulation(msg)
    sim_result.resultado = environment.run_simulation(initial_message, initial_agents)
    sim_results.append(sim_result)
    print("-----------------------------------------------------C")
algoritmo_genetico(sim_results,10,5,10,0.25) 
cupid = Cupid(graph)
print(cupid.solucion_emparejamientos)