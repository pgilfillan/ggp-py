from .node import PropNetNode, PropNetEdge, Term
from .util import parse_gdl

class PropNet:

    def __init__(self, description):
        self.nodes = {}
        self.init_marking = set()

        self.bases = set()
        self.inputs = set()
        self.roles = set()
        self.legals = set()
        self.rewards = set()
        self.views = set()
        self.terminal = None

        self.dummy_count = 0

        term_tuples = parse_gdl(description)
        for term_tuple in term_tuples:
            self.add_node(term_tuple[0], term_tuple[1])

        print("Init marking:", self.init_marking)
        print()
        for base_node_str in self.init_marking:
            self.nodes[base_node_str].value = True
        
        for node_name in self.nodes:
            print(self.nodes[node_name])


    def add_node(self, term, conditions=[]):
        term_str = str(term)

        if term_str in self.nodes:
            old_node = self.nodes[term_str]

            if len(conditions) > 0:
                if old_node.in_edge is not None:
                    # If the old node has an AND or NOT edge type, add a dummy node to combine the sources into one node
                    if old_node.in_edge.type == PropNetEdge.Type.And or old_node.in_edge.type == PropNetEdge.Type.Negation:
                        dummy_node = self.add_dummy_node()
                        old_node.in_edge.dest = dummy_node
                        new_edge = PropNetEdge([dummy_node], old_node, PropNetEdge.Type.Or)
                        old_node.in_edge = new_edge

                    old_node.in_edge.type = PropNetEdge.Type.Or
                    self.add_conditions_with_or(conditions, old_node)

                else:
                    add_conditions_to_node(conditions, old_node)

            return old_node
        else:
            new_node = self.new_node_add(term)
            self.add_conditions_to_node(conditions, new_node)
            return new_node


    def add_conditions_to_node(self, conditions, node):
        if len(conditions) == 0:
            return
        elif len(conditions) == 1:
            if conditions[0].Type == Term.Type.Not:
                cond_node = self.add_node(conditions[0].inner_terms[1])
                new_edge = PropNetEdge([cond_node], node, PropNetEdge.Type.Negation)
            else:
                cond_node = self.add_node(conditions[0])
                new_edge = PropNetEdge([cond_node], node, PropNetEdge.Type.Identity)
            node.in_edge = new_edge
        else:
            new_edge = PropNetEdge([], node, PropNetEdge.Type.And)
            node.in_edge = new_edge
            for condition in conditions:
                if condition.type == Term.Type.Not:
                    cond_node = self.add_node(condition.inner_terms[1])
                    dummy_node = self.add_dummy_node()
                    dummy_edge = PropNetEdge([cond_node], dummy_node, PropNetEdge.Type.Negation)
                    dummy_node.in_edge = dummy_edge
                    source_node = dummy_node
                else:
                    source_node = self.add_node(condition)

                new_edge.sources.append(source_node)

    # Assumes node already has an OR type in_edge
    def add_conditions_with_or(self, conditions, node):
        if len(conditions) == 0:
            return
        elif len(conditions) == 1 and conditions[0].type != Term.Type.Not:
            cond_node = self.add_node(conditions[0])
            node.in_edge.sources.append(cond_node)
        else:
            dummy_node = self.add_dummy_node()
            self.add_conditions_to_node(conditions, dummy_node)
            node.in_edge.sources.append(dummy_node)


    def add_dummy_node(self):
        dummy_string = "dummy" + str(self.dummy_count)
        dummy_node = PropNetNode(Term(dummy_string))
        self.nodes[dummy_string] = dummy_node
        self.views.append(dummy_node)
        self.dummy_count += 1
        return dummy_node


    def new_node_add(self, term):
        prop_type = term.type
        if prop_type == Term.Type.Role:
            new_node = PropNetNode(term)
            self.roles.add(new_node)
        elif prop_type == Term.Type.Input:
            # Don't need to do anything with input terms:
            # can use legals instead + input should 
            # not be a condition, can return
            return
        elif prop_type == Term.Type.Base:
            base_term = term.inner_terms[1]
            base_str = str(base_term)

            if base_str not in self.nodes:
                new_node = PropNetNode(base_term)
                self.bases.add(new_node)
                self.nodes[base_str] = new_node
                return new_node
            else:
                return self.nodes[base_str]
        elif prop_type == Term.Type.Init:
            self.init_marking.add(str(term.inner_terms[1]))
            # Init should have not be a condition, can return
            return
        elif prop_type == Term.Type.GDLTrue:
            prop_term = term.inner_terms[1]
            prop_term_str = str(prop_term)

            if prop_term_str not in self.nodes:
                new_node = PropNetNode(prop_term)
                self.bases.add(new_node)
                self.nodes[prop_term_str] = new_node
                return new_node
            else:
                return self.nodes[prop_term_str]
        elif prop_type == Term.Type.Does:
            input_term_str = "(" + str(term.inner_terms[1]) + " " + str(term.inner_terms[2]) + ")"
            if input_term_str not in self.nodes:
                new_node = PropNetNode(Term(input_term_str))
                self.inputs.add(new_node)
                self.nodes[input_term_str] = new_node
                return new_node
            else:
                return self.nodes[input_term_str]
        elif prop_type == Term.Type.Next:
            new_node = PropNetNode(term)
            self.views.add(new_node)

            base_term = term.inner_terms[1]
            base_str = str(base_term)
            if base_str not in self.nodes:
                base_node = PropNetNode(base_term)
                self.bases.add(base_node)
                self.nodes[base_str] = base_node
            else:
                base_node = self.nodes[base_str]

            new_edge = PropNetEdge([new_node], base_node, PropNetEdge.Type.Transition)
            base_node.in_edge = new_edge
        elif prop_type == Term.Type.Legal:
            new_node = PropNetNode(term)
            self.legals.add(new_node)

            input_term_str = "(" + str(term.inner_terms[1]) + " " + str(term.inner_terms[2]) + ")"
            if input_term_str not in self.nodes:
                new_input_node = PropNetNode(Term(input_term_str))
                self.inputs.add(new_input_node)
                self.nodes[input_term_str] = new_input_node
        elif prop_type == Term.Type.Goal:
            new_node = PropNetNode(term)
            self.rewards.add(new_node)
        elif prop_type == Term.Type.Terminal:
            new_node = PropNetNode(term)
            self.terminal = new_node
        else:
            new_node = PropNetNode(term)
            self.views.add(new_node)

        self.nodes[str(term)] = new_node
        return new_node
