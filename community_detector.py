import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from itertools import product

communities = {}

def crear_aristas(grafo, agents):
    for i, agent_1 in enumerate(agents):
        for j , agent_2 in enumerate(agents):
            if i < j:
                topics_1 = set([belief.topic for belief in agent_1.beliefs])
                topics_2 = set([belief.topic for belief in agent_2.beliefs])
                common_topics = topics_1 & topics_2
                if len(common_topics) > 0:
                    for topic in common_topics:
                        if abs(opinion(agent_1, topic) - opinion(agent_2, topic)) <= 1:
                            try:
                                communities[topic] += 1
                            except:
                                communities[topic] = 1
                            # grafo.add_edge(agent_1.name[6:], agent_2.name[6:], topic=topic)
                        
def opinion(agent, topic):
    return [b.opinion for b in agent.beliefs if b.topic == topic][0]
    
def get_comunities(agents):
    # Crear un grafo no dirigido
    grafo = nx.MultiGraph()

    # Crear lista de nodos
    nodos = [agent.name[6:] for agent in agents]

    # Añadir nodos al grafo
    grafo.add_nodes_from(nodos)

    # Crear aristas                    
    crear_aristas(grafo, agents)
     
    # print('Community')               
    # print(sorted(nx.community.greedy_modularity_communities(grafo)[0], reverse=True)[:2])
    
    # Imprimir las comunidades más grandes
    print(sorted(communities.items(), key=lambda x: x[1], reverse=True)[:2])
    
    # Posicionamiento de nodos (opcional)
    pos = nx.spring_layout(grafo)

    # Dibujar nodos
    nx.draw_networkx_nodes(grafo, pos=pos, node_size=500, node_color="lightblue")

    # Dibujar aristas
    nx.draw_networkx_edges(grafo, pos=pos, arrowsize=5)

    # Mostrar etiquetas de nodos
    nx.draw_networkx_labels(grafo, pos=pos, font_size=8)

    # Mostrar el gráfico
    plt.show()

    # # Mostrar mapa de colores para nodos (opcional)
    # cmap = cm.get_cmap("viridis")
    # node_colors = [cmap(i) for i in range(len(nodos))]
    # nx.draw_networkx_nodes(grafo, pos=pos, node_size=500, node_color=node_colors)

    # # Mostrar el grafo
    # plt.show()
    
    # Calcular la centralidad de grado de los nodos
    centralidad_grado = nx.degree_centrality(grafo)

    # Identificar nodos con mayor centralidad de grado
    nodos_centrales = [nodo for nodo, valor in centralidad_grado.items() if valor > 0.5]

    # Imprimir información sobre el grafo
    print(f"Número de nodos: {nx.number_of_nodes(grafo)}")
    print(f"Número de aristas: {nx.number_of_edges(grafo)}")
    print(f"Nodos con mayor centralidad de grado: {nodos_centrales}")

# get_comunities(None)





# ## Comunidades mas grandes
# import networkx as nx

# def obtener_dos_comunidades_mas_grandes(grafo):
#     # Obtener todas las componentes conectadas y ordenarlas por tamaño
#     componentes = sorted(nx.connected_components(grafo), key=len, reverse=True)
    
#     # Tomar las dos primeras componentes más grandes
#     dos_grandes = componentes[:2]
    
#     # Crear subgrafos para las dos comunidades más grandes
#     comunidades_grandes = [grafo.subgraph(c) for c in dos_grandes]
    
#     return comunidades_grandes

# # Ejemplo de uso:
# # Suponiendo que 'grafo' es tu objeto de gráfico
# comunidades_grandes = obtener_dos_comunidades_mas_grandes(grafo)

# # Ahora, 'comunidades_grandes' es una lista de dos subgrafos, cada uno representando una de las dos comunidades más grandes














# ### Multigrafo
# import networkx as nx
# import matplotlib.pyplot as plt

# # Crear un MultiGraph
# G = nx.MultiGraph()

# # Agregar aristas con diferentes etiquetas
# G.add_edge(1, 2, label='A')
# G.add_edge(1, 2, label='B')
# G.add_edge(1, 2, label='C')
# G.add_edge(3, 1, label='D')
# G.add_edge(3, 2, label='E')

# # Posicionamiento de nodos
# pos = nx.spring_layout(G)

# # Dibujar nodos
# nx.draw_networkx_nodes(G, pos)

# # Dibujar aristas
# nx.draw_networkx_edges(G, pos)

# # Dibujar etiquetas de aristas
# edge_labels = nx.get_edge_attributes(G, 'label')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# # Mostrar el gráfico
# plt.axis('off')
# plt.show()
