import random

from matplotlib import pyplot as plt
from cupidNew import get_result
from genetic import genetic_algorithm, optimize_graph
from graph import generate_agents_from_graph
from genetic import get_agreement_agents_count as agree_function
from genetic import get_notified_agents_count as notified_function
from API import *

def run_genetic(population_size = 30, num_parents = 5, num_generations = 100, mutation_rate = 0.5, num_agents = 300, num_neighbors = 4, probability = 0.2, objective_function = notified_function, num_constant_bests = 1, graph_evolution = False):

    agents, graph = generate_agents_from_graph(num_agents, num_neighbors, probability)

    # Seleccionar agentes iniciales
    initial_agent_indices = random.sample(range(num_agents), 3) 
    initial_agent_indices = [1,2,3]
    initial_agents = [agents[i] for i in initial_agent_indices]

    # Ejecutar el algoritmo genético
    best_message, results_list = genetic_algorithm(population_size, graph, num_parents, num_generations, mutation_rate, initial_agents, objective_function, num_constant_bests)

    if graph_evolution:
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

    return best_message


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
# run_genetic(population_size = 30, num_parents = 5, num_generations = 10, mutation_rate = 0.5, num_agents = 50, num_neighbors = 2, probability = 0.5, objective_function = get_result, num_constant_bests = 3)
#run_genetic(population_size = 30, num_parents = 10, num_generations = 100, mutation_rate = 0.5, num_agents = 300, num_neighbors = 4, probability = 0.2, objective_function = notified_function, num_constant_bests = 1)
#run_genetic(population_size = 30, num_parents = 8, num_generations = 75, mutation_rate = 0.5, num_agents = 200, num_neighbors = 4, probability = 0.2, objective_function = agree_function, num_constant_bests = 2)
#run_genetic(population_size = 50, num_parents = 10, num_generations = 70, mutation_rate = 0.7, num_agents = 100, num_neighbors = 4, probability = 0.5, objective_function = notified_function, num_constant_bests = 3)
#run_genetic(population_size = 30, num_parents = 5, num_generations = 85, mutation_rate = 0.5, num_agents = 500, num_neighbors = 7, probability = 0.6, objective_function = get_result(0.8), num_constant_bests = 1)
#run_genetic(population_size = 30, num_parents = 7, num_generations = 60, mutation_rate = 0.5, num_agents = 300, num_neighbors = 7, probability = 0.4, objective_function = agree_function, num_constant_bests = 1)
# run_adapt(objective_function=get_result, num_constant_bests=2)

# prompt ="Las multinacionales multimillonarias son pilares de la economía global. Generan empleo, promueven la innovación y contribuyen al desarrollo económico. Su escala les permite optimizar recursos y ofrecer una amplia gama de productos y servicios. Además, lideran en investigación y desarrollo, colaboran en responsabilidad social corporativa y fomentan el progreso científico y tecnológico. En resumen, su impacto positivo en la sociedad es significativo y multifacético."
# message = run_genetic()
# generated_beliefs = message.get_beliefs()
# topic_extractor = TopicExtractor()
# original_beliefs = topic_extractor.extract_topics(prompt)

# message_generator = MessageGenerator()
# message = message_generator.generate_message(prompt, original_beliefs, generated_beliefs)
# print(f"Original message: {prompt}")
# print(f"Original Beliefs: {original_beliefs}")
# print("-------------------------------------")
# print(f"Generated Beliefs: {generated_beliefs}")
# print(f"Generated message: {message}")


# run_genetic(population_size = 30, num_parents = 5, num_generations = 10, mutation_rate = 0.5, num_agents = 50, num_neighbors = 2, probability = 0.5, objective_function = get_result, num_constant_bests = 3)
#Cambio en el tamanno de la poblacion
# run_genetic(population_size = 30, num_parents = 5, num_generations = 10, mutation_rate = 0.5, num_agents = 10, num_neighbors = 2, probability = 0.5, objective_function = get_result, num_constant_bests = 3)