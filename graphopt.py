import pydot, simplegraph as sg

startname = 's'
terminalname = 't'

def rename_sf(s):
    max_val = max(int(n.name) for n in s.nodes)
    for n in s.nodes:
        if int(n.name) == 0:
            n.name = startname
        elif int(n.name) == max_val:
            n.name = terminalname

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

    rename_sf(s)
    return s

def mk_dotgraph(s):
    g = pydot.Dot(graph_type='digraph')
    nodemap = {}
    for n in s.nodes:
        newn = pydot.Node(n.name)
        if n.name == startname:
            newn.set_label('Start')
        elif n.name == terminalname:
            newn.set_label('Terminal')
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
    specialnames = (startname,terminalname)

    predecessor_map = {}
    for n in s.nodes:
        for (l,m) in n.successors:
            if m == n: continue
            preds = None
            if m in predecessor_map:
                preds = predecessor_map[m]
            else:
                preds = set()
                predecessor_map[m] = preds
            preds.add(n)

    rewrites = {}

    for n in s.nodes:
        for m in s.nodes:
            if n in rewrites or m in rewrites: continue
            if (e,n) in m.successors and (e,m) in n.successors:
                def swap_for_n(m2):
                    if m2 == m:
                        return n
                    else:
                        return m2

                new_successors = set((l,swap_for_n(m2)) for (l,m2) in m.successors)
                new_successors.update((l,swap_for_n(m2)) for (l,m2) in n.successors)

                mark = set()
                for (l,m2) in n.successors:
                    if m2 == m:
                        mark.add((l,m))
                n.successors.difference_update(mark)
                n.successors.update(new_successors)
                n.successors.discard((e,n))

                rewrites[m] = n
                for p in rewrites:
                    if rewrites[p] == m:
                        rewrites[p] = n
                if m.name in specialnames:
                    n.name = m.name

    for n in rewrites:
        for m in predecessor_map[n]:
            if m in rewrites: continue

            new_successors = set()
            for (l,n2) in m.successors:
                if n2.name == n.name:
                    new_successors.add((l,rewrites[n]))
                else:
                    new_successors.add((l,n2))
            m.successors = new_successors

    s.nodes.difference_update(rewrites.keys())

def graph_optimize(graph):
    s = mk_simplegraph(graph)
    merge_epsilons(s)
    components = s.tarjan()
    g = mk_dotgraph(s)
    cluster_index = 0
    for c in components:
        cur = pydot.Cluster(str(cluster_index))
        for n in c:
            cur.add_node(g.get_node(n.name))
        g.add_subgraph(cur)
        cluster_index += 1
    return g
