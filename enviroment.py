# from agent import Agent
from message import Message


class Environment:
    _instance = None  # Class attribute to store the single instance

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Environment, cls).__new__(cls)
            cls.instance.agents = {}  # Inicializa agentes aquí
            cls.instance.replies = []  # Inicializa agentes aquí

        return cls.instance

    @classmethod
    def get_instance(cls):
        """Método para obtener la instancia única"""
        if cls._instance is None:
            cls._instance = Environment()
        return cls._instance


    def register_agent(self, agent ):
        self.agents[agent.name] = agent

    def send_message(self, message : Message):
        message.decrease_strength()
        self.replies.append(message)  # Store the sent message as a reply

    def run_simulation(self, initial_message : Message, initial_agents):
        messages = []
        agents_notified = {}
        for agent in initial_agents:
            new_message = initial_message.clone()
            new_message.destination = agent.name
            messages.append(new_message)

        while messages:
            for message in messages:
                if message.strength > 0:
                    try:
                        agents_notified[self.agents[message.destination]]
                        messages.remove(message)
                        
                        continue
                    except:    
                        agents_notified[self.agents[message.destination]] = True
                        destiny_agent = self.agents[message.destination]
                        destiny_agent.receive_message(message)
                messages.remove(message)
                
            messages.extend(self.replies)
            self.replies = []
        
        return len([agent for agent,val in agents_notified.items() if val == True])
        