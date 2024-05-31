from collections import deque
import time


class Graphe:
  """
    Classe représentant un graphe non orienté.
    """

  def __init__(self):
    """
        Initialise un graphe vide.
        """
    self.graphe = {}

  def ajouterArete(self, sommet_dep, sommet_arr):
    """
        Ajoute une arête entre deux sommets.
        """
    if sommet_dep in self.graphe:
      self.graphe[sommet_dep].append(sommet_arr)
    else:
      self.graphe[sommet_dep] = [sommet_arr]

  def obtenirVoisins(self, sommet):
    """
        Retourne une liste des voisins d'un sommet.
        """
    return self.graphe.get(sommet, [])


def checkReine(plateau, ligne, colonne):
  """
    Vérifie s'il est possible de placer une reine à une position donnée sur un plateau.
    
    Retourne True si la reine peut être placée à cet emplacement, False sinon.
    """
  # Vérifie la colonne
  for i in range(ligne):
    if plateau[i] == colonne:
      return False
    # Vérifie les diagonales
    if abs(plateau[i] - colonne) == ligne - i:
      return False
  return True


def bfs(n, colonne_premiere_reine):
  """
    Effectue un parcours en largeur d'abord pour trouver les 
    configurations valides du problème des N reines.
    
    Retourne une liste de toutes les configurations valides 
    pour le placement des reines.
    """
  resultat = []
  file = deque([(1, [colonne_premiere_reine])])
  graphe = Graphe()
  for i in range(n):
    for j in range(n):
      if i != j:
        graphe.ajouterArete(i, j)

  while file:
    ligne, plateau = file.popleft()
    if ligne == n:
      resultat.append(plateau)
    else:
      for colonne in range(n):
        if checkReine(plateau, ligne, colonne):
          nouveau_plateau = plateau + [colonne]
          file.append((ligne + 1, nouveau_plateau))
  return resultat


def afficherPlateau(plateau):
  """
    Affiche le plateau avec les reines placées.
    """
  n = len(plateau)
  for i in range(n):
    ligne_str = ""
    for j in range(n):
      if j == plateau[i]:
        ligne_str += " Q"
      else:
        ligne_str += " ."
    print(ligne_str)


n = 6
colonne_premiere_reine = int(input("Entrez la colonne de la première reine : "))
# Enregistrement du temps de début
start_time = time.perf_counter()
solutions = bfs(n, colonne_premiere_reine)
# Enregistrement du temps de fin
end_time = time.perf_counter()
# Calcul du temps total d'exécution en millisecondes
execution_time_ms = (end_time - start_time)

# Affichage des solutions
print(f"Nombre de solutions pour {n} reines : {len(solutions)}")
for i, sol in enumerate(solutions):
  print(f"Solution {i + 1}:")
  afficherPlateau(sol)
  print()
# Affichage du temps d'exécution en millisecondes
print(f"Temps d'exécution : {execution_time_ms} secondes")
