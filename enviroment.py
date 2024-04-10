from agent import Agent
from message import Message


class Environment:
    _instance = None  # Class attribute to store the single instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.agents = {}  # Initialize agents dictionary
        return cls._instance
    
    def __init__(self):
        self.agents = {}  # Dictionary to store agents by their names

    def register_agent(self, agent):
        self.agents[agent.name] = agent

    def send_message(self, message : Message):
        message.decrease_strength()
        self.replies.append(message)  # Store the sent message as a reply

    def run_simulation(self, initial_message : Message, initial_agents):
        messages = []

        for agent in initial_agents:
            print(initial_message)
            new_message = initial_message.clone().destination(agent)
            messages.append(new_message)

        while messages:
            for message in messages:
                if message.strength > 0:
                    destiny_agent : Agent = self.agents[message.destination]
                    destiny_agent.receive_message(message)
                messages.remove(message)
                
            messages.extend(self.replies)
            self.replies = []