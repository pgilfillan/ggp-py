from .node import PropNetNode, PropNetEdge, Term
from .util import parse_gdl

class PropNet:

    ###### Methods for PropNet creation ######
    
    def __init__(self, description):
        self.nodes = {}
        self.init_marking = set()
        self.roles = set()

        self.bases = {}
        self.inputs = {}
        self.legals = {}
        self.rewards = {}
        self.views = set()
        self.terminal = None

        self.dummy_count = 0

        term_tuples = parse_gdl(description)
        for term_tuple in term_tuples:
            self.add_node(term_tuple[0], term_tuple[1])

        #print("Init marking:", self.init_marking)
        #print("Roles:", self.roles)
        #print()
        for base_node_str in self.init_marking:
            self.nodes[base_node_str].value = True
        
        for node_name in self.nodes:
            pass
            #print(self.nodes[node_name].term)
        #print("\nNum nodes:", len(self.nodes))
        #print("Dummy count:", self.dummy_count)
        #print()

        #print("Legals:", self.legals)
        #print("Bases:", self.bases)
        #print("Inputs:", self.inputs)
        #print("Terminal:", self.terminal)
        #print("Rewards:", self.rewards)
        #print("Views:", self.views)

    def __str__(self):
        node_values = [str((self.nodes[node].term, self.nodes[node].value)) for node in self.nodes]
        return '\n'.join(node_values) + '\n'


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
                    self.add_conditions_to_node(conditions, old_node)

            return old_node
        else:
            new_node = self.new_node_add(term)
            self.add_conditions_to_node(conditions, new_node)
            return new_node


    def add_conditions_to_node(self, conditions, node):
        if len(conditions) == 0:
            return
        elif len(conditions) == 1:
            if conditions[0].type == Term.Type.Not:
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
        self.views.add(dummy_node)
        self.dummy_count += 1
        return dummy_node


    def new_node_add(self, term):
        prop_type = term.type
        if prop_type == Term.Type.Role:
            self.roles.add(str(term.inner_terms[1]))
            # Role should not have a condition, can return
            return
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
                self.bases[base_str] = new_node
                self.nodes[base_str] = new_node
                return new_node
            else:
                return self.nodes[base_str]
        elif prop_type == Term.Type.Init:
            self.init_marking.add(str(term.inner_terms[1]))
            # Init should have not be a condition, can return
            return
        elif prop_type == Term.Type.GDLTrue:
            base_term = term.inner_terms[1]
            base_str = str(base_term)

            if base_str not in self.nodes:
                new_node = PropNetNode(base_term)
                self.bases[base_str] = new_node
                self.nodes[base_str] = new_node
                return new_node
            else:
                return self.nodes[base_str]
        elif prop_type == Term.Type.Does:
            input_term_str = "(" + str(term.inner_terms[1]) + " " + str(term.inner_terms[2]) + ")"
            if input_term_str not in self.nodes:
                new_node = PropNetNode(Term(input_term_str))
                self.inputs[input_term_str] = new_node
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
                self.bases[base_str] = base_node
                self.nodes[base_str] = base_node
            else:
                base_node = self.nodes[base_str]

            new_edge = PropNetEdge([new_node], base_node, PropNetEdge.Type.Transition)
            base_node.in_edge = new_edge
        elif prop_type == Term.Type.Legal:
            new_node = PropNetNode(term)

            role = str(term.inner_terms[1])
            if role not in self.legals:
                self.legals[role] = set()
            self.legals[role].add(new_node)

            input_term_str = "(" + role + " " + str(term.inner_terms[2]) + ")"
            if input_term_str not in self.nodes:
                new_input_node = PropNetNode(Term(input_term_str))
                self.inputs[input_term_str] = new_input_node
                self.nodes[input_term_str] = new_input_node
        elif prop_type == Term.Type.Goal:
            new_node = PropNetNode(term)
            role = str(term.inner_terms[1])
            if role not in self.rewards:
                self.rewards[role] = set()
            self.rewards[role].add(new_node)
        elif prop_type == Term.Type.Terminal:
            new_node = PropNetNode(term)
            self.terminal = new_node
        else:
            new_node = PropNetNode(term)
            self.views.add(new_node)

        self.nodes[str(term)] = new_node
        return new_node

    ###### Methods for PropNet manipulation ######

    def mark_bases(self, true_bases):
        for base in self.bases:
            if base in true_bases:
                self.bases[base].value = True
            else:
                self.bases[base].value = False

    def mark_inputs(self, actions):
        for role in actions:
            input_str = "(" + role + " " + actions[role] + ")"
            self.inputs[input_str].value = True

    def reset_to_initial(self):
        self.clear()
        for base_str in self.init_marking:
            self.bases[base_str].value = True
    
    def clear(self):
        for _, node in self.nodes.items():
            node.value = False

    def node_mark(self, node):
        node_str = str(node.term)

        # Special case: legal nodes with no conditions should always be true
        if node.term.type == Term.Type.Legal and node.in_edge is None:
            return True
        elif node_str in self.bases or node_str in self.inputs or node.in_edge is None:
            return node.value
        
        edge_type = node.in_edge.type
        sources = node.in_edge.sources
        if edge_type == PropNetEdge.Type.Identity:
            source_mark = self.node_mark(sources[0])
            node.value = source_mark
            return node.value
        elif edge_type == PropNetEdge.Type.Negation:
            source_mark = self.node_mark(sources[0])
            node.value = not source_mark
            return node.value
        elif edge_type == PropNetEdge.Type.Or:
            for source in sources:
                source_mark = self.node_mark(source)
                if source_mark:
                    node.value = True
                    return True

            node.value = False
            return False
        elif edge_type == PropNetEdge.Type.And:
            for source in sources:
                source_mark = self.node_mark(source)
                if not source_mark:
                    node.value = False
                    return False
                
            node.value = True
            return True
            
    
    def get_state(self):
        state = set()
        for base, base_node in self.bases.items():
            if base_node.value:
                state.add(base)

        return state