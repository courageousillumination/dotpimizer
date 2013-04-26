import pydot

def regex_to_graph(regex, graph_name = "regex_graph"):
    """
    Convert a regular expression to a pydot
    graph object
    """
    graph = pydot.Dot(graph_name, graph_type='digraph')
    graph.add_node(pydot.Node('0'))
    state = 0
    
    #String code
    for char in regex:
        graph.add_node(pydot.Node(str(state + 1)))
        graph.add_edge(pydot.Edge(str(state), str(state + 1), label=char))
        state += 1
    return graph
