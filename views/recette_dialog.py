from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel,QLineEdit, QComboBox, QDateTimeEdit, QPushButton,QMessageBox
from PyQt6.QtCore import Qt
from decimal import Decimal, InvalidOperation

from database import ajoutrecette
from utils.constants import *


class RecetteDialog(QDialog):
    def __init__(self, parent = None ):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self._configurer_fenetre()
        self._construire_ui()

    def _configurer_fenetre(self):
        self.setWindowTitle("Nouvelle Recette")
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

        # ── Champ Description ──
        layout.addWidget(self._creer_label("Description"))
        self.input_description = QLineEdit()
        self.input_description.setPlaceholderText("Ex: Riz et légumes")
        self.input_description.setStyleSheet(self._style_input())
        layout.addWidget(self.input_description)

        layout.addStretch()

        # ── Boutons ──
        boutons_layout = QHBoxLayout()
        btn_annuler = QPushButton("Annuler")
        btn_annuler.setStyleSheet(self._style_bouton(FOND_INPUT, TEXTE_SECONDAIRE))
        btn_annuler.clicked.connect(self.reject)  # ferme dialog, exec() renvoie False

        btn_valider = QPushButton("Ajouter")
        btn_valider.setStyleSheet(self._style_bouton(VERT_RECETTE, "#FFFFFF"))
        btn_valider.clicked.connect(self._valider)

        boutons_layout.addWidget(btn_annuler)
        boutons_layout.addWidget(btn_valider)
        layout.addLayout(boutons_layout)

        
    def _creer_label(self, texte: str) -> QLabel:
        label = QLabel(texte)
        label.setStyleSheet(f"color: {TEXTE_LABEL}; font-size: 11px; font-weight: bold;")
        return label

    
    def _style_input(self) -> str:
        return f"""
            QWidget {{
                background-color: {FOND_INPUT};
                color: {TEXTE_PRINCIPAL};
                border: 1px solid {BORDURE};
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
            }}
        """

    def _style_bouton(self, bg: str, color: str) -> str:
        return f"""
            QPushButton {{
                background-color: {bg};
                color: {color};
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
            }}
        """
    
    def _valider(self):
        txt_montant   = self.input_montant.text().strip()
        descriptions  = self.input_description.text().strip()

        if not txt_montant:
            QMessageBox.warning(self, "Champ vide", "Veuillez saisir un montant.")
            return 
        try:
            montantr = Decimal(txt_montant)
        except InvalidOperation:
            QMessageBox.warning(self, "Montant invalide", "Le montant doit être un nombre valide.")
            return
        if montantr <= 0 :
            QMessageBox.warning(self, "Montant invalide", "Le montant doit être supérieur à 0.")
            return
        
        succes = ajoutrecette(montantr, descriptions)

        if succes:
            QMessageBox.information(self, "Succès", "Recette ajoutée avec succès.")
            self.accept()
        else:
            QMessageBox.critical(self, "Erreur", "Impossible d'ajouter la Recette.")