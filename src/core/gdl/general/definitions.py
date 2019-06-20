
class Term:

    def __init__(self, name, value=True):
        self.name = name
        self.value = value

    def set(self, new_val):
        self.value = new_val

    def get(self):
        return self.value

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.name.__hash__()

    def __str__(self):
        return self.name