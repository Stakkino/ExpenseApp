from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from database import (get_solde, get_total_depense, get_total_economie, get_solde_dispo)
from utils.formatters import format_montant
from utils.constants import *


class DashboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet(f"background-color: {FOND_PRINCIPAL};")
        self._construire_ui()
        self.refresh()

   
    def _construire_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # Ligne des 4 cartes
        self.cartes_layout = QHBoxLayout()
        self.cartes_layout.setSpacing(16)

        # Création des 4 cartes — gardées en référence pour refresh()
        self.carte_solde    = self._creer_carte("Solde Total",      "0 Ar", JAUNE_SOLDE,    "assets/icons/solde.png")
        self.carte_depense  = self._creer_carte("Total Dépenses",   "0 Ar", ROUGE_DEPENSE,  "assets/icons/depense.png")
        self.carte_economie = self._creer_carte("Économies",        "0 Ar", BLEU_ECONOMIE,  "assets/icons/econimie.png")
        self.carte_dispo    = self._creer_carte("Solde Disponible", "0 Ar", VERT_RECETTE,   "assets/icons/sdispo.png")

        self.cartes_layout.addWidget(self.carte_solde)
        self.cartes_layout.addWidget(self.carte_depense)
        self.cartes_layout.addWidget(self.carte_economie)
        self.cartes_layout.addWidget(self.carte_dispo)

        layout.addLayout(self.cartes_layout)
        layout.addStretch()

   
    def _creer_carte(self, titre: str, valeur: str,
                     couleur: str, icone_path: str) -> QFrame:
        carte = QFrame()
        carte.setSizePolicy(QSizePolicy.Policy.Expanding,
                            QSizePolicy.Policy.Fixed)
        carte.setFixedHeight(120)
        carte.setStyleSheet(f"""
            QFrame {{
                background-color: {FOND_CARTE};
                border-radius: 12px;
            }}
        """)

        layout = QHBoxLayout(carte)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # ── Icone ──
        icone_label = QLabel()
        icone_label.setFixedSize(40, 40)
        icone_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icone_label.setStyleSheet(f"""
            background-color: {couleur};
            border-radius: 20px;
        """)
        pixmap = QPixmap(icone_path)
        if not pixmap.isNull():
            icone_label.setPixmap(
                pixmap.scaled(22, 22,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation)
            )

        # ── Textes ──
        textes_layout = QVBoxLayout()
        textes_layout.setSpacing(4)

        label_titre = QLabel(titre)
        label_titre.setStyleSheet(f"""
            color: {TEXTE_LABEL};
            font-size: 11px;
            font-weight: bold;
            letter-spacing: 1px;
        """)

        label_valeur = QLabel(valeur)
        label_valeur.setStyleSheet(f"""
            color: {couleur};
            font-size: 20px;
            font-weight: bold;
        """)

        textes_layout.addWidget(label_titre)
        textes_layout.addWidget(label_valeur)

        layout.addWidget(icone_label)
        layout.addLayout(textes_layout)
        layout.addStretch()

        # Stocke le label_valeur dans la carte pour refresh()
        carte.label_valeur = label_valeur

        return carte

   
    def refresh(self):
        """Appelée après chaque INSERT — recharge les chiffres depuis la BDD."""
        self.carte_solde.label_valeur.setText(
            format_montant(get_solde()))

        self.carte_depense.label_valeur.setText(
            format_montant(get_total_depense()))

        self.carte_economie.label_valeur.setText(
            format_montant(get_total_economie()))

        self.carte_dispo.label_valeur.setText(
            format_montant(get_solde_dispo()))