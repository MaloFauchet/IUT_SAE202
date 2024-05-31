from time import perf_counter

n = 6  # Taille de l'échiquier


class Graphe:
    def __init__(self, positions, n):
        self.positions = positions  # Liste des positions des reines
        self.n = n  # Taille de l'échiquier
        self.profondeur = len(positions)  # Profondeur du nœud dans l'arbre

    def c_disponible(self):
        # Méthode pour trouver les colonnes disponibles pour placer une nouvelle reine
        interdit = set()

        for i, pos_i in enumerate(self.positions):
            interdit |= self.c_interdites(i, pos_i)  # Calcul des colonnes interdites

        return [x for x in range(self.n) if x not in interdit]  # Colonnes disponibles

    def creer_fils(self):
        # Méthode pour créer les fils du nœud actuel en explorant les colonnes disponibles
        for num_case in self.c_disponible():
            yield Graphe(self.positions + [num_case], self.n)  # Création d'un nouveau nœud fils

    def c_interdites(self, i, pos_i):
        # Méthode pour trouver les colonnes interdites pour placer une reine dans une ligne donnée
        x = (pos_i - (self.profondeur - i))
        y = pos_i
        z = (pos_i + (self.profondeur - i))
        return {x, y, z}  # Retourne un ensemble des colonnes interdites pour la reine


def dfs_trouver_solutions(racine):
    # Fonction de recherche DFS pour trouver toutes les solutions possibles
    p = []
    p.append(racine)  # Ajout du nœud racine à la pile
    solutions = []  # Liste pour stocker les solutions trouvées

    while p:  # Tant que la pile n'est pas vide
        sommet = p.pop()  # Retire un nœud de la pile
        if sommet.profondeur == sommet.n:  # Si le nœud représente une solution complète
            solutions.append(sommet.positions)  # Ajout de la solution à la liste
        else:  # Sinon, explorer les fils du nœud
            for fils in sommet.creer_fils():  # Pour chaque fils possible
                p.append(fils)  # Ajout du fils à la pile

    return solutions  # Retourne la liste des solutions trouvées


def afficher_echiquier(solution):
    # Fonction pour afficher l'échiquier avec les reines placées
    echiquier = [['.' for _ in range(n)] for _ in range(n)]  # Crée un échiquier vide

    # Place les reines sur l'échiquier
    for i, pos in enumerate(solution):
        echiquier[i][pos] = 'R'  # 'R' représente une reine

    # Affiche l'échiquier
    print("Échiquier :")
    for row in echiquier:
        print(' '.join(row))
    print("\n")


def filtrer_solutions(colonne):
    # Fonction pour filtrer les solutions en fonction de la colonne de la première reine
    racine = Graphe([colonne], n)  # Crée le nœud racine avec la colonne spécifiée
    solutions = dfs_trouver_solutions(racine)  # Trouve toutes les solutions possibles

    # Filtrer les solutions pour ne garder que celles avec la première reine dans la colonne spécifiée
    # solutions_filtrees = []
    # for solution in solutions:
    #     if solution[0] == colonne:
    #         solutions_filtrees.append(solution)

    return solutions  # Retourne les solutions filtrées


colonne = int(input(f"Entrez la colonne où se trouve la première reine (0 à {n-1}) : "))

temps_debut = perf_counter()
solutions = filtrer_solutions(colonne)  # Trouve les solutions pour la colonne spécifiée
temps_fin = perf_counter()
print(f"Temps de recherche : {temps_fin - temps_debut:.6f} secondes.")
nb_solutions = len(solutions)  # Nombre de solutions trouvées

# Affiche le nombre de solutions et chaque solution
print("Il y a", nb_solutions, "solutions possibles avec la première reine placée en colonne", colonne, "et ligne 1")
# for i, solution in enumerate(solutions, 1):
#     print("Solution", i, ":")
#     afficher_echiquier(solution)  # Affiche l'échiquier pour chaque solution
