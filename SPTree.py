
class Node :
   def __init__(self, parent1, parent2, seq, level):
      self.parent1 = parent1
      self.parent2 = parent2
      self.seq = seq
      self.level = level
      
   def __str__(self):
      return '(' + str(self.parent1) + ' , ' + str(self.parent2) + ' , ' + str(self.seq) + ' , ' + str(self.level) + ')'

#end Nodo
      
class SPTree :
   
#   def __init__(self):
#      self.root = None
      
   def __init__(self, types=None) :
      self.nodes = []
      self.root = []
      self.nEl = 0;
      i = 0
      for elem in types:
         n = Node("A","B",elem,i)
         self.nodes.insert(i, n)
         self.nEl = self.nEl+1
   
   def __str__(self):
      s = "("
      for i in range(0,self.nEl):
         s += str(self.nodes[i]) + " "
      s += ")"
      return s;
#end SPTree
      
#main
def main(): 
   #n = Node('A', 'B', ["Larceny"], 1);
   #print(str(n))
   t = SPTree(["Larceny", "Robbery"])
   print(str(t))
   
#in questo modo controllo se sto eseguendo direttamente questo script
if __name__ == "__main__":
   print("Testing: ")
   main()