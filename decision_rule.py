from abc import ABC, abstractmethod

from message import Message
class DecisionRule(ABC):
    """Abstract base class for decision rules."""
    @abstractmethod
    def decide(self, agent_beliefs, message_interest, message_agreement, message):
        """Decides whether to transmit the message."""
        pass

    @abstractmethod
    def alter(self, agent_beliefs, common_topics, message_interest, message_agreement, message):
        """Alters the message based on agent beliefs and message agreement."""
        pass
    
class AgreementWithMessageRule(DecisionRule):
    """Decision rule to transmit the message without alterations if agreement and interest are high."""
    def decide(self, agent_beliefs, message_interest, message_agreement, message):
        """Decides whether to transmit the message without alterations."""
        agreement_threshold = 0.5
        interest_threshold = 0.5
        
        if len(message_agreement) == 0:
            average_agreement = 0
        else:
            average_agreement = sum(message_agreement.values()) / len(message_agreement)

        if average_agreement > agreement_threshold and message_interest > interest_threshold:
            return True  # Transmit the message without alterations
        else:
            return False  # Do not transmit the message

    def alter(self, agent_beliefs, common_topics, message_interest, message_agreement, message : Message):
        """Does not alter the message as it is transmitted without changes."""
        new_message = message.clone()
        new_message.strength = new_message.strength + 4
        return new_message
    
    def report(self, agentName, newMessage = None):
        report = f"{agentName}: Mensaje transmitido sin alteraciones debido a alto acuerdo e interés."  # Agrega el reporte
        return report
    

class DisagreementWithMessageRule(DecisionRule):
    """Decision rule to not transmit the message if disagreement and interest are high."""
    def decide(self, agent_beliefs, message_interest, message_agreement, message):
        """Decides whether to not transmit the message."""
        disagreement_threshold = -0.5
        interest_threshold = 0.5

        if len(message_agreement) == 0:
            average_agreement = 0
        else:
            average_agreement = sum(message_agreement.values()) / len(message_agreement)

        if average_agreement < disagreement_threshold and message_interest > interest_threshold:
            return True  # Do not transmit the message
        else:
            return False  # Transmit the message

    def alter(self, agent_beliefs, common_topics, message_interest, message_agreement, message):
        """Does not alter the message as it is not transmitted."""
        return None
    
    def report(self, agentName, newMessage = None):
        report = f"{agentName}: Mensaje no transmitido debido a alto desacuerdo e interés."
        return report


class AdjustMessageRule(DecisionRule):
    """Decision rule to adjust the message based on agreement and interest."""
    def decide(self, agent_beliefs, message_interest, message_agreement, message):
        """Decides whether to adjust the message."""
        agreement_moderation_range = (-0.5, 0.5)
        interest_threshold = 0.5
        
        if len(message_agreement) == 0:
            return False  # No agreement in the message
        average_agreement = sum(message_agreement.values()) / len(message_agreement)

        if agreement_moderation_range[0] <= average_agreement <= agreement_moderation_range[1] and message_interest > interest_threshold:
            return True  # Adjust the message
        else:
            return False  # Do not adjust the message
        
    
    def alter(self, agent_beliefs, common_topics, message_interest, message_agreement, message):
        """Alters the message based on agent beliefs and message agreement."""
        new_message = message.clone()
        for topic in common_topics:  
            if message_agreement[topic] > 0:
                new_message.increase_belief(topic)
            elif message_agreement[topic] <= 0:
                new_message.decrease_belief(topic)

        return new_message
    
    def report(self, agentName, newMessage = None):
        report = f"{agentName}: Mensaje ajustado debido a acuerdo moderado e interés.\nNuevo mensaje:\n{newMessage}"
        return report

class RandomDecisionRule(DecisionRule):
    """Decision rule to randomly transmit the message."""
    def decide(self, agent_beliefs, message_interest, message_agreement, message):
        """Decides whether to transmit the message randomly."""
        import random
        return random.choice([False, True])  # Randomly decide to transmit or not   

    def alter(self, agent_beliefs, common_topics, message_interest, message_agreement, message):
        """Does not alter the message as it is transmitted without changes."""
        return message.clone()
    
    def report(self, agentName, newMessage = None):
        report = f"{agentName}: Mensaje transmitido aleatoriamente."
        return report
    

