#!/usr/bin/env python

from __future__ import print_function
import pydot, sys

if len(sys.argv) < 2:
    print('Usage Error: dotpimizer.py regex-as-str',file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    import regexgraph, graphopt
    g = regexgraph.regex_to_graph(sys.argv[1])
    g.write('init.dot')
    g2 = graphopt.graph_optimize(g)
    g2.write('final.dot')
