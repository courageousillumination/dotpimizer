#!/usr/bin/env python

class Node(object):
    def __init__(self):
        # A list of (label,node) pairs
        self.neighbors = set()

class Graph(object):
    def __init__(self):
        self.nodes = set()

    def tarjan(self):
        components = []

        stack = []
        visited = set()

        indices = {}
        lowlink = {}

        def strongconnect(node):
            i = 0
            if len(indices) > 0:
                i = max(v for (k,v) in indices.items())+1
            indices[node] = i
            lowlink[node] = i
            visited.add(node)
            stack.append(node)

            for l,m in node.neighbors:
                if m not in visited:
                    strongconnect(m)
                    lowlink[node] = min(lowlink[node],lowlink[m])
                elif m in stack:
                    lowlink[node] = min(lowlink[node],indices[m])

            if lowlink[node] == indices[node]:
                component = set()
                components.append(component)
                while stack[-1] != node:
                    component.add(stack.pop())
                component.add(node)

        for n in self.nodes:
            if n not in visited:
                strongconnect(n)

        return components
