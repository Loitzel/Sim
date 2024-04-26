
class Belief:
    """Represents a belief with a topic and an opinion."""
    def __init__(self, topic, opinion):
        self.topic = topic
        self.opinion = opinion

    def __str__(self):
        return f"{self.topic}: {self.opinion}"
    
    def get_belief(self):
        """Returns the belief as a tuple (topic, opinion)."""
        return (self.topic, self.opinion)
    
    def __eq__(self, value: object) -> bool:
        return self.topic == value.topic