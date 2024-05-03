from belief import Belief
from typing import List

class Message:
    """Represents a message with strength and beliefs."""
    def __init__(self, strength, beliefs, source = None, destination = None):
        self.beliefs:List[Belief] = beliefs
        self.strength = strength
        self.source = source
        self.destination = destination
        self.result = 0
        self.age = 0
    
    def _update_strength(self, delta):
        """Updates the strength of the message by adding delta."""
        self.strength += delta
    
    def increase_strength(self):
        """Increases the strength of the message by 1."""
        return self._update_strength(1)

    def decrease_strength(self):
        """Decreases the strength of the message by 1."""
        return self._update_strength(-1)
    
    def get_topics(self):
        """Returns a list of topics covered in the message."""
        return [belief.topic for belief in self.beliefs]

    def get_beliefs_as_dict(self):
        """Returns a dictionary of beliefs and their opinions."""
        dictionary = {}
        for belief in self.beliefs:
            dictionary[belief.topic] = belief.opinion
        return dictionary

    def change_belief(self, topic, new_opinion):
        """
        Changes the opinion of the belief with the specified topic.
        
        If the topic does not exist in beliefs, creates a new belief.
        """
        for belief in self.beliefs:
            if belief.topic == topic:
                belief.opinion = new_opinion
                return
        self.beliefs.append(Belief(topic, new_opinion))
    
    def get_opinion_for_topic(self, topic):
        for belief in self.beliefs:
            if belief.topic == topic:
                return belief.opinion 
    
    def increase_belief(self, topic):
        """Increases the opinion of the belief with the specified topic by 1."""
        for belief in self.beliefs:
            if belief.topic == topic:
                belief.opinion = min(belief.opinion + 1, 2)
                return

    def decrease_belief(self, topic):
        """Decreases the opinion of the belief with the specified topic by 1."""
        for belief in self.beliefs:
            if belief.topic == topic:
                belief.opinion = max(belief.opinion - 1, -2)
                return

    def clone(self):
        """Returns a copy of the message."""
        clone = Message(self.strength, self.beliefs.copy(), self.source, self.destination)
        clone.result = self.result
        return clone

    def __str__(self):
        """Returns a string representation of the message."""
        message_str = f"Message Strength: {self.strength}\nSource: {self.source}\nDestination:{self.destination}\nBeliefs:\n"
        for belief in self.beliefs:
            message_str += str(belief) + "\n"
        return message_str
    