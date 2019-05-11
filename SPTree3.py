
class Node :
   def __init__(self, parent1, parent2, value, setIns, children):
      self.parent1 = parent1
      self.parent2 = parent2
      self.value = value
      self.set = setIns
      self.children = []
   
   def insertParent1(self, parent1):
      self.parent1 = parent1
   
   def insertParent2(self, parent2):
      if (self.value == parent2.value):
         self.parent2 = parent2
      else:
         print("Error nel value del parent2")
   #end insertParent2
   
   def insertSet(self, setIns):
      self.set = setIns
      
   def insertChild(self, newChild):
      self.children.append(newChild)
      
   def __str__(self):
#      s = '(' + str(self.parent1) + ', ' + str(self.parent2) + ', ' + str(self.value) + ', '
#      s += "[ "
#      for el in self.children:
#         s += el.value + " "
#      s += "])"
      #METODO COMPATTO
      s = "(" + str(self.value)
      for el in self.children:
         s+= str(el)
      s += ")"
      return s
#end Nodo
      
class SPTree :
   
   #genero la root dell'albero e il suo attributo di candidates validi
   def __init__(self) :
      self.root = Node(None, None, None, None, None);
   
   def newParent2(self, currNode, newValue):
      headNode = currNode.parent2
      par2 = None
      for child in headNode.children:
         if child.value == newValue:
            par2 = child
            break
      if par2 is None:
         print("Error parent2")
      
      return par2
   #end newParent2
   
   #input ho una lista che rappresenta la mia sequenza
   #input il set relativo a questa seuenza
   #inserisce il nodo definito dall'ultimo elemento della sequenza (lista) in input
   def insertNode(self, seq, setNode):
      #inserisco l'ultimo elemento della seq scendendo nell'albero rispettandola
      currNode = self.root
      #se sto inserendo nella root
      if isinstance(seq, str) :
         n = Node(self.root,self.root,seq,setNode,None)
         currNode.insertChild(n)
         return

      currNode = self.searchNode(seq[:len(seq)-1])
      if currNode is None:
         print("error sequenza non inseribile" + str(seq))
         return
      p2 = self.newParent2(currNode, seq[len(seq)-1])
      n = Node(currNode, p2, seq[len(seq)-1], setNode, None)
      currNode.insertChild(n) #aggiungo figlio nuovo nodo
   #end insertNode
   
   #deleteNode
   #elimina (taglia) il nodo finale della sequenza data in input
   def deleteNode(self, seq):
      n = self.searchNode(seq)
      if n is None:
         print("error delete node")
         return
      tipo = seq[len(seq)-1]
      for child in n.parent1.children:
         if child.value == tipo:
            n.parent1.children.remove(child)
            print("eliminato ramo di: " + str(seq))
            return
      print("non eliminato: " + str(seq))
   #end deleteNode
   
   #cerca una sequenza data in input
   #restituisce il true o false se esiste o meno
   def searchSeq(self, seq):
      currNode = self.root
      string = []
      for i in range(len(seq)):
         currEl = seq[i]
         found = False
         if currNode.children is None:
            return False
         
         for child in currNode.children:
            if child.value == currEl:
               currNode = child
               string.append(child.value)
               found = True
               break
         if not found :
            #print("sequenza non trovata: " + str(seq) )
            return False
      return found
   #end serchSeq
   
   #cerca una sequenza data in input (lista di tipi)
   #restituisce il nodo della fine della sequenza
   def searchNode(self, seq):
      currNode = self.root
      string = []
      for i in range(len(seq)):
         currEl = seq[i]
         found = 0
         for child in currNode.children:
            if child.value == currEl:
               currNode = child
               string.append(child.value)
               found = 1
               break
         if not found :
            print("sequenza non trovata " + str(seq))
            return None
      return currNode
   #end serchNode

      
   def __str__(self):
      s = str(self.root) + "\n"
      #s += "Sequenze inserite: " + str(self.candidates) + "\n"
      return s
#end SPTree
      
#main
def main(): 
   
   #testInsert()
   testInsertComplete()
#end main

#esempio del paper
def testInsertComplete():
   t = SPTree(["A", "B", "C", "D", "E", "F"])
   #print(t)
   seq1 = ["A", "B"]
   seq2 = ["B", "C"]
   seq3 = ["B", "D"]
   seq4 = ["C", "E"]
   seq5 = ["C", "F"]
   seq21 = ["A", "B", "C"]
   seq22 = ["A", "B", "D"]
   seq23 = ["B", "C", "E"]
   seq24 = ["B", "C", "F"]
   seq31 = ["A", "B", "C", "E"]
   seq32 = ["A", "B", "C", "F"]
   
   t.insertNode(seq1)
   t.insertNode(seq2)
   t.insertNode(seq3)
   t.insertNode(seq4)
   t.insertNode(seq5)
   t.insertNode(seq21)
   t.insertNode(seq22)
   t.insertNode(seq23)
   t.insertNode(seq24)
   t.insertNode(seq31)
   t.insertNode(seq32)
      
   print(t)
   
   s = t.searchNode(["A", "B", "C"])
   print("sequenza ABC: " + str(s))
#end testInsertComplete

def testInsert():
   t = SPTree(["Larceny", "Robbery", "Homicide"])
   print(t)
   #aggiungo una nuova sequenza
   seq = ["Larceny", "Homicide"]
   seq2 = ["Larceny", "Robbery"]
   seq3 = ["Larceny", "Robbery", "Homicide"]
   seq4 = ["Homicide", "Robbery"]
   t.insertNode(seq)
   f = t.root.children[0]
   print("f1: " + str(f))
   t.insertNode(seq2)
   f = t.root.children[0]
   print("f2: " + str(f))
   t.insertNode(seq3)
   f2 = t.root.children[0].children[1]
   print("f3: " + str(f2))
   t.insertNode(seq4)
   s = t.searchNode(["Homicide", "Robbery"])
   print(s)
#end testInsert

def testSet():
   t = SPTree()
   
   #inserisco i sets
   a = "A"
   sA = set()
   sA.add("10")
   b = "B"
   sB = set()
   sB.add('IT01R003')
   c = "C"
   sC = set()
   sC.add('30')
   t.insertNode(a, sA)
   t.insertNode(b, sB)
   t.insertNode(c, sC)
   t.insertNode("D", set())
   
   t.insertNode(["A", "B"], set())
   t.insertNode(["B", "C"], set())
   t.insertNode(["A", "B", "C"], set())
   t.insertNode(["B", "D"], set())
   t.insertNode(["A","B","D"], set())
   
   print("prima \n" + str(t))
   
   ns = t.searchNode(["A", "B"])
   ns.parent1.children.remove(ns)
   t.refreshCandidates()
   print("dopo \n" + str(t))
   
   
#in questo modo controllo se sto eseguendo direttamente questo script
if __name__ == "__main__":
   print("Testing: ")
   testSet()