class GreetingClient:
    def __init__(self, name):
        self.name = name

    def get_greeting(self):
        return f"Hello from {self.name}"