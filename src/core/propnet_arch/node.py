
class PropNetNode:

    def __init__(self, name, init_value, type=None):
        self.name = name
        self.value = init_value
        self.type = type
        self.edges = []

    def add_edge(self, dest_node, type):
        self.edges.append(self.PropNetEdge(self, dest_node, type))

class PropNetEdge:
    def __init__(self, source_node, dest_node, type):
        self.source = source_node
        self.dest = dest_node
        self.type = type

    class Type:
        Identity = 1
        Negation = 2
        Or = 3
        And = 4
        Nor = 5
        Nand = 6