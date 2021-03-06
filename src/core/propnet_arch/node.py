import re

class PropNetNode:

    def __init__(self, term):
        self.term = term
        self.value = False
        self.in_edge = None

    def __repr__(self):
        return "{Name: " + str(self.term) + ", Value: " + str(self.value) + ", Condition edge: " + str(self.in_edge) + "}"

    def __eq__(self, other):
        return self.term == other.term

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.term.__hash__()


class PropNetEdge:
    def __init__(self, source_nodes, dest_node, type):
        self.sources = source_nodes
        self.dest = dest_node
        self.type = type

    class Type:
        Identity = 1
        Negation = 2
        Or = 3
        And = 4
        Transition = 5

    def __repr__(self):
        return "Conditions: " + str(self.sources) + ", Type: " + str(self.type)

class Term:

    def __init__(self, term_str):
        self.term_str = term_str
        if re.search(r'\(.*\)', term_str):
            self.inner_terms = props_split(term_str.strip()[1:-1])
        else:
            self.inner_terms = []

        self._set_type()

    def __str__(self):
        return self.term_str

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.term_str == other.term_str

    def is_leaf(self):
        return len(self.inner_terms) == 0

    def __hash__(self):
        return self.term_str.__hash__()

    def _set_type(self):
        if self.term_str == "terminal":
            self.type = Term.Type.Terminal
        elif not self.is_leaf():
            term_type = str(self.inner_terms[0])
            if term_type == "role":
                self.type = Term.Type.Role
            elif term_type == "input":
                self.type = Term.Type.Input
            elif term_type == "base":
                self.type = Term.Type.Base
            elif term_type == "init":
                self.type = Term.Type.Init
            elif term_type == "true":
                self.type = Term.Type.GDLTrue
            elif term_type == "does":
                self.type = Term.Type.Does
            elif term_type == "next":
                self.type = Term.Type.Next
            elif term_type == "legal":
                self.type = Term.Type.Legal
            elif term_type == "goal":
                self.type = Term.Type.Goal
            elif term_type == "terminal":
                self.type = Term.Type.Terminal
            elif term_type == "not":
                self.type = Term.Type.Not
            else:
                self.type = Term.Type.Other
        else:
            self.type = Term.Type.Other

    class Type:
        Base = 1
        Role = 2
        Input = 3
        Init = 4
        GDLTrue = 5
        Does = 6
        Next = 7
        Legal = 8
        Goal = 9
        Terminal = 10
        Not = 11
        Other = 12

def props_split(proposition):
    bracket_count = 0
    recording = False
    terms = []
    term_chars = []
    has_been_gap = False
    last_non_ws_char = ''
    for char in proposition:
        if not char.isspace():
            recording = True
            if char == '(':
                bracket_count += 1
            elif char == ')':
                bracket_count -= 1
            
            if has_been_gap and last_non_ws_char != '(' and char != ')':
                term_chars.append(' ')
            last_non_ws_char = char
            has_been_gap = False
        elif bracket_count == 0:
            recording = False
        else:
            has_been_gap = True

        if recording:
            if not char.isspace():
                term_chars.append(char)
        elif not recording and len(term_chars) > 0:
            terms.append(Term(''.join(term_chars)))
            term_chars = []

    if len(term_chars) > 0:
        terms.append(Term(''.join(term_chars)))

    return terms