import time

import my_graph as mg


class HuitReines:
    def __init__(self, n: int, colonne_debut: int = 0, ligne_debut: int = 0) -> None:
        self.n: int = n  # Taille du plateau
        self.colonne_debut: int = colonne_debut
        self.ligne_debut: int = ligne_debut

        self.graphe: mg.Graphe2 = mg.Graphe2()

        self.liste_solutions: list[list[list[int]]] = []

        self.initGraphe()
        self.backtracking(colonne_actuelle=colonne_debut)

    def initGraphe(self) -> None:
        """Initialise les sommets du graphes avec pour chaque sommet, ses coordonees"""
        i: int
        j: int
        for i in range(self.n):
            for j in range(self.n):
                self.graphe.add_sommet((i, j))

    def calculerMenaces(self, pos: mg.Sommet) -> None:
        """
        Ajoute des aretes de pos vers chaque sommet menace par pos
        :param pos: la position d'un sommet
        """
        x: int
        y: int
        x, y = pos

        self.calculerMenacesColonne(x, y)
        self.calculerMenacesLigne(x, y)
        self.calculerMenacesDiagonale(x, y)

    def calculerMenacesColonne(self, x: int, y: int) -> None:
        """
        Ajoute une aretes pour chaque sommet de la colonne menace par pos
        :param x: numero de la ligne de la reine
        :param y: numero de la colonne de la reine
        """
        i: int
        for i in range(self.n):
            if i != x:
                self.graphe.add_arete([(x, y), (i, y)])

    def calculerMenacesLigne(self, x: int, y: int) -> None:
        i: int
        for i in range(self.n):
            if i != y:
                self.graphe.add_arete([(x, y), (x, i)])

    def calculerMenacesDiagonale(self, i: int, j: int) -> None:
        # Marquer les diagonales ascendantes et descendantes
        self.calculeMenaceDiagHautDroit(i, j)  # diagonale ascendante
        self.calculeMenaceDiagBasDroit(i, j)  # diagonale descendante
        self.calculeMenaceDiagHautGauche(i, j)
        self.calculeMenaceDiagBasGauche(i, j)

    def calculeMenaceDiagHautDroit(self, x: int, y: int) -> None:
        old_x: int
        old_y: int
        old_x, old_y = x, y
        x -= 1
        y += 1

        while x >= 0 and y < self.n:
            self.graphe.add_arete([(old_x, old_y), (x, y)])
            x -= 1
            y += 1

    # Méthode pour marquer une diagonale descendante à partir de la position (x, y)
    def calculeMenaceDiagBasDroit(self, x: int, y: int) -> None:
        old_x: int
        old_y: int
        old_x, old_y = x, y
        x += 1
        y += 1

        while x < self.n and y < self.n:
            self.graphe.add_arete([(old_x, old_y), (x, y)])
            x += 1
            y += 1

    def calculeMenaceDiagHautGauche(self, x: int, y: int) -> None:
        old_x: int
        old_y: int
        old_x, old_y = x, y
        x -= 1
        y -= 1

        while x >= 0 and y >= 0:
            self.graphe.add_arete([(old_x, old_y), (x, y)])
            x -= 1
            y -= 1

    # Méthode pour marquer une diagonale descendante à partir de la position (x, y)
    def calculeMenaceDiagBasGauche(self, x: int, y: int) -> None:
        old_x: int
        old_y: int
        old_x, old_y = x, y
        x += 1
        y -= 1

        while x < self.n and y >= 0:
            self.graphe.add_arete([(old_x, old_y), (x, y)])
            x += 1
            y -= 1

    def backtracking(self, colonne_actuelle: int = 0) -> bool:
        # Si toutes les colonnes ont été parcourues, le placement des reines est valide
        if colonne_actuelle == self.n:
            self.liste_solutions.append(self.getPlateau())
            return False

        debut: int = 0
        # commence la boucle à partir de la ligne de début choisi si colonne actuelle = colonne de debut
        if colonne_actuelle == self.colonne_debut:
            debut = self.ligne_debut

        # Parcours les lignes de la colonne actuelle
        ligne: int
        for ligne in range(debut, self.n):
            # Vérifie si la reine peut être placée dans cette case
            if self.graphe.sommet_degre((ligne, colonne_actuelle)) == 0:
                # Place la reine dans cette case
                self.calculerMenaces((ligne, colonne_actuelle))
                self.graphe.graphe_dict[(ligne, colonne_actuelle)].est_reine = True

                # Appelle récursivement le backtracking pour la colonne suivante
                if self.backtracking(colonne_actuelle + 1):
                    return True

                # Sinon si aucun placement valide n'a été trouvé dans les colonnes suivantes,
                # retire la reine de cette case et explorer d'autres possibilités
                self.graphe.remove_arete((ligne, colonne_actuelle))
                self.graphe.graphe_dict[(ligne, colonne_actuelle)].est_reine = False

        # Si aucun placement valide n'a été trouvé pour cette colonne, retourne False
        return False

    def __str__(self) -> str:
        """Affiche les sommets du graphe de facon lisible"""
        result: str = f""
        tmp: int = 0

        sommet: mg.Sommet
        for sommet in self.graphe.all_sommets():
            if sommet[0] != tmp:
                result += f"\n {sommet} "
                tmp = sommet[0]
            else:
                result += f" {sommet} "
        return result

    def getPlateau(self) -> list[list[int]]:
        plateau: list[list[int]] = [[0 for _ in range(self.n)] for _ in range(self.n)]

        sommet: mg.Sommet
        for sommet, _ in self.graphe.graphe_dict.items():
            if isinstance(sommet, tuple):
                if self.graphe.graphe_dict[sommet].est_reine:
                    plateau[sommet[0]][sommet[1]] = 1
                elif self.graphe.sommet_degre(sommet) > 0:
                    plateau[sommet[0]][sommet[1]] = -1
        return plateau


if __name__ == '__main__':
    temps_debut: float = time.perf_counter()
    a = HuitReines(6)
    temps_fin: float = time.perf_counter()
    # DEBUG
    print(f"Temps de recherche : {temps_fin - temps_debut:.6f} secondes.")
