import random
from genetic import genetic_algorithm
from graph import generate_agents_from_graph


population_size = 5
num_parents = 10
num_generations = 100
mutation_rate = 0.1

# Generar agentes y grafo (puedes usar tu función existente)
num_agents = 100  
num_neighbors = 4  
probability = 0.2
agents, graph = generate_agents_from_graph(num_agents, num_neighbors, probability)

# Seleccionar agentes iniciales
initial_agent_indices = random.sample(range(num_agents), 3) 
initial_agent_indices = [1,2,3]
initial_agents = [agents[i] for i in initial_agent_indices]

# Ejecutar el algoritmo genético
best_message, list = genetic_algorithm(population_size, num_parents, num_generations, mutation_rate, initial_agents)

print(best_message)
print(best_message.result)
print(list)

    