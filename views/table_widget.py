from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QDateEdit, QTableWidget, QHeaderView, QTableWidgetItem
from PyQt6.QtCore import Qt, QDate

from database import *
from utils.constants import *


class TableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet(f"""
            background-color: {FOND_PRINCIPAL};
            """)
        self.type_courant = "recette"
        self._construire_ui()
        self.charger_recette()

    def _construire_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24,24,24,24)
        layout.setSpacing(18)

        ligne_bouton = QHBoxLayout()
        self.btnRecette = QPushButton("Recettes")
        self.btnDepense = QPushButton("Dépenses")
        self.btnEconomie = QPushButton("Économies")

        for bouton in (self.btnRecette,self.btnDepense,self.btnEconomie):
            bouton.setCursor(Qt.CursorShape.PointingHandCursor)
            bouton.setFixedHeight(38)
            bouton.setStyleSheet(f"""
                QPushButton{{
                    background:{BLEU_ECONOMIE};
                    color:white;
                    border:none;
                    border-radius:8px;
                    font-weight:bold;
                }}
                QPushButton:hover{{
                    background:#2980B9;
                }}
                """)
            ligne_bouton.addWidget(bouton)
        ligne_bouton.addStretch()
        layout.addLayout(ligne_bouton)

        ligne_filtre = QHBoxLayout()
        lbl1 = QLabel("Date début")
        self.dateDebut = QDateEdit()
        self.dateDebut.setCalendarPopup(True)
        self.dateDebut.setDate(QDate.currentDate().addMonths(-1))
        lbl2 = QLabel("Date fin")
        self.dateFin = QDateEdit()
        self.dateFin.setCalendarPopup(True)
        self.dateFin.setDate(QDate.currentDate())
        self.btnFiltrer = QPushButton("Filtrer")
        self.btnReset = QPushButton("Réinitialiser")

        for widget in (self.btnFiltrer, self.btnReset):
            widget.setCursor(Qt.CursorShape.PointingHandCursor)
            widget.setFixedHeight(35)
        ligne_filtre.addWidget(lbl1)
        ligne_filtre.addWidget(self.dateDebut)
        ligne_filtre.addSpacing(20)
        ligne_filtre.addWidget(lbl2)
        ligne_filtre.addWidget(self.dateFin)
        ligne_filtre.addSpacing(25)
        ligne_filtre.addWidget(self.btnFiltrer)
        ligne_filtre.addWidget(self.btnReset)
        ligne_filtre.addStretch()
        layout.addLayout(ligne_filtre)


        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet(f"""
            QTableWidget{{
                background:white;
                border-radius:10px;
                gridline-color:#DDDDDD;
                font-size:12px;
            }}
            QHeaderView::section{{
                background:{BLEU_ECONOMIE};
                color:white;
                font-weight:bold;
                border:none;
                height:34px;
            }}
            """)
        layout.addWidget(self.table)


        self.btnRecette.clicked.connect(self.charger_recette)
        self.btnDepense.clicked.connect(self.charger_depense)
        self.btnEconomie.clicked.connect(self.charger_economie)
        self.btnFiltrer.clicked.connect(self.filtrer)
        self.btnReset.clicked.connect(self.refresh)

    # RECETTES
    def charger_table_recette(self):
        self.type_courant = "recette"
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID","Montant","Description","Date"])
        donnees = get_all_recette()
        self._remplir_table(donnees)


    # DEPENSES
    def charger_table_depense(self):
        self.type_courant = "depense"
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID","Catégorie","Description","Montant","Date"])
        donnees = get_all_depense()
        self._remplir_table(donnees)


    # ECONOMIES
    def charger_table_economie(self):
        self.type_courant = "economie"
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID","Type","Montant","Description","Date"])
        donnees = get_all_economie()
        self._remplir_table(donnees)


    # FILTRE
    def filtrer(self):
        date_debut = self.dateDebut.date().toPyDate()
        date_fin = self.dateFin.date().toPyDate()
        if self.type_courant == "recette":
            donnees = get_all_recette(date_debut, date_fin)
        elif self.type_courant == "depense":
            donnees = get_all_depense(date_debut, date_fin)
        else:
            donnees = get_all_economie(date_debut, date_fin)
        self._remplir_table(donnees)


    # RESET
    def refresh(self):
        self.dateDebut.setDate(QDate.currentDate().addMonths(-1))
        self.dateFin.setDate(QDate.currentDate())
        if self.type_courant == "recette":
            self.charger_recette()
        elif self.type_courant == "depense":
            self.charger_depense()
        else:
            self.charger_economie()



    # AFFICHAGE TABLE
    def _remplir_table(self, donnees):
        self.table.clearContents()
        self.table.setRowCount(len(donnees))
        for ligne, element in enumerate(donnees):
            for colonne, valeur in enumerate(element):
                item = QTableWidgetItem(str(valeur))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(ligne, colonne, item)