# coding: utf-8
"""
Une classe Python pour creer et manipuler des graphes
"""


class Noeud:
    def __init__(self) -> None:
        self.est_reine: bool = False
        self.aretes: ListeSommet = []


# Annotations de type
Sommet = tuple[int, int]
ListeSommet = list[Sommet]
GrapheReine = dict[Sommet, Noeud]


class Graphe(object):

    def __init__(self, graphe_dict: GrapheReine = None) -> None:
        """
        initialise un objet graphe.
        Si aucun dictionnaire n'est
        créé ou donné, on en utilisera un
        vide
        """
        if graphe_dict is None:
            graphe_dict: GrapheReine = dict()
        self.graphe_dict: GrapheReine = graphe_dict

    def aretes(self, sommet: Sommet) -> ListeSommet:
        """ retourne une liste de toutes les aretes d'un sommet"""
        return self.graphe_dict[sommet].aretes

    def all_sommets(self) -> ListeSommet:
        """ retourne tous les sommets du graphe """
        return list(self.graphe_dict.keys())

    def all_aretes(self) -> list[set[Sommet]]:
        """ retourne toutes les aretes du graphe """
        return self.__list_aretes()

    def add_sommet(self, sommet: Sommet) -> None:
        """
        Si le "sommet" n'set pas déjà présent
        dans le graphe, on rajoute au dictionnaire
        une clé "sommet" avec une liste vide pour valeur.
        Sinon on ne fait rien.
        """
        if sommet not in self.graphe_dict:
            self.graphe_dict[sommet] = Noeud()

    def add_arete(self, arete: ListeSommet) -> None:
        """ l'arete est de  type set, tuple ou list;
            Entre deux sommets il peut y avoir plus
        d'une arete (multi-graphe)
        """
        arete1: Sommet
        arete2: Sommet
        arete1, arete2 = tuple(arete)

        x: Sommet
        y: Sommet
        for x, y in [(arete1, arete2), (arete2, arete1)]:
            if x in self.graphe_dict:
                self.graphe_dict[x].aretes.append(y)

    def remove_arete(self, arete: Sommet) -> None:
        """
        Retire l'arête spécifiée du graphe.
        :param arete: L'arête à retirer, représentée sous forme de tuple, set ou liste.
        """
        sommet: Sommet
        for sommet in self.graphe_dict.keys():
            if sommet == arete:
                self.graphe_dict[sommet].aretes = []
            elif arete in self.graphe_dict[sommet].aretes:
                self.graphe_dict[sommet].aretes.remove(arete)

    def __list_aretes(self) -> list[set[Sommet]]:
        """ Methode privée pour récupérer les aretes.
        Une arete est un ensemble (set)
        avec un (boucle) ou deux sommets.
        """
        aretes: list[set[Sommet]] = []
        sommet: Sommet
        voisin: Sommet
        for sommet in self.graphe_dict:
            for voisin in self.graphe_dict[sommet].aretes:
                if ({voisin, sommet}) not in aretes:
                    aretes.append({sommet, voisin})
        return aretes

    def trouve_chaine(self, sommet_dep: Sommet, sommet_arr: Sommet, chain: ListeSommet | None = None) -> None | ListeSommet:
        """ Trouver un chemin élémentaire de sommet_dep à sommet_arr
            dans le graphe """
        tmp_graphe: GrapheReine = self.graphe_dict
        if not ({sommet_dep, sommet_arr}.issubset(tmp_graphe)):
            return None

        if chain is None:
            chain = []

        chain = chain + [sommet_dep]
        if sommet_dep == sommet_arr:
            return chain

        sommet: Sommet
        for sommet in tmp_graphe[sommet_dep].aretes:
            if sommet not in chain:
                ext_chain: ListeSommet = self.trouve_chaine(sommet, sommet_arr, chain)
                if ext_chain:
                    return ext_chain
        return None

    def trouve_tous_chaines(self, sommet_dep: Sommet, sommet_arr: Sommet, chain: ListeSommet | None = None) -> ListeSommet:
        """ Trouver tous les chemins élémentaires de sommet_dep à
            sommet_arr dans le graphe """
        if chain is None:
            chain = []

        tmp_graphe: GrapheReine = self.graphe_dict
        if not ({sommet_dep, sommet_arr}.issubset(tmp_graphe)):
            return []

        chain = chain + [sommet_dep]
        if sommet_dep == sommet_arr:
            return chain

        if sommet_dep not in tmp_graphe:
            return []

        chains = []

        sommet: Sommet
        for sommet in tmp_graphe[sommet_dep].aretes:
            if sommet not in chain:
                ext_chains: ListeSommet = self.trouve_tous_chaines(sommet, sommet_arr, chain)
                c: Sommet
                for c in ext_chains:
                    chains.append(c)
        return chains

    def __iter__(self) -> iter:
        self._iter_obj: iter = iter(self.graphe_dict)
        return self._iter_obj

    def __next__(self) -> Sommet:
        """ Pour itérer sur les sommets du graphe """
        return next(self._iter_obj)

    def __str__(self) -> str:
        res: str = "sommets: "

        k: Sommet
        for k in self.graphe_dict.keys():
            res += str(k) + " "
        res += "\naretes: "

        aretes: set[Sommet]
        for arete in self.__list_aretes():
            res += str(arete) + " "
        return res


class Graphe2(Graphe):

    def sommet_degre(self, sommet: Sommet) -> int:
        """ renvoie le degre du sommet """
        degre: int = len(self.graphe_dict[sommet].aretes)

        sommet: Sommet
        if sommet in self.graphe_dict[sommet].aretes:
            degre += 1
        return degre

    def trouve_sommet_isole(self) -> ListeSommet:
        """ renvoie la liste des sommets isoles """
        graphe: GrapheReine = self.graphe_dict
        isoles: ListeSommet = []

        sommet: Sommet
        for sommet in graphe:
            if not graphe[sommet].aretes:
                isoles += [sommet]
        return isoles

    def Delta(self) -> int:
        """ le degre maximum  """
        max_degre: int = 0

        sommet: Sommet
        for sommet in self.graphe_dict:
            sommet_degre: int = self.sommet_degre(sommet)
            if sommet_degre > max_degre:
                max_degre = sommet_degre
        return max_degre

    def list_degres(self) -> list[int]:
        """
        calcule tous les degres et renvoie un
        tuple de degres decroissant
        """
        degres: list[int] = []

        sommet: Sommet
        for sommet in self.graphe_dict:
            degres.append(self.sommet_degre(sommet))
        degres.sort(reverse=True)
        return degres
