import pydot, simplegraph as sg

def mk_simplegraph(g):
    s = sg.Graph()

    node_map = {}
    for n in g.get_nodes():
        newn = sg.Node(n.get_name())
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
            newn.successors.add((e.get_label(),newm))
    return s

def mk_dotgraph(s):
    g = pydot.Dot(graph_type='digraph')
    nodemap = {}
    for n in s.nodes:
        newn = pydot.Node(n.name)
        g.add_node(newn)
        nodemap[n] = newn
    for n in nodemap:
        newn = nodemap[n]
        for (l,m) in n.successors:
            e = pydot.Edge(n.name,m.name)
            e.set_label(l)
            g.add_edge(e)
    return g

def merge_epsilons(s):
    from regexgraph import epsilon as e
    removed_nodes = set()
    for n in s.nodes:
        if n in removed_nodes: continue
        for m in s.nodes:
            if n in removed_nodes or m in removed_nodes: continue
            if (e,n) in m.successors and (e,m) in n.successors:
                n.successors.update(m.successors)
                n.successors.discard((e,m))
                if m in m.successors:
                    n.successors.add((e,n))
                removed_nodes.add(m)
                if n.name == '0' or m.name == '0':
                    n.name = '0'
    s.nodes.difference_update(removed_nodes)

def graph_optimize(graph):
    s = mk_simplegraph(graph)
    components = s.tarjan()
    g = mk_dotgraph(s)
#    cluster_index = 0
#    for c in components:
#        cur = pydot.Cluster(str(cluster_index))
#        for n in c:
#            cur.add_node(nodemap[n])
#        graph.add_subgraph(cur)
#        cluster_index += 1
    return graph
