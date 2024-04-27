import random

from matplotlib import pyplot as plt
from cupidNew import get_result
from genetic import genetic_algorithm, optimize_graph
from graph import generate_agents_from_graph
from genetic import get_agreement_agents_count as agree_function
from genetic import get_notified_agents_count as notified_function


def run_genetic(population_size = 30, num_parents = 5, num_generations = 100, mutation_rate = 0.5, num_agents = 300, num_neighbors = 4, probability = 0.2, objective_function = notified_function, num_constant_bests = 1):

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
    plt.show()


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


run_adapt(objective_function=agree_function, num_constant_bests=2)
#Este es el del cupido
# run_adapt(objective_function=get_result, num_constant_bests=2)
