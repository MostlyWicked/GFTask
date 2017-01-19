# Instructions

## Requirements

Write a program - using any technology that you wish, that accepts a file
containing a description of a directed graph where each node is a word and each
edge (to another word) has a weight associated with it.

Then, given a search word, the program will traverse the graph from a starting
node with the given search word, through all outgoing edges of each connected
node to find all termination nodes (nodes from which there is no outgoing edge),
then generate and print out the probability - in percentage - of reaching each
reachable terminating node, assuming a traveler will travel the graph by
selecting an outgoing edge in a weighted (according to the edge weight)
uniformly distributed random selection.

If the given search word is not found in the graph, output an error message to
that effect.

Additionally, describe problems with the current specification and suggest
changes and/or additional implementation that can be used alleviate them.

## File Format Specification

The directed word graph is stored in a file that describes the edges of the
graph.

The file is formatted as a simple text file where each line describes a single
edge using a colon-delimited format as such:

```
ORIGINATING_WORD:WEIGHT_NUMBER:TERMINATING_WORD
```

For example:

```
beginning:1:ending
```

See provided example file that describes a simple graph containing 15 words.
