import pydot, simplegraph as sg

def mk_simplegraph(g):
    s = sg.Graph()

    node_map = {}
    for n in g.get_nodes():
        newn = sg.Node()
        s.nodes.add(newn)
        node_map[newn] = n
    for newn in node_map:
        n = node_map[newn]
        edges = g.get_edges()
        edges = [e for e in edges if e.get_source() == n.get_name()]
        for e in edges:
            m = e.get_destination()
            ms = [x for x in node_map if (node_map[x].get_name() == m)]
            newm = ms[0]
            newn.neighbors.add((e.get_label(),newm))
    return (s,node_map)

def graph_optimize(graph):
    s,nodemap = mk_simplegraph(graph)
    components = s.tarjan()
    cluster_index = 0
    for c in components:
        cur = pydot.Cluster(str(cluster_index))
        for n in c:
            cur.add_node(nodemap[n])
        graph.add_subgraph(cur)
        cluster_index += 1
    return graph
