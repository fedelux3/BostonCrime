
class Node :
   def __init__(self, parent1, parent2, value, children):
      self.parent1 = parent1
      self.parent2 = parent2
      self.value = value
      self.children = []
   
   def insertParent1(self, parent1):
      self.parent1 = parent1
   
   def insertParent2(self, parent2):
      if (self.value == parent2.value):
         self.parent2 = parent2
      else:
         print("Error nel value del parent2")
   #end insertParent2
   
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
   
   #assumo che types sia una lista con TUTTI i diversi tipi (NO SEQUENZE)
   def __init__(self, types=None) :
      self.root = Node(None, None, None, None);
      for elem in types:
         n = Node(self.root,self.root,elem,None)
         #print(elem)
         self.root.insertChild(n)
   
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
   
   def insertNode(self, seq):
      #inserisco l'ultimo elemento della seq scendendo nell'albero rispettandola
      currNode = self.root
      currEl = 0
      childCurr = currNode.children
      found = 1 #booleano per vedere se ho trovato
      #passo tutta la sequenza fino all'ultimo elemento
      for i in range(len(seq)-1):
         found = 0
         for child in childCurr:
            if child.value == seq[i]:
               currNode = child
               found = 1
               break
         if not found :
            print("!!!non trovato!!! " + seq[i])
         childCurr = currNode.children
         currEl = i
         if  childCurr is None :
            print("trovato child none")
            break
      if currEl >= len(seq):
         print("Errore nel indice currEl")
      #print("sto inserendo: " + seq[currEl+1] + " in: " + str(currNode))
      p2 = self.newParent2(currNode, seq[currEl+1])
      n = Node(currNode, p2, seq[currEl+1], None)
      currNode.insertChild(n) #aggiungo figlio nuovo nodo
   #end insertNode
   
  
   
   #cerca una sequenza data in input e la restituisce
   def searchSeq(self, seq):
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
            print("sequenza non trovata")
            return
      return currNode
   #end serchSeq
   
   def __str__(self):
      s = str(self.root) + "\n"
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
   s = t.searchSeq(["Homicide", "Robbery"])
   print(s)
#end testInsert
   
#in questo modo controllo se sto eseguendo direttamente questo script
if __name__ == "__main__":
   print("Testing: ")
   main()