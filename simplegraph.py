#!/usr/bin/env python

class Node(object):
    def __init__(self,name):
        # A list of (label,node) pairs
        self.successors = set()
        self.name = name

class Graph(object):
    def __init__(self):
        self.nodes = set()

    def tarjan(self):
        components = []

        stack = []
        indices = {}
        lowlink = {}

        def strongconnect(node):
            i = 0
            if len(indices) > 0:
                i = max(v for (k,v) in indices.items())+1
            indices[node] = i
            lowlink[node] = i
            stack.append(node)

            for l,m in node.successors:
                if m not in lowlink:
                    strongconnect(m)
                    lowlink[node] = min(lowlink[node],lowlink[m])
                elif m in stack:
                    lowlink[node] = min(lowlink[node],indices[m])

            if lowlink[node] == indices[node]:
                component = set()
                while True:
                    m = stack.pop()
                    component.add(m)
                    if m == node: break
                components.append(component)

        for n in self.nodes:
            if n not in lowlink:
                strongconnect(n)

        return components
