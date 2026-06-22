from PyQt6.QtWidgets import QTableWidgetItem
from database import get_all_recette

def charger_table_recette(self):

    donnees = get_all_recette()

    self.tableRecette.setRowCount(len(donnees))

    for ligne, recette in enumerate(donnees):

        self.tableRecette.setItem(
            ligne, 0,
            QTableWidgetItem(str(recette[0]))
        )

        self.tableRecette.setItem(
            ligne, 1,
            QTableWidgetItem(str(recette[1]))
        )

        self.tableRecette.setItem(
            ligne, 2,
            QTableWidgetItem(str(recette[2]))
        )

        self.tableRecette.setItem(
            ligne, 3,
            QTableWidgetItem(str(recette[3]))
        )