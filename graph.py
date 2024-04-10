import random
import networkx as nx

from agent import Agent
from belief import Belief
from decision_rule import *
from topics import Topics
from enviroment import Environment


def generate_agents_from_graph(num_agents, num_neighbors, probability):
    # Create a small-world graph
    graph = nx.watts_strogatz_graph(n=num_agents, k=num_neighbors, p=probability)

    # Generate agents and assign neighbors
    agents = []

    enviroment = Environment()

    for node in graph.nodes:
        # Store the agent as a node attribute
        belief1 = Belief(Topics.HEALTH_AND_WELLNESS.value, random.randint(-2, 2))
        belief2 = Belief(Topics.TECHNOLOGY_AND_SOCIETY.value, random.randint(-2, 2))
        belief3 = Belief(Topics.ENVIRONMENT_AND_SUSTAINABILITY.value, random.randint(-2, 2))
        beliefs = [belief1, belief2, belief3]
        
        agree_rule = AgreementWithMessageRule()
        disagree_rule = DisagreementWithMessageRule()
        adjust_rule = AdjustMessageRule()
        decision_rules = [agree_rule, disagree_rule, adjust_rule]
        
        agent = Agent(beliefs, decision_rules, [], name=f"Agent_{node}")  # Empty neighbors list for now
        
        enviroment.register_agent(agent)
        agents.append(agent)
        
        graph.nodes[node]['agent'] = agent  # Associate agent with the node

    # Now, iterate again to populate neighbor agents
    for node in graph.nodes:
        agent = graph.nodes[node]['agent']
        neighbors = [graph.nodes[neighbor]['agent'] for neighbor in graph.neighbors(node)]
        agent.neighbors = neighbors

    return agents, graph