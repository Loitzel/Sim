import random

from matplotlib import pyplot as plt
from genetic import genetic_algorithm
from graph import generate_agents_from_graph
from genetic import get_agreement_agents_count as agree_function
from genetic import get_notified_agents_count as notified_function


def run_experiment(population_size = 20, num_parents = 5, num_generations = 100, mutation_rate = 0.1, num_agents = 500, num_neighbors = 4, probability = 0.2, objective_function = notified_function):

    agents, _ = generate_agents_from_graph(num_agents, num_neighbors, probability)

    # Seleccionar agentes iniciales
    initial_agent_indices = random.sample(range(num_agents), 3) 
    initial_agent_indices = [1,2,3]
    initial_agents = [agents[i] for i in initial_agent_indices]

    # Ejecutar el algoritmo genético
    best_message, results_list = genetic_algorithm(population_size, num_parents, num_generations, mutation_rate, initial_agents, objective_function)

    # Graficar los resultados
    plt.plot(results_list)
    plt.xlabel("Generación")
    plt.ylabel("Mejor Resultado (Cantidad de Agentes Notificados)")
    # Agregar texto con los valores de los parámetros
    plt.text(0.05, 0.95, f"Tamaño de Población: {population_size}\n"
                        f"Número de Padres: {num_parents}\n"
                        f"Número de Generaciones: {num_generations}\n"
                        f"Tasa de Mutación: {mutation_rate}\n"
                        f"Mejor Resultado: {best_message.result}\n"
                        f"\n"
                        f"Cantidad de Agentes: {num_agents}\n"
                        f"Número de Vecinos: {num_neighbors}\n"
                        f"Probabilidad: {probability}", 
             horizontalalignment='left', verticalalignment='top', transform=plt.gca().transAxes, fontsize=8)
    plt.title("Evolución del Algoritmo Genético")
    plt.show()
    

run_experiment(objective_function=notified_function)