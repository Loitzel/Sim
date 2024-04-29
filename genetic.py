import random
from API import TopicExtractor
from belief import Belief
from enviroment import Environment
from message import Message
from reporter import Reporter
from topics import Topics
from agent import Agent
from cupid import Cupid

def get_notified_agents_count(_):
    reporter = Reporter()
    return len(reporter._notified_agents)
def get_agreement_agents_count(_):
    reporter = Reporter()
    return len(reporter._agreed_agents)

def get_unpairable_pairs(grafo):
    result = Cupid(grafo,0.3)
    return result.solucion_emparejamientos
    
def generate_random_messages(num_messages, num_topics_per_message):
    population = []
    for _ in range(num_messages):
        topics = Topics.select_random_topics(num_topics_per_message)
        beliefs = [Belief(topic.value, random.randint(-2, 2)) for topic in topics]
        message = Message(strength=5, beliefs=beliefs)  # Fuerza inicial 5
        population.append(message)
    return population

def generate_messages_from_prompts(prompts):
    extractor = TopicExtractor()
    population = []
    for prompt in prompts:
        topics = extractor.extract_topics(prompt)
        beliefs = [Belief(topic[0], topic[1]) for topic in topics]
        message = Message(strength=5, beliefs=beliefs)
        population.append(message)
    return population

def generate_messages_with_specific_topics(topics, num_messages):
    population = []
    for _ in range(num_messages):
        beliefs = [Belief(topic.value, random.randint(-2, 2)) for topic in topics]
        message = Message(strength=5, beliefs=beliefs)
        population.append(message)
    return population

def evaluate_message(population, graph, initial_agents, objective_function, reset = True):
    environment = Environment.get_instance()
    for message in population:
        if message.result > 0:
            continue

        reporter = Reporter()
        # Ejecutar la simulación para cada mensaje
        environment.run_simulation(message, initial_agents)
        score = objective_function(graph)
        reporter = Reporter()
        reporter.Reset()

        if reset:
            environment.Reset()
        # Almacenar el resultado (cantidad de agentes notificados)
        message.result = score

def select_parents(population, num_parents):
    """Selecciona los padres con base en el atributo 'result' de los mensajes."""
    # Ordenar la población por el atributo 'result' (de mayor a menor)
    population.sort(key=lambda message: message.result, reverse=True)
    print([message.result for message in population])
    
    # Seleccionar los primeros 'num_parents' mensajes como padres
    parents = population[:num_parents]
    print([message.result for message in parents])
    return parents

def crossover1(parent1, parent2):
    """Realiza el cruce entre dos padres y combina creencias."""
    beliefs1 = parent1.beliefs
    beliefs2 = parent2.beliefs

    # Encontrar tópicos comunes y promediar opiniones
    common_topics = set(belief.topic for belief in beliefs1) & set(belief.topic for belief in beliefs2)
    child_beliefs = []
    for topic in common_topics:
        opinion1 = next(belief.opinion for belief in beliefs1 if belief.topic == topic)
        opinion2 = next(belief.opinion for belief in beliefs2 if belief.topic == topic)
        average_opinion = (opinion1 + opinion2) / 2
        rounded_opinion = round(average_opinion)  # Redondear al entero más cercano
        child_beliefs.append(Belief(topic, rounded_opinion))

    # Agregar tópicos no comunes de los padres
    for belief in beliefs1 + beliefs2:
        if belief.topic not in common_topics:
            child_beliefs.append(belief)

    # Limitar el número de creencias a 5 al azar
    random.shuffle(child_beliefs)
    child_beliefs = child_beliefs[:5]

    # Crear un nuevo mensaje con las creencias combinadas
    child_message = Message(strength=5, beliefs=child_beliefs)

    return child_message

def crossover2(parent1, parent2):
    '''Mix of both parents beliefs randomly'''
    beliefs1 = parent1.beliefs
    beliefs2 = parent2.beliefs

    #promedio entero de la cantidad de beliefs de los padres
    amount = (len(beliefs1) + len(beliefs2)) // 2

    #mezcla de beliefs de ambos padres
    child_beliefs = []
    while len(child_beliefs) < amount:
        for belief in beliefs1:
            if random.random() < 0.5:
                child_beliefs.append(belief)
        for belief in beliefs2:
            if random.random() < 0.5:
                child_beliefs.append(belief)

    child_message = Message(strength=5, beliefs=child_beliefs)

    return child_message
            
def mutate(message, mutation_rate=0.1):
    """Aplica mutaciones al mensaje."""
    mutated_beliefs = []
    for belief in message.beliefs:
        if random.random() <= mutation_rate:
            # Decidir si modificar el valor o agregar un nuevo topic
            if random.random() < 0:
                # Modificar el valor del topic
                new_opinion = random.randint(-2, 2)
                mutated_beliefs.append(Belief(belief.topic, new_opinion))
            else:
                # Agregar un nuevo topic
                new_topic = Topics.select_random_topics(1)[0].value
                new_opinion = random.randint(-2, 2)
                mutated_beliefs.append(Belief(new_topic, new_opinion))
        else:
            # Mantener la creencia sin cambios
            mutated_beliefs.append(belief)

    # Crear un nuevo mensaje con las creencias mutadas
    mutated_message = Message(strength=message.strength, beliefs=mutated_beliefs)
    return mutated_message

def reproduce(parent1, parent2, mutation_rate=0.1):
    """Realiza el cruce y la mutación para crear un nuevo hijo."""
    child_message = crossover1(parent1, parent2)
    mutated_child = mutate(child_message, mutation_rate)
    return mutated_child

def genetic_algorithm(population_size, graph,  num_parents, num_generations, mutation_rate, initial_agents, objective_function = get_notified_agents_count, num_constant_bests = 1, randomSearch = False, initial_message = None):
    # Generar la población inicial
    population = generate_random_messages(population_size, num_topics_per_message=5)
    
    if initial_message is not None:
        population = population + [initial_message]

    evolution_list = []
    average_list = []
    global_best = [None, 0]
    best_score_persistance = 10

    previous_best = None
    for generation in range(num_generations):
        print(generation)
        # Evaluar la población
        evaluate_message(population, graph, initial_agents, objective_function)

        if previous_best is not None:
            population = population + previous_best
        # Imprimir información de la generación
        best_message = max(population, key=lambda message: message.result)

        average_score = sum(message.result for message in population) / population_size

        # print(best_message.result)
        evolution_list.append(best_message.result)
        average_list.append(average_score)


        if global_best[1] < best_message.result:
            global_best = (best_message, best_message.result)

        # Seleccionar padres
        parents = select_parents(population, num_parents)

        # Crear nueva generación
        new_population = []
        for _ in range(population_size):
            # Seleccionar padres aleatoriamente
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            # Reproducir (cruce y mutación)
            child = reproduce(parent1, parent2, mutation_rate)

            # Agregar el hijo a la nueva población
            new_population.append(child)

        # Reemplazar la población actual con la nueva generación
        if previous_best == population[:num_constant_bests]:
            best_score_persistance -= 1
        
        if best_score_persistance > 0:
            previous_best = population[:num_constant_bests]
            if initial_message is not None:
                previous_best = previous_best + [initial_message]
        else:
            best_score_persistance = 10
            previous_best = generate_random_messages(num_constant_bests, num_topics_per_message=5)
            if initial_message is not None:
                previous_best = previous_best + [initial_message]
            

        if randomSearch:
            population = generate_random_messages(population_size, num_topics_per_message=5)
        else:
            population = new_population

    return global_best[0], evolution_list

def optimize_graph(number_of_iterations, population_size, graph,  num_parents, num_generations, mutation_rate, initial_agents, objective_function = get_notified_agents_count, num_constant_bests = 1, randomSearch = False):
    
    best_message = None
    message_list = []
    result_list = []

    environment = Environment()
    
    for iteration in range(number_of_iterations):
        best_message, _ = genetic_algorithm(population_size, graph,  num_parents, num_generations, mutation_rate, initial_agents, objective_function, num_constant_bests, randomSearch, best_message)
        evaluate_message([best_message], graph, initial_agents, objective_function, reset=False)

        message_list.append(best_message)
        result_list.append(best_message.result)
        environment.SetCurrentAsDefault()

    return message_list, result_list

