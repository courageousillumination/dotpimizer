#!/usr/bin/env python

from __future__ import print_function
import pydot, sys

if len(sys.argv) < 2:
    print('Usage Error: dotpimizer.py regex-as-str',file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    import regexgraph, graphopt
    g = regexgraph.regex_to_graph(sys.argv[1])
    reps = graphopt.graph_optimize(g)
    i = 0
    for graph in reps[:-1]:
        if i == 0:
            graph.write('init.dot')
        else:
            graph.write('mid'+str(i)+'.dot')
        i += 1
    reps[-1].write('final.dot')
