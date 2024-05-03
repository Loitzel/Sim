from abc import ABC, abstractmethod

from message import Message

class CommunicationRule(ABC):
    '''Interface for rules that define if a message should be send to another agent'''
    @abstractmethod
    def communicate(self, interest, message_beliefs, neighbor_beliefs, message: Message = None):
        pass

class TalkativeAgentRule(CommunicationRule):
    '''The agent will send the message if there's at least one topic that could interest to the neighbor
    or if it doesn't know anything about the neighbor'''

    def communicate(self, interest, message_beliefs, neighbor_beliefs, message: Message = None):
        if(len(neighbor_beliefs) == 0):
            return True
        
        message_topics = message.get_topics()
        neighbor_topics = [neighbor_belief.topic for neighbor_belief in neighbor_beliefs]
        
        for topic in message_topics:
            if topic in neighbor_topics:
                return True

        return False
    
class ShyAgentRule(CommunicationRule):
    '''The agent will send the message if there's at least one topic that could interest to the neighbor'''

    def communicate(self, interest, message_beliefs, neighbor_beliefs, message: Message = None):
        
        if(len(neighbor_beliefs) == 0):
            return False
        
        message_topics = message.get_topics()
        neighbor_topics = [neighbor_belief.topic for neighbor_belief in neighbor_beliefs]

        for topic in message_topics:
            if topic in neighbor_topics:
                return True

        return False
    
class GossipAgentRule(CommunicationRule):
    '''The agent will always send the message'''

    def communicate(self, interest, message_beliefs, neighbor_beliefs, message: Message = None):
        return True
    
class ExcitedAgentRule(CommunicationRule):
    '''The agent will send the message if there's at least one topic that could interest to the neighbor
    or if it shows high interest on the message'''

    def communicate(self, interest, message_beliefs, neighbor_beliefs, message: Message = None):

        if(len(neighbor_beliefs) == 0):
            return False
        
        message_topics = message.get_topics()
        neighbor_topics = [neighbor_belief.topic for neighbor_belief in neighbor_beliefs]

        if(interest >= 2):
            return True
        
        for topic in message_topics:
            if topic in neighbor_topics:
                return True
            
        return False
