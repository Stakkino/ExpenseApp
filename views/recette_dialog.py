from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel,QLineEdit, QComboBox, QDateTimeEdit, QPushButton,QMessageBox, QFrame
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from decimal import Decimal, InvalidOperation

from database import get_all_recette,ajoutrecette
from utils.formatters import format_montant
from utils.constants import *


class RecetteDialog(QDialog):
    def __init__(self, parent = None ):
        super().__init__(parent)
        self._configurer_fenetre()
        self._construire_ui()

    def _configurer_fenetre(self):
        self.setWindowTitle("Nouvelle Dépense")
        self.setFixedSize(380, 380)
        self.setStyleSheet(f"background-color: {FOND_SECONDAIRE};")

    def _construire_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        # ── Titre ──
        titre = QLabel("Ajouter une recette")
        titre.setStyleSheet(f"color: {TEXTE_PRINCIPAL}; font-size: 16px; font-weight: bold;")
        layout.addWidget(titre)

        # ── Champ Montant ──
        layout.addWidget(self._creer_label("Montant (Ar)"))
        self.input_montant = QLineEdit()
        self.input_montant.setPlaceholderText("Ex: 15000")
        self.input_montant.setStyleSheet(self._style_input())
        layout.addWidget(self.input_montant)