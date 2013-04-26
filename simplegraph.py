#!/usr/bin/env python

class Node(object):
    def __init__(self,name):
        # A list of (label,node) pairs
        self.neighbors = []
        self.name = name

class Graph(object):
    def __init__(self):
        self.nodes = []
