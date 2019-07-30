import re
from .node import props_split, Term

# TODO: parse with variables
def parse_gdl(description):
    term_tuples = []
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
        term_tuples.append((prop_term, cond_terms))

    return term_tuples

def get_conditions(conditions):
    if conditions is None:
        return []

    return props_split(conditions)


def get_prop(proposition):
    return Term(proposition)
