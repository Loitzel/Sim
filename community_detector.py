def opinion(agent, topic):
    for b in agent.beliefs:
        if b.topic == topic:
            return b.opinion
                                
# def get_comunities(agents):
#     communities = {}
#     for i, agent_1 in enumerate(agents):
#         topics_1 = {belief.topic for belief in agent_1.beliefs}
#         for j in range(i+1, len(agents)):
#             agent_2 = agents[j]
#             topics_2 = {belief.topic for belief in agent_2.beliefs}
#             common_topics = topics_1 & topics_2
#             for topic in common_topics:
#                 if abs(opinion(agent_1, topic) - opinion(agent_2, topic)) <= 1:
#                     communities[topic] = communities.get(topic, 0) + 1
#     return communities

                                
def get_highly_endorsed_messages(agents):
    communities = {}
    for agent in agents:
        for belief in agent.beliefs:
           communities[(belief.topic, belief.opinion >= 0)] = communities.get((belief.topic, belief.opinion >= 0), 0) + 1
    
    result = sorted(communities.items(), key=lambda x: x[1], reverse=True)[:2]
    return [topic for topic, _ in result]