from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel,QLineEdit, QComboBox, QPushButton
from PyQt6.QtCore import Qt
from decimal import Decimal, InvalidOperation
from database import *
from utils.constants import *
from utils.theme_manager import ThemeManager
theme = ThemeManager.theme()
from views.message_dialog import CustomMessageDialog

class EconomieDialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self._configurer_fenetre()
        self._construire_ui()

    def _configurer_fenetre(self):
        self.setWindowTitle("Nouvelle Économie")
        self.setFixedSize(380, 440)
        self.setStyleSheet(f"background-color: {theme['FOND_SECONDAIRE']};")

    def _construire_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        # ── Titre ──
        titre = QLabel("Ajouter une économie")
        titre.setStyleSheet(f"color: {theme['TEXTE_PRINCIPAL']}; font-size: 16px; font-weight: bold;")
        layout.addWidget(titre)

        # ── Solde disponible (info) ──
        self.label_solde = QLabel()
        self.label_solde.setStyleSheet(f"color: {theme['TEXTE_SECONDAIRE']}; font-size: 12px;")
        layout.addWidget(self.label_solde)

        # ── Solde economie (info) ──
        self.label_econom = QLabel()
        self.label_econom.setStyleSheet(f"color: {theme['TEXTE_SECONDAIRE']}; font-size: 12px;")
        layout.addWidget(self.label_econom)

        # ── Champ type ──
        layout.addWidget(self._creer_label("Type"))
        self.combo_type = QComboBox()
        self.combo_type.addItems(['Ajouter', 'Retrait'])
        self.combo_type.setStyleSheet(self._style_input())
        layout.addWidget(self.combo_type)

        # ── Champ Montant ──
        layout.addWidget(self._creer_label("Montant (Ar)"))
        self.input_montant = QLineEdit()
        self.input_montant.setPlaceholderText("Ex: 5000")
        self.input_montant.setStyleSheet(self._style_input())
        layout.addWidget(self.input_montant)

        # ── Champ Description ──
        layout.addWidget(self._creer_label("Description"))
        self.input_description = QLineEdit()
        self.input_description.setPlaceholderText("Ex: Projet Vacance")
        self.input_description.setStyleSheet(self._style_input())
        layout.addWidget(self.input_description)

        layout.addStretch()

        # ── Boutons ──
        boutons_layout = QHBoxLayout()
        btn_annuler = QPushButton("Annuler")
        btn_annuler.setStyleSheet(self._style_bouton(theme['FOND_INPUT'], theme['TEXTE_SECONDAIRE']))
        btn_annuler.clicked.connect(self.reject)

        btn_valider = QPushButton("Ajouter")
        btn_valider.setStyleSheet(self._style_bouton(theme['BLEU_ECONOMIE'], "#FFFFFF"))
        btn_valider.clicked.connect(self._valider)

        boutons_layout.addWidget(btn_annuler)
        boutons_layout.addWidget(btn_valider)
        layout.addLayout(boutons_layout)

        # Affiche les info
        self.label_solde.setText(
            f"Solde disponible : {get_solde_dispo():,.0f} Ar".replace(",", " "))
        self.label_econom.setText(
            f"Solde économie : {get_total_economie():,.0f} Ar".replace(",", " "))
        
    def _creer_label(self, texte: str) -> QLabel:
        label = QLabel(texte)
        label.setStyleSheet(f"color: {theme['TEXTE_LABEL']}; font-size: 11px; font-weight: bold;")
        return label

    
    def _style_input(self) -> str:
        return f"""
            QWidget {{
                background-color: {theme['FOND_INPUT']};
                color: {theme['TEXTE_PRINCIPAL']};
                border: 1px solid {theme['BORDURE']};
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
        types         = self.combo_type.currentText()
        descriptions  = self.input_description.text().strip()

        if not txt_montant:
            CustomMessageDialog("Champ vide", "Veuillez saisir un montant.", "warning", self).exec()
            return
        try:
            montante = Decimal(txt_montant)
        except InvalidOperation:
            CustomMessageDialog("Montant invalide", "Le montant doit être un nombre valide.", "info", self).exec()
            return
        if montante <= 0:
            CustomMessageDialog("Montant invalide", "Le montant doit être supérieur à 0.", "info", self).exec()
            return
        
        if types is None:
            CustomMessageDialog("Champ vide", "Veuillez choisir un type.", "warning", self).exec()
            return
        
        succes = actionconomie(types, montante, descriptions)

        if succes:
            CustomMessageDialog("Succès", "Économie ajoutée avec succès.", "success", self).exec()
            self.accept() 
        else:
            CustomMessageDialog("Erreur", "Impossible d'ajouter l'économie.\nVérifiez que le montant ne dépasse pas le solde économie.", "error", self).exec()