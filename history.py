class History:
    def __init__(self):
        self.history = []

    def add_to_history(self, url):
        self.history.append(url)

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history.clear()