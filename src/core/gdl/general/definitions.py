
class Term:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def set(self, new_val):
        self.value = new_val

    def get(self):
        return self.value