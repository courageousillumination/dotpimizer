import pydot

class Token:
    def __init__(self):
        return None
    def add_to_graph(self, graph):
        return None



class OrOp(Token):
    def __init__(self, groups):
        self.groups = groups
    def add_to_graph(self, graph, state, parent = None):
        state+=1
        end_nodes = []
        for group in self.groups:
            graph.add_edge(pydot.Edge(parent, str(state), label="epsilon"))
            state = group.add_to_graph(graph, state)
            end_nodes.append(state-1)
        print end_nodes
        #Create an end node and link everything back to that
        state += 1
        graph.add_node(pydot.Node(str(state)))
        for node in end_nodes:
            graph.add_edge(pydot.Edge(str(node), str(state), label="epsilon"))
        return state
class LiteralExpression(Token):
    def __init__(self, chars):
        self.chars = chars
    
    def add_to_graph(self, graph, state, parent = None):
        #Add the link to the parent
        if parent != None:
            graph.add_edge(pydot.Edge(parent, str(state+1), label=self.char)) 
        state+=1
        for char in self.chars:
            graph.add_node(pydot.Node(str(state)))
            graph.add_edge(pydot.Edge(str(state-1), str(state), label=char))
            state+=1
        return state

                
def tokenize(regex):
    result = []
    #Split on or first cause that binds hella loose
    or_split = regex.split('|')
    if len(or_split) != 1:
        result = [OrOp([tokenize(x) for x in or_split])]
    #Otherwise actually tokenize
    else:
        #Just deal with literal
        result = LiteralExpression(regex)
    return result

def regex_to_graph(regex, graph_name = "regex_graph"):
    """
    Convert a regular expression to a pydot
    graph object. Requires correct parentheses
    
    """
    graph = pydot.Dot(graph_name, graph_type='digraph')
    graph.add_node(pydot.Node('0'))
    state = 0
    
    tokens = tokenize(regex)
    
    for token in tokens:
        state = token.add_to_graph(graph, state, "0")
        
    return graph
