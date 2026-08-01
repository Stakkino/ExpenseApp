from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDateEdit, QTableWidget, QHeaderView, QTableWidgetItem
from PyQt6.QtCore import Qt, QDate

from database import *
from utils.constants import *
from utils.theme_manager import ThemeManager
theme = ThemeManager.theme()


class TableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet(f"""
            background-color: {theme['FOND_PRINCIPAL']};
            """)
        self.type_courant = "recette"
        self._construire_ui()
        self.charger_table_recette()

    def _construire_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24,24,24,24)
        layout.setSpacing(18)

        # ================= FILTRE =================
        ligne_filtre = QHBoxLayout()
        ligne_filtre.setSpacing(12)
        style_label = f""" QLabel {{color:{theme['TEXTE_PRINCIPAL']};font-size:12px;font-weight:bold;}}"""
        lbl1 = QLabel("Date début")
        lbl1.setStyleSheet(style_label)
        self.dateDebut = QDateEdit()
        self.dateDebut.setCalendarPopup(True)
        self.dateDebut.setDate(QDate.currentDate().addMonths(-1))

        lbl2 = QLabel("Date fin")
        lbl2.setStyleSheet(style_label)
        self.dateFin = QDateEdit()
        self.dateFin.setCalendarPopup(True)
        self.dateFin.setDate(QDate.currentDate())

        style_date = f"""
            QDateEdit {{
                background:{theme['FOND_INPUT']};
                color:{theme['TEXTE_PRINCIPAL']};
                border:1px solid {theme['BORDURE']};
                border-radius:8px;
                padding:6px 10px;
                font-size:12px;
            }}
            QDateEdit:hover {{
                    border:1px solid {theme['ACCENT_PRIMAIRE']};
                }}
            QDateEdit::drop-down {{
                    border:none;
                }}
        """
        self.dateDebut.setStyleSheet(style_date)
        self.dateFin.setStyleSheet(style_date)

        # Bouton Filtrer
        self.btnFiltrer = QPushButton("Filtrer")
        self.btnFiltrer.setStyleSheet(f"""
            QPushButton {{
                background:{theme['ACCENT_PRIMAIRE']};
                color:white;
                border:none;
                border-radius:8px;
                padding:8px 22px;
                font-size:12px;
                font-weight:bold;
            }}
            QPushButton:hover {{
                background:{theme['ACCENT_HOVER']};
            }}
            QPushButton:pressed {{
                background:{theme['ACCENT_PRESSED']};
            }}
        """)

        # Bouton Reset
        self.btnReset = QPushButton("Réinitialiser")
        self.btnReset.setStyleSheet(f"""
            QPushButton {{
                background:{theme['FOND_CARTE']};
                color:{theme['TEXTE_PRINCIPAL']};
                border:1px solid {theme['BORDURE']};
                border-radius:8px;
                padding:8px 18px;
                font-size:12px;
                font-weight:bold;
            }}
            QPushButton:hover {{
                background:{theme['BORDURE']};
                border:1px solid {theme['ACCENT_PRIMAIRE']};
            }}
            QPushButton:pressed {{
                background:{theme['FOND_INPUT']};
            }}
        """)
        for widget in (self.btnFiltrer,self.btnReset):
            widget.setCursor(Qt.CursorShape.PointingHandCursor)
            widget.setFixedHeight(38)

        ligne_filtre.addWidget(lbl1)
        ligne_filtre.addWidget(self.dateDebut)
        ligne_filtre.addSpacing(15)
        ligne_filtre.addWidget(lbl2)
        ligne_filtre.addWidget(self.dateFin)
        ligne_filtre.addSpacing(20)
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
            QTableWidget {{
                background:{theme['FOND_SECONDAIRE']};
                alternate-background-color:{theme['FOND_CARTE']};
                color:{theme['TEXTE_PRINCIPAL']};
                border:1px solid {theme['BORDURE']};
                border-radius:12px;
                gridline-color:{theme['BORDURE']};
                font-size:12px;
                selection-background-color:{theme['ACCENT_PRIMAIRE']};
                selection-color:white;
            }}
            QTableWidget::item {{
                padding:8px;
                border-bottom:1px solid {theme['BORDURE']};
            }}
            QTableWidget::item:hover {{
                background:#243B55;
            }}
            QHeaderView::section {{
                background:{theme['ACCENT_PRIMAIRE']};
                color:white;
                font-size:12px;
                font-weight:bold;
                height:38px;
                border:none;
                padding-left:8px;
            }}
            QScrollBar:vertical {{
                background:{theme['FOND_PRINCIPAL']};
                width:10px;
            }}
            QScrollBar::handle:vertical {{
                background:{theme['ACCENT_PRIMAIRE']};
                border-radius:5px;
            }}
        """)
        
        layout.addWidget(self.table)

        self.btnFiltrer.clicked.connect(self.filtrer)
        self.btnReset.clicked.connect(self.refresh)

    # RECETTES
    def charger_table_recette(self):
        self.type_courant = "recette"
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID","Montant","Description","Date et Heure"])
        donnees = get_all_recette()
        self._remplir_table(donnees)


    # DEPENSES
    def charger_table_depense(self):
        self.type_courant = "depense"
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID","Catégorie","Description","Montant","Date et Heure"])
        donnees = get_all_depense()
        self._remplir_table(donnees)


    # ECONOMIES
    def charger_table_economie(self):
        self.type_courant = "economie"
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID","Type","Montant","Description","Date et Heure"])
        donnees = get_all_economie()
        self._remplir_table(donnees)

    #-----------------------HISTORIQUE------------------------
    def charger_table_historique(self):
        self.type_courant = "historique"
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Type", "Montant", "Description", "Date et Heure"])
        donnees = get_all_historique()
        self._remplir_table(donnees)


    # FILTRE
    def filtrer(self):
        date_debut = self.dateDebut.date().toPyDate()
        date_fin = self.dateFin.date().toPyDate()
        if self.type_courant == "recette":
            donnees = get_all_recette(date_debut, date_fin)
        elif self.type_courant == "depense":
            donnees = get_all_depense(date_debut, date_fin)
        elif self.type_courant == "economie":
            donnees = get_all_economie(date_debut, date_fin)
        elif self.type_courant == "historique":
            donnees = get_all_historique(date_debut, date_fin)
        self._remplir_table(donnees)


    # RESET
    def refresh(self):
        self.dateDebut.setDate(QDate.currentDate().addMonths(-1))
        self.dateFin.setDate(QDate.currentDate())
        if self.type_courant == "recette":
            self.charger_table_recette()
        elif self.type_courant == "depense":
            self.charger_table_depense()
        elif self.type_courant == "economie":
            self.charger_table_economie()
        elif self.type_courant == "historique":
            self.charger_table_historique()



    # AFFICHAGE TABLE
    def _remplir_table(self, donnees):
        self.table.clearContents()
        self.table.setRowCount(len(donnees))
        for ligne, element in enumerate(donnees):
            for colonne, valeur in enumerate(element):
                item = QTableWidgetItem(str(valeur))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(ligne, colonne, item)