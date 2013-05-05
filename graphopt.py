import pydot, simplegraph as sg
from regexgraph import epsilon

startname = 's'
terminalname = 't'
s_and_t = 'st'
specialnames = (startname,terminalname,s_and_t)

def rename_sf(s):
    max_val = max(int(n.name) for n in s.nodes)
    for n in s.nodes:
        if int(n.name) == 0:
            n.name = startname
        elif int(n.name) == max_val:
            n.name = terminalname

def mk_simplegraph(g):
    s = sg.Graph()
    edges = g.get_edges()

    node_map = {}
    for n in g.get_nodes():
        newn = sg.Node(n.get_name())
        s.nodes.add(newn)
        node_map[newn] = n
    for newn in node_map:
        n = node_map[newn]
        successor_edges = [e for e in edges if e.get_source() == n.get_name()]
        for e in successor_edges:
            m = e.get_destination()
            ms = [x for x in node_map if (node_map[x].get_name() == m)]
            newm = ms[0]
            l = e.get_label()
            if l == '': l = epsilon
            newn.successors.add((l,newm))

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
        elif n.name == s_and_t:
            newn.set_label('Start/Terminal')
        g.add_node(newn)
        nodemap[n] = newn
    for n in nodemap:
        newn = nodemap[n]
        for (l,m) in n.successors:
            e = pydot.Edge(n.name,m.name)
            e.set_label(l)
            g.add_edge(e)
    return g

def get_pred_map(s):
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

    return predecessor_map

def merge_epsilons(s):
    e = epsilon

    predecessor_map = get_pred_map(s)

    rewrites = {}

    for n in s.nodes:
        if n.name in specialnames: continue
        for m in s.nodes:
            if n in rewrites or m in rewrites: continue
            if m.name in specialnames: continue
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
    return len(rewrites)


def merge_single_path_nodes(s):
    def concat(l1,l2):
        s1 = ''
        s2 = ''
        if l1 != epsilon: s1 = l1
        if l2 != epsilon: s2 = l2
        out = s1+s2
        if out == '':
            out = epsilon
        return out

    pred_map = get_pred_map(s)
    mark = set()
    for n in s.nodes:
        if n.name in specialnames: continue
        new_edges = set()
        for (l,m) in n.successors:
            if m.name in specialnames: continue
            if len(m.successors) == 1 and len(pred_map[m]) == 1:
                (l2,m2) = m.successors.pop()
                if n == m2:
                    m.successors.add((l2,n))
                else:
                    mark.add(m)
                    new_edges.add((concat(l,l2),m2))
                    pred_map[m2].add(n)
        n.successors.update(new_edges)
        n.successors.discard((epsilon,n))

    for m in mark:
        preds = pred_map[m]
        for n in preds:
            mark_edges = set((l,m2) for (l,m2) in n.successors if m2 == m)
            n.successors.difference_update(mark_edges)

    s.nodes.difference_update(mark)
    return len(mark)

def graph_optimize(graph):
    reps = [graph]
    s = mk_simplegraph(graph)
    change = 1
    while change > 0:
        change = merge_epsilons(s)
        if change > 0:
            reps.append(mk_dotgraph(s))
        tmp = merge_single_path_nodes(s)
        if tmp > 0:
            reps.append(mk_dotgraph(s))
        change += tmp

    components = s.tarjan()
    g = mk_dotgraph(s)
    cluster_index = 0
    for c in components:
        cur = pydot.Cluster(str(cluster_index))
        for n in c:
            newn = g.get_node(n.name)
            if not newn:
                print(n.name)
            cur.add_node(newn)
        g.add_subgraph(cur)
        cluster_index += 1
    reps.append(g)
    return reps
