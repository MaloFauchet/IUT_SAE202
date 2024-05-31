from collections import deque
class Pile(deque):
    def __init__(self):
        super().__init__()
 
    def est_vide(self):
        '''renvoie True si la pile est vide'''
        return len(self) == 0
    
    def empiler(self, element):
        '''empile element dans la pile'''
        self.append(element)
 
    def depiler(self):
        '''retire le sommet de pile et renvoie sa valeur'''
        if not self.est_vide():
            return self.pop() # retire l'élément d'index -1
        else:
            print("la pile est vide!")
            


class File(deque):
    def __init__(self):
        super().__init__()
 
    def est_vide(self):
        '''renvoie True si la pile est vide'''
        return len(self) == 0
    
    def enfiler(self, element):
        '''empile element dans la pile'''
        self.append(element)
 
    def defiler(self):
        '''retire le sommet de pile et renvoie sa valeur'''
        if not self.est_vide():
            return self.popleft() # retire l'élément d'index -1
        else:
            print("impossible de défiler : la file est vide!")
    
      
