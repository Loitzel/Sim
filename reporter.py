class Reporter:
    _instance = None
    _notified_agents = set()
    _agreed_agents = set()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.filename = "simulation_report.txt"  # Set the filename
        return cls._instance

    def report(self, message, agent_name = None):
        pass
        # with open(self.filename, "a") as file:
            
        #     file.write(str(message) + "\n")

    def reportAgent(self, agent_name):
        self._notified_agents.add(agent_name)
        # print(f"AgentCount: {len(self._notified_agents)}")

    def reportAgreement(self, agent_name):
        self._agreed_agents.add(agent_name)

    def Reset(self):
        self._notified_agents.clear()
        self._agreed_agents.clear()

        