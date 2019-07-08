import re

class Term:

    def __init__(self, term_str):
        self.term_str = term_str
        if re.search(r'\(.*\)', term_str):
            self.inner_terms = props_split(term_str.strip()[1:-1])
        else:
            self.inner_terms = []

    def __str__(self):
        return self.term_str

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.term_str == other.term_str

    def is_leaf(self):
        return len(self.inner_terms) == 0

def props_split(proposition):
    bracket_count = 0
    recording = False
    terms = []
    term_chars = []
    for char in proposition:
        if not char.isspace():
            recording = True
            if char == '(':
                bracket_count += 1
            elif char == ')':
                bracket_count -= 1
        elif bracket_count == 0:
            recording = False

        if recording:
            term_chars.append(char)
        elif not recording and len(term_chars) > 0:
            terms.append(Term(''.join(term_chars)))
            term_chars = []

    if len(term_chars) > 0:
        terms.append(Term(''.join(term_chars)))

    return terms

def parse_gdl(description):
    roles = {}
    inputs = {}
    inits = {}
    nexts = {}
    bases = {}
    legals = {}
    goals = {}

    description = description.strip()
    for line in description.splitlines():
        line = line.strip()
        if re.search(r'<=', line):
            search = re.search(r'\(<= ([a-z]+) (.*)\)', line)
            if search is None:
                search = re.search(r'\(<= (\([^)]*\)) (.*)\)', line)
            proposition = search.group(1)
            conditions = search.group(2)
        else:
            proposition = line
            conditions = None

        prop_term = get_prop(proposition)
        cond_terms = get_conditions(conditions)

        if proposition == "terminal":
            prop_type = "terminal"
        elif not prop_term.is_leaf():
            prop_type = str(prop_term.inner_terms[0])
        else:
            prop_type = "other"

        if prop_type == "role":
            roles[proposition] = (prop_term, cond_terms)
        elif prop_type == "input":
            inputs[proposition] = (prop_term, cond_terms)
        elif prop_type == "base":
            bases[proposition] = (prop_term, cond_terms)
        elif prop_type == "init":
            inits[proposition] = (prop_term, cond_terms)
        elif prop_type == "true":
            print("true should not appear as a proposition")
        elif prop_type == "does":
            print("does should not appear as a proposition")
        elif prop_type == "next":
            nexts[proposition]  = (prop_term, cond_terms)
        elif prop_type == "legal":
            legals[proposition] = (prop_term, cond_terms)
        elif prop_type == "goal":
            goals[proposition] = (prop_term, cond_terms)
        elif prop_type == "terminal":
            terminal = ("terminal", cond_terms)
        else:
            print("Is Other")

    print("Roles:", roles)
    print("Inputs:", inputs)
    print("Inits:", inits)
    print("Nexts:", nexts)
    print("Bases:", bases)
    print("Legals:", legals)
    print("Goals:", goals)
    print("Terminal:", terminal)

def get_conditions(conditions):
    if conditions is None:
        return

    return props_split(conditions)


def get_prop(proposition):
    return Term(proposition)


