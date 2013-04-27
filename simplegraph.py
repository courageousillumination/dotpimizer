#!/usr/bin/env python

class Node(object):
    def __init__(self,name):
        # A list of (label,node) pairs
        self.neighbors = []
        self.name = name

class Graph(object):
    def __init__(self):
        self.nodes = []

    def tarjan(self):
        components = []

        i = 0
        stack = []
        visited = set()

        indices = {}
        lowlink = {}

        def strongconnect(node):
            indices[node] = i
            lowlink[node] = i
            visited.add(node)
            stack.append(node)
            i += 1

            for m in node.neighbors:
                if m not in visited:
                    strongconnect(m)
                    lowlink[node] = min(lowlink[node],lowlink[m])
                else if m in stack:
                    lowlink[node] = min(lowlink[node],indices[m])
                else:
                    pass

            if lowlink[node] == indices[node]:
                component = set()
                components.append(component)
                while len(stack) > 0 and stack[-1] != node:
                    m = stack.pop()
                    component.add(m)

        for n in self.nodes:
            if n not in visited:
                strongconnect(n)

        return components
