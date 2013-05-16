dotpimizer
==============

A python utility to convert a regex to automata graphs.

We convert the source regex to an NFA, then perform simplifying transformations on the NFA.
Right now, these consist of simple merges on epsilon transitions and nodes that only have one path in and out.

After we have simplified the NFA, we draw its strongly connected components, which decompose the NFA into parts corresponding to parts of the regex which have been closed with '+' or '*'.
