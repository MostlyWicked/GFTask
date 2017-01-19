# For this task I have chosen to write simple, clean code with minimal/no use of OOP (no real need of it for a task this simple).
# Python was chosen for this exact reason - while I believe static-typed languages are much better for serious, complicated
# projects, Python does offer very simple, powerful in-built data structures and functions that will simplify and shorten the code
# needed for this task.

# A possible future improvement would be to encapsulate the graph representation into a class, rather than using a dictionary
# for this purpose (can even use the same dictionary format as the graph-class' internal representation). Or use a graph class
# from an external library.
# However, as I said, I don't consider this a strict necessity for a task of this simplicity, therefore I won't bother.

# Note: This implementation can currently only solve the problem for acyclic graphs, that's the best I could do with only one day.

# Specification problems:
# a) The file format can be simplified or shortened - rather than having every edge take up its own line we can use an adjacency list.
# This will result in a shorter file (possibly much shorter), with the disadvantage that selecting individual edges become harder.
# b) It would be much more efficient if there was a requirement that all edges that start in a particular node are grouped together.
# While the example file does this, this wasn't a formal requirement. File with sorted edges would be even better.
# c) Should search terms be case sensitive? It is not clear from the specs, I assumed they *are*.

import sys

    #First argument is the file path, second is the search word.

if len(sys.argv) != 3:
    print "Incorrect number of arguments"
    sys.exit()

def fileToDictGraph(fpath):

    """
        @input: Valid file path. File should be formatted as instructed in the "instructions.md" file.
        
        @output: a Python dictionary where the unique keys are nodes in the graph,
                the value is a list of length 2 - the second element is an integer used for
                marking nodes in the BFS stage. The first element is a list containing
                2-element sub-lists (think of them as mutable tuples) representing edges - each
                sub-list has another node as its first element (representing the node this edge
                leads to), and the edge's weight as its second element.

                {key : [[[node,weight],...],int], ...}
                
        @time complexity: Usually O(|E|) (|E| == number of edges in graph). WC is O(|E|^2) in the very unlikely
                          event of frequent hash collisions in the dictionary.
                
    """
    terminated = False
    try:
        fileOfGraph = open(fpath,'r')
        graphDict = {}

        for ind in xrange(2):
            for fileGraphLine in fileOfGraph:
                parsedLine = fileGraphLine.split(":")
            
                if ind == 0:
                    graphDict[parsedLine[0].strip()] = [[],0]
                    graphDict[parsedLine[2].strip()] = [[],0]   
                else:
                    graphDict[ parsedLine[0].strip() ][0].append( [parsedLine[2].strip() , int(parsedLine[1])] )
            fileOfGraph.seek(0)
                

    except IOError:
        print "Error in fileToDictGraph: Incorrect file path ({})".format(sys.argv[1])
        return None
    except KeyError:
        print "Error in fileToDictGraph: Tried to append entry ({})into nonexisting key ({}).\n".format(parsedLine[2].strip(),parsedLine[0].strip())
        terminated = True
    except:
        print "Error in fileToDictGraph: An unexpected error occurred, terminating program"
        terminated = True
    finally:
        fileOfGraph.close()

    if terminated:
        return None

    return graphDict

def getNodeNeighbours(graph, node):
    return graph[node][0]

def convertToProb(graph):
    """
        @input: graph as dictionary (see output of fileToDictGraph())
        @output: no output. As a side effect, all weights of graph edges are modified in terms of probability of selection (float type)

        @time complexity: O(|V|+|E|) - again, assuming typical hash collision rate.
    """
    for node in graph:
        sumEdges = 0
        for i in xrange(2):
            for edge in getNodeNeighbours(graph, node):
                if i == 0:
                    sumEdges += edge[1]
                else:
                    edge[1] = float(edge[1]) / sumEdges



def searchGraphPathProb(graph, keyword, dicOfTerminals, count=1.0):
    """
        @input: graph - an acyclic graph (dictionary as outputted by fileToDictGraph()) with weights modified by convertToProb()
                keyword - search word (string)
                count - counts multiplied probabilities for recursion, default is 1
                dicOfTerminals - dictionary (should start empty)
                
        @output: fills up d - keys are terminating nodes, values are probability of reaching.
        
        @time complexity: O(|V| + |E|)
    """

    if len(getNodeNeighbours(graph,keyword)) == 0: #if this is a terminal node - stop and add to dictionary.
        if keyword in dicOfTerminals:
            dicOfTerminals[keyword] += count
        else:
            dicOfTerminals[keyword] = count
        return
    
    for edge in getNodeNeighbours(graph,keyword):
        if graph[edge[0]][1] == 0: #if we haven't entered a circle, continue path
            graph[edge[0]][1] = 1 #mark this as a continuation of the current path (for cycle detection)
            searchGraphPathProb(graph, edge[0], dicOfTerminals,count*edge[1])
            graph[edge[0]][1] = 0 #this is no longer a part of the "current" path, mark removed
        else:
            print "Cycle detected in graph - graph has to be acyclic. Terminating program."
            sys.exit()

    
# CODE EXECUTION STARTS HERE

graphDict = fileToDictGraph(sys.argv[1])

if graphDict == None:
    sys.exit()

convertToProb(graphDict)

l={}
try:
    searchGraphPathProb(graphDict,sys.argv[2],l)
except KeyError:
        print "Error - word \"{}\" not found in graph".format(sys.argv[2])
        sys.exit()

for i in l:
    print "Termination node \"{}\" has probability {}% of being reached".format(i,l[i]*100)
