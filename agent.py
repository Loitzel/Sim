from abc import ABC, abstractmethod
from message import Message
from reporter import Reporter
from enviroment import Environment
class AgentInterface(ABC):
    """Abstract base class for agent interfaces."""
    @abstractmethod
    def receive_message(self, message):
        """Receives a message and triggers the agent's deliberation."""
        pass

    @abstractmethod
    def deliberate(self, message, agreement, interest, common_topics):
        """Deliberates on whether to transmit, alter, or not transmit the message."""
        pass

    @abstractmethod
    def execute_action(self, message):
        """Executes the action determined by the deliberation."""
        pass
    


class Agent(AgentInterface):
    """Agent class implementing the AgentInterface."""
    def __init__(self, beliefs, decision_rules, neighbors, name=''):
        """Initializes the agent with beliefs and decision rules."""
        self.name = name
        self.beliefs = beliefs  # Agent's beliefs
        self.decision_rules = decision_rules  # Decision rules for deliberation
        self.neighbors = neighbors  # Add neighbors attribute

    def receive_message(self, message: Message):
        """Receives a message and initiates the deliberation process."""
        message_beliefs = message.get_beliefs()
        agent_beliefs = {belief.topic: belief.opinion for belief in self.beliefs}

        agreement_with_message, interest_on_message, common_topics = self.calculate_agreement_and_interest(agent_beliefs, message_beliefs)
        self.deliberate(message, agreement_with_message, interest_on_message, common_topics)

    def deliberate(self, message : Message, agreement, interest, common_topics):
        """Deliberates on whether to transmit, alter, or not transmit the message."""
        new_message : Message = message.clone()
        agent_report = ''

        for rule in self.decision_rules:
            decision = rule.decide(self.beliefs, interest, agreement, message)
            if decision:
                new_message = rule.alter(self.beliefs, common_topics, interest, agreement, new_message)
        
        if message is not None:
            for neighbor in self.neighbors:
                if neighbor == message.source:
                    continue
                new_message = message.clone()  # Create a copy for each neighbor
                new_message.source = self.name
                new_message.destination = neighbor
                agent_report = rule.report(self.name, new_message)
                self.execute_action(new_message, agent_report)
        
    def execute_action(self, message, agent_report):
        environment = Environment()  # Access the singleton Environment
        reporter = Reporter()
        print(message)
        environment.send_message(message)
        reporter.report(agent_report)

    def calculate_agreement_and_interest(self, agent_beliefs, message_beliefs):
        """Calculates agreement and interest between agent beliefs and message beliefs."""
        common_topics = set(agent_beliefs.keys()) & set(message_beliefs.keys())

        agreement_scores = {}

        for topic in common_topics:
            total_agreement = abs(agent_beliefs[topic] - message_beliefs[topic])
            max_possible_agreement = 2  # Maximum agreement possible on a single topic (both opinions are +2 or -2)

            agreement_score = 1 - (total_agreement / max_possible_agreement)  # Convert difference to agreement score
            agreement_scores[topic] = agreement_score

        return agreement_scores, len(common_topics), common_topics
    
    def __str__(self):
        return self.name
