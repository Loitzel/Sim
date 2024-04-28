import random
import os
from matplotlib import pyplot as plt
from cupidNew import get_result
from genetic import genetic_algorithm, optimize_graph
from graph import generate_agents_from_graph
from genetic import get_agreement_agents_count as agree_function
from genetic import get_notified_agents_count as notified_function
import json

output_folder = 'output_images_cupid_function2'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Contador global para los nombres de archivo
image_counter = 0

def run_genetic(population_size = 30, num_parents = 5, num_generations = 100, mutation_rate = 0.5, num_agents = 300, num_neighbors = 4, probability = 0.2, objective_function = notified_function, num_constant_bests = 1):
    global image_counter
    agents, graph = generate_agents_from_graph(num_agents, num_neighbors, probability)

    # Seleccionar agentes iniciales
    initial_agent_indices = random.sample(range(num_agents), 3) 
    initial_agent_indices = [1,2,3]
    initial_agents = [agents[i] for i in initial_agent_indices]

    # Ejecutar el algoritmo genético
    best_message, results_list = genetic_algorithm(population_size, graph, num_parents, num_generations, mutation_rate, initial_agents, objective_function, num_constant_bests)

    # Ejecutar el algoritmo genético
    best_message_r, results_list_r = genetic_algorithm(population_size, graph, num_parents, num_generations, mutation_rate, initial_agents, objective_function, num_constant_bests, randomSearch = True)

    # Graficar los resultados combinados
    plt.plot(results_list, label='Algoritmo Genético', color='blue')
    plt.plot(results_list_r, label='Random', color='red')
    plt.xlabel("Generación")
    plt.ylabel("Mejor Resultado")
    # Agregar texto con los valores de los parámetros
    plt.text(0.05, 0.95, f"Tamaño de Población: {population_size}\n"
                        f"Número de Padres: {num_parents}\n"
                        f"Número de Generaciones: {num_generations}\n"
                        f"Tasa de Mutación: {mutation_rate}\n"
                        f"\n"
                        f"Cantidad de Agentes: {num_agents}\n"
                        f"Número de Vecinos: {num_neighbors}\n"
                        f"Probabilidad: {probability}", 
            horizontalalignment='left', verticalalignment='top', transform=plt.gca().transAxes, fontsize=8)
    plt.title("Comparación entre Algoritmo Genético y Random")
    plt.legend()
    
    # Guardar la figura en lugar de mostrarla
    image_path = os.path.join(output_folder, f'image_{image_counter}.png')
    plt.savefig(image_path)
    plt.close() # Cerrar la figura para liberar memoria
    image_counter += 1

    #plt.show()
    
    # Calcular y devolver los valores máximos
    max_value_genetic = max(results_list)
    max_value_random = max(results_list_r)
    return max_value_genetic, max_value_random

def run_adapt(number_of_iterations = 5, population_size = 30, num_parents = 5, num_generations = 100, mutation_rate = 0.5, num_agents = 300, num_neighbors = 4, probability = 0.2, objective_function = notified_function, num_constant_bests = 1):

    agents, graph = generate_agents_from_graph(num_agents, num_neighbors, probability)

    # Seleccionar agentes iniciales
    initial_agent_indices = random.sample(range(num_agents), 3) 
    initial_agent_indices = [1,2,3]
    initial_agents = [agents[i] for i in initial_agent_indices]

    # Ejecutar el algoritmo genético
    best_message, results_list = optimize_graph(number_of_iterations, population_size, graph, num_parents, num_generations, mutation_rate, initial_agents, objective_function, num_constant_bests)

    # Graficar los resultados combinados
    plt.plot(results_list, label='Optimizacion del Grafo', color='blue')
    plt.xlabel("Iteración")
    plt.ylabel("Mejor Resultado")
    # Agregar texto con los valores de los parámetros
    plt.text(0.05, 0.95, f"Tamaño de Población: {population_size}\n"
                        f"Número de Padres: {num_parents}\n"
                        f"Número de Generaciones: {num_generations}\n"
                        f"Tasa de Mutación: {mutation_rate}\n"
                        f"\n"
                        f"Cantidad de Agentes: {num_agents}\n"
                        f"Número de Vecinos: {num_neighbors}\n"
                        f"Probabilidad: {probability}", 
            horizontalalignment='left', verticalalignment='top', transform=plt.gca().transAxes, fontsize=8)
    plt.legend()
    plt.show()


# run_adapt(objective_function=agree_function, num_constant_bests=2)
#Este es el del cupido
population_size = [15,30,45]
num_parents = [5,10,15] 
num_generations = [20,50,80] 
mutation_rate = [0.2,0.5,0.8]
num_agents = [100,300,500] 
num_neighbors = [2,4,8] 
probability = [0.2,0.5,0.7] 
objective_function = notified_function 
num_constant_bests = [1,3,5]


funt = "cupid_function"
result = []
# for pop_size in population_size:
    # for num_par in num_parents:
for num_gen in num_generations:
    for mut_rat in mutation_rate:
        #for num_age in num_agents:
            # for num_nei in num_neighbors:
                # for prob in probability:
                    # for num_cons in num_constant_bests:
                        genet, rand = run_genetic(population_size[1], num_parents[1], num_gen, mut_rat, num_agents[0], num_neighbors[1], probability[1], get_result, num_constant_bests[1])
                        # Agregar un diccionario con los parámetros y los valores máximos a la lista result
                        result.append({
                            "pop_size": population_size[1],
                            "num_par": num_parents[1],
                            "num_gen": num_gen,
                            "mut_rat": mut_rat,
                            "num_age": num_agents[0],
                            "num_nei": num_neighbors[1],
                            "prob": probability[1],
                            "num_cons": num_constant_bests[1],
                            "genet_result": genet,
                            "rand_result": rand
                        })

# Guardar los resultados en un archivo JSON
with open('cupid.json', 'w') as json_file:
    json.dump(result, json_file, indent=2)