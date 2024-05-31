import sys
assert sys.version_info >= (3, 10), "Ce script doit être lancé sous Python 3.10 ou une version postérieure"

import tkinter as tk
import tkinter.simpledialog as sd
import time

import huitreines


class Window(tk.Tk):
    def __init__(self, size: int = 4, colonne_debut: int = 0, ligne_debut: int = 0) -> None:
        super().__init__()

        temps_debut: float = time.perf_counter()
        self.board: list[list[list[int]]] = huitreines.HuitReines(size, colonne_debut, ligne_debut).liste_solutions
        temps_fin: float = time.perf_counter()
        # DEBUG
        print(f"Temps de recherche : {temps_fin - temps_debut:.6f} secondes.")

        self.title(f"SAE202 Problème des {size} reines")

        self.rows: int = size
        self.cols: int = size
        self.cell_size: int = 25  # Taille de chaque cellule

        self.solution_actuelle_label: tk.Label = tk.Label(self)
        self.number_solution_label: tk.Label = tk.Label(self)
        self.change_solution_btn: tk.Button = tk.Button(self)
        self.canvas: tk.Canvas = tk.Canvas(self)
        self.legend1: tk.Label = tk.Label(self)
        self.legend2: tk.Label = tk.Label(self)
        self.legend3: tk.Label = tk.Label(self)

        # Affichage du tableau
        self.draw_board()

        self.mainloop()

    def draw_board(self, solution_num: int = 1) -> None:
        # Solution actuelle
        self.solution_actuelle_label = tk.Label(self, text=f"SOLUTION N°{solution_num}", font=("Arial", 16))
        self.solution_actuelle_label.pack(pady=10)
        # Nombre de solutions
        self.number_solution_label = tk.Label(self, text=f"Il y a {len(self.board)} solution(s)")
        self.number_solution_label.pack(pady=5)

        # Changer de solution
        self.change_solution_btn = tk.Button(self, text="Changer de solution", command=self.change_solution, bg="darkgray")
        self.change_solution_btn.pack(pady=5)

        # Création du canvas
        self.canvas = tk.Canvas(self, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
        self.canvas.pack()

        row: int
        col: int
        for row in range(self.rows):
            for col in range(self.cols):
                x1: int = col * self.cell_size
                y1: int = row * self.cell_size
                x2: int = x1 + self.cell_size
                y2: int = y1 + self.cell_size
                color: str = "white"  # Par défaut, couleur blanche pour 0

                if self.board[solution_num-1][row][col] == 1:
                    color = "green"
                elif self.board[solution_num-1][row][col] == -1:
                    color = "red"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

        self.legend1 = tk.Label(self, text="Carré rouge = Case menacée")
        self.legend1.pack(anchor="w")

        self.legend2 = tk.Label(self, text="Carré vert = Case possédant une reine")
        self.legend2.pack(anchor="w")

        self.legend3 = tk.Label(self, text="Carré blanc = Case vide et non menacée")
        self.legend3.pack(anchor="w")

    def change_solution(self):
        solution_num: int = sd.askinteger("Changer de solution", f"Entrer un entier entre 1 et {len(self.board)}", initialvalue=1, minvalue=1, maxvalue=len(self.board))
        if solution_num is None:  # Si l'utilisateur a appuyé sur 'annuler'
            return
        self.solution_actuelle_label.destroy()
        self.number_solution_label.destroy()
        self.change_solution_btn.destroy()
        self.canvas.destroy()
        self.legend1.destroy()
        self.legend2.destroy()
        self.legend3.destroy()
        self.draw_board(solution_num)


if __name__ == '__main__':
    grid_size: int = sd.askinteger("Taille de la grille", "Veuillez entrer la taille de la grille.\n(Doit être supérieur à 4)", minvalue=4, initialvalue=4)
    if grid_size is None:  # Si l'utilisateur a appuyé sur 'annuler'
        exit(0)

    start_column: int = sd.askinteger("Colonne de début", f"Veuillez entrer la colonne à laquelle le programme de résolution commencera.\nEntre 0 et {grid_size-1}", minvalue=0, maxvalue=grid_size-1, initialvalue=0)
    start_row: int = sd.askinteger("Ligne de début", f"Veuillez entrer la ligne à laquelle le programme de résolution commencera.\nEntre 0 et {grid_size-1}", minvalue=0, maxvalue=grid_size-1, initialvalue=0)
    if start_column is None or start_row is None:  # Si l'utilisateur a appuyé sur 'annuler'
        exit(0)

    window: Window = Window(grid_size, start_column, start_row)
