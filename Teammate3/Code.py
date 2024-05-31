from structures_lineaires import File, Pile
from time import perf_counter

############################################# Classe Noeud #################################

class Noeud:
    def __init__(self, positions, n = 6): # échiquier de taille 8 par défaut
        self.positions = positions
        self.n = n
        self.fils = []
        self.profondeur = 0

    def __str__(self):
        nb_caract = 4*self.n + 3
        ligne_vide =  "  " + (" " + "\u2015"*3)*self.n +"\n" + "  " + "|   " *self.n + "|\n"
        r = ""
        j = 0
        for i in range(self.n):
            a = list(ligne_vide)
            str_j = str(j) + (2-len(str(j)))*" "
            if i < len(self.positions):
                a[nb_caract + 4*(self.positions[i]+1)] = "D"
            
            a[nb_caract], a[nb_caract +1] = str_j[0], str_j[1]
            r = "".join(a) + r
            j+=1
        
        derniere = "    " + "".join([str(j) + (4-len(str(j)))*" " for j in range(self.n)])
        return  r + "  " + (" " + "\u2015"*3)*self.n + "\n" + derniere
    
    def disponible(self):
        d = []
        interdit = []
        
        taille_p = len(self.positions)
        #calcul des valeurs interdite
        for i in range(taille_p):
            interdit += interdites(i, self.positions[i], taille_p, self.n)
        #remplissage de la liste "d" avec toute les valeurs de 0 a n-1 sans les valeurs interdite
        for x in range(self.n):
            if x not in interdit:
                d.append(x)
        return d
    
    def creer_fils(self):
        for num_case in self.disponible():
            fils = Noeud(self.positions + [num_case], self.n)
            self.fils.append(fils)
            fils.profondeur = self.profondeur+1

def interdites(i, pos_i, j, n) :
    '''renvoie les index des cases interdites pour la ligne d'index j > i, lorsqu'une dame est sur la ligne d'index i en case d'index pos_i'''
    #interdiction diagonales
    x = (pos_i-(j-i)) #diagonale gauche
    y = pos_i         #colonne
    z = (pos_i+(j-i)) #diagonale droite
    liste = []
    if(j < 8 and j>i):
        if(x>=0):
            liste.append(x)
        liste.append(y)
        if(z<8):
            liste.append(z)
    return liste



############################################ Parcours en largeur #############################

racine = Noeud([], 6) # création de la racine
temps_debut = perf_counter()
f = File()
f.enfiler(racine)
nb_solutions = 0
n = racine.n
while not f.est_vide():
    tete = f.defiler()
    if tete.profondeur <= racine.n:
        tete.creer_fils()
        for fils in tete.fils:
            f.enfiler(fils)
            if tete.profondeur == n-1: # c'est une feuille car n dames ont ete placees
                nb_solutions += 1
                # print("Solution N°", nb_solutions, ":\n", fils, "\n")

print("Il y a ", nb_solutions,"solutions possibles.")


############################### Parcours en profondeur (backtracking) #######################

# racine = Noeud([], 6)# création de la racine
#
# temps_debut = perf_counter()
# p = Pile()
# p.empiler(racine)
# nb_solutions = 0
# n = racine.n
# while not p.est_vide():
#     sommet = p.depiler()
#     if sommet.profondeur <= racine.n:
#         sommet.creer_fils()
#         for fils in reversed(sommet.fils):
#             p.empiler(fils)
#             if sommet.profondeur == n-1: # c'est une feuille car n dames ont ete placees
#                 nb_solutions += 1
                # print("Solution N°", nb_solutions, ":\n", fils, "\n")
temps_fin = perf_counter()
print(f"Temps de recherche : {temps_fin - temps_debut:.6f} secondes.")

            
print("Il y a ", nb_solutions,"solutions possibles.")