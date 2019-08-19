import re
from .node import Term, props_split

def parse_gdl(description):
    term_tuples = []
    split = props_split(description)
    for term in split:
        if str(term.inner_terms[0]) == "<=":
            term_tuples.append((term.inner_terms[1], term.inner_terms[2:]))
        else:
            term_tuples.append((term, []))
    return term_tuples
