from PyQt6.QtWidgets import QTableWidgetItem

from database.queries import get_all_recette, get_all_depense, get_all_economie



#==========================
# RECETTES
#==========================
def charger_table_recette(table):
    donnees = get_all_recette()
    table.clearContents()
    table.setRowCount(len(donnees))
    for ligne, recette in enumerate(donnees):
        for colonne, valeur in enumerate(recette):
            table.setItem(ligne, colonne, QTableWidgetItem(str(valeur)))


#==========================
# DEPENSES
#==========================
def charger_table_depense(table):
    donnees = get_all_depense()
    table.clearContents()
    table.setRowCount(len(donnees))
    for ligne, depense in enumerate(donnees):
        for colonne, valeur in enumerate(depense):
            table.setItem(ligne, colonne, QTableWidgetItem(str(valeur)))


#==========================
# ECONOMIES
#==========================
def charger_table_economie(table):
    donnees = get_all_economie()
    table.clearContents()
    table.setRowCount(len(donnees))
    for ligne, economie in enumerate(donnees):
        for colonne, valeur in enumerate(economie):
            table.setItem(ligne,colonne,QTableWidgetItem(str(valeur)))