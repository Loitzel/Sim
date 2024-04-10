class Reporter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.filename = "simulation_report.txt"  # Set the filename
        return cls._instance

    def report(self, message):
        with open(self.filename, "a") as file:
            file.write(message + "\n")