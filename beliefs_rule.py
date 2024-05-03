
from abc import ABC, abstractmethod
from belief import Belief
from message import Message


class BeliefRule(ABC):
    @abstractmethod
    def change(self, agent, message_interest, message_agreement, message: Message):
        pass
    
class ConfirmationBiasRule(BeliefRule):

    """Belief rule to adjust beliefs by bias"""
    def change(self, agent, message_interest, message_agreement, message: Message):
        change = False
        agent_beliefs = agent.beliefs
        agent_topics = [agent_belief.topic for agent_belief in agent_beliefs]
        if len(message_agreement) == 0:
            return False
        else:
            for belief in message.beliefs:
                topic = belief.topic
                opinion = belief.opinion
                
                if topic in agent_topics:
                    agent_belief = [agent_belief for agent_belief in agent_beliefs if agent_belief.topic == topic][0]
                    
                    #Delete all beliefs with that topic
                    agent_beliefs = [agent_belief for agent_belief in agent_beliefs if agent_belief.topic != topic]

                    if opinion >= 1:
                        agent_belief.opinion = min(2, opinion + 1)
                    elif opinion <= -1:
                        agent_belief.opinion = max(-2, opinion - 1)

                    agent_beliefs.append(agent_belief)

        agent.beliefs = agent_beliefs
        return change

class CorrelationRule(BeliefRule):
    '''Belief rule that adds a new beliefs from the message if the agreement with the message it's high'''
    
    def change(self, agent, message_interest, message_agreement, message: Message):
        change = False
        agent_beliefs = agent.beliefs
        message_topics = message.get_topics()
        agent_topics = [agent_belief.topic for agent_belief in agent_beliefs]

        amount_of_agrees = 0

        for topic in agent_topics:
            if topic in message_topics:
                
                for belief in agent_beliefs:
                    if belief.topic == topic and belief.opinion * message.get_opinion_for_topic(topic) > 0:
                            amount_of_agrees += 1

        if amount_of_agrees >= 2:
            for topic in message_topics:
                if topic not in agent_topics:
                    agent_beliefs.append(Belief(topic, message.get_opinion_for_topic(topic)))
        
        return change
    
class DenialRule(BeliefRule):
    '''Belief rule that deletes a belief if the agreement with the message it's low'''
    
    def change(self, agent, message_interest, message_agreement, message: Message):
        change = False
        agent_beliefs = agent.beliefs
        message_topics = message.get_topics()
        agent_topics = [agent_belief.topic for agent_belief in agent_beliefs]

        amount_of_disagrees = 0

        for topic in agent_topics:
            if topic in message_topics:
                
                for belief in agent_beliefs:
                    if belief.topic == topic and belief.opinion * message.get_opinion_for_topic(topic) < 0:
                            amount_of_disagrees += 1

        if amount_of_disagrees >= 2:
            for topic in message_topics:
                if topic in agent_topics:
                    agent_beliefs = [agent_belief for agent_belief in agent_beliefs if agent_belief.topic != topic]
                    return change
        
        return change
