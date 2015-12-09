# pagerank algorith
import math
import sys
import re
import string
import pprint
import time

class PageRank:
   """A class that represents a graph used for pagerank"""
   
   def __init__(self):
      self.degree = {}
      self.destinations = {}
      self.rank = {}
      self.sources = {}

   def addNode(self, node):
      """Add a new source to the graph. Overwrites existing source with
      the same name"""
      if node not in self.degree:
         self.degree[node] = 0
         self.destinations[node] = []
         self.sources[node] = []

   def addEdge(self, source, target):
      """Add a new edge to the graph"""
      if source not in self.degree:
         self.addNode(source)

      if target not in self.degree:
         self.addNode(target)

      self.destinations[source].append(target)
      self.degree[source] = self.degree.get(source,0) + 1

      self.sources[target].append(source)

   def getDegree(self, node):
      """Return the degree of the given node"""
      return self.degree[node]

   def getDestinations(self, source):
      """Return a list of destinations for source"""
      return self.destinations[source]

   def getSources(self, source):
      """Return a list of source nodes"""
      return self.sources[source]

   def printGraph(self):
      """Print out the graph"""

      for node in sorted(self.degree.keys()):
         print "%s\t%d\t%s" % (node, self.degree[node], self.destinations[node])

   def goodEnough(self, newPageRank, oldPageRank):
      """Check if pagerank has conveged"""
      epsilon = 0.00001
      sum = 0
      for node in newPageRank:
         sum += math.fabs(newPageRank[node] - oldPageRank[node])
      
      return sum < epsilon

   def getPageRank(self):
      """Return the number of iterations it took to converge as well as the 
      pagerank of the graph"""

      numOfNodes = len(self.degree)
      for node in self.degree:
         self.rank[node] = 1.0 / numOfNodes 

      d = 0.8
      i = 1
      while True:
         newPageRank = {}
         for node in self.rank:
            sum = 0
            for source in self.sources[node]:
               sum += self.rank[source] / self.degree[source]

            newPageRank[node] = ((1 - d) / numOfNodes) + d * sum

         if (self.goodEnough(newPageRank, self.rank)):
            self.rank = newPageRank
            self.rank = sorted(self.rank.items(), key=lambda x: x[1], reverse=False)[:40]
            return i, self.rank

         self.rank = newPageRank
         i += 1

def getData(fp):
   """Create a PageRank graph from the file"""
   graph = PageRank()
   data = fp.read().splitlines()

   for line in data:
      nodes = re.split(r',', line)
      nodes = [col.strip(' ' + string.punctuation) for col in nodes]

      if int(nodes[1]) > int(nodes[3]):
         graph.addEdge(str(nodes[2]), str(nodes[0]))
      else:
         graph.addEdge(str(nodes[0]), str(nodes[2]))

   return graph

def getDataDirected(fp):
   """Create a PageRank graph from the file"""
   graph = PageRank()
   data = fp.read().splitlines()

   for line in data:
      if '#' in line:
         continue 
      else:
         nodes = line.split()
         graph.addEdge(int(nodes[0]), int(nodes[1]))

   return graph


if __name__ == '__main__':
   fname = sys.argv[1]
   fp = open(fname, 'r')

   start_graph = time.time()

   if len(sys.argv) > 2:
      if sys.argv[2] == '-d' or '--directed':
         graph = getDataDirected(fp)
   else:
      graph = getData(fp)

   end_graph = time.time()

   start_res = time.time()
   i, results = graph.getPageRank()
   end_res = time.time()

   #graph.printGraph()

   print "Read time: %f" % (end_graph - start_graph)
   print "Processing time: %f" % (end_res - start_res)
   print "Iterations until convergance: %i" % i
   print

   print "pageRanks:"
   i = 1
   for k, v in results:
      print "%i  obj: %s with PageRank: %f indegree: %d outdegree: %d total: %d" % (i, k, v, len(graph.getSources(k)), graph.getDegree(k), len(graph.getSources(k)) + graph.getDegree(k))
      i += 1




         
