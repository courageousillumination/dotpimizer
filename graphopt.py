import pydot, simplegraph as sg

def mk_simplegraph(g):
    s = sg.Graph()

    node_map = {}
    for n in g.get_nodes():
        newn = sg.Node()
        node_map[newn] = n
    for newn in node_map:
        n = node_map[newn]
        edges = g.get_edge(n,None)
        for e in edges:
            m = e.get_destination()
            ms = [x for x in node_map if (node_map[x] == m)]
            newm = ms[0]
            newn.neighbors.add(e.get_label(),newm)
    return (s,node_map)

def graph_optimize(graph):
    s,nodemap = mk_simplegraph(graph)
    components = s.tarjan()
    for c in components:
        cur = pydot.Cluster()
        for n in c:
            cur.add_node(nodemap[n])
        graph.add_subgraph(cur)
    return graph
