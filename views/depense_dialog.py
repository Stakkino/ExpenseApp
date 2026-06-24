from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel,QLineEdit, QComboBox, QDateTimeEdit, QPushButton,QMessageBox
from PyQt6.QtCore import Qt
from decimal import Decimal, InvalidOperation
from database import ajoutdepense, get_solde_dispo
from database.connection import DBConnection
from utils.constants import *


class DepenseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self._configurer_fenetre()
        self._construire_ui()
        self._charger_categories()

    def _configurer_fenetre(self):
        self.setWindowTitle("Nouvelle Dépense")
        self.setFixedSize(380, 400)
        self.setStyleSheet(f"background-color: {FOND_SECONDAIRE};")

    def _construire_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        # ── Titre ──
        titre = QLabel("Ajouter une dépense")
        titre.setStyleSheet(f"color: {TEXTE_PRINCIPAL}; font-size: 16px; font-weight: bold;")
        layout.addWidget(titre)

        # ── Solde disponible (info) ──
        self.label_solde = QLabel()
        self.label_solde.setStyleSheet(f"color: {TEXTE_SECONDAIRE}; font-size: 12px;")
        layout.addWidget(self.label_solde)

        # ── Champ Montant ──
        layout.addWidget(self._creer_label("Montant (Ar)"))
        self.input_montant = QLineEdit()
        self.input_montant.setPlaceholderText("Ex: 15000")
        self.input_montant.setStyleSheet(self._style_input())
        layout.addWidget(self.input_montant)

        # ── Champ Catégorie ──
        layout.addWidget(self._creer_label("Catégorie"))
        self.combo_categorie = QComboBox()
        self.combo_categorie.setStyleSheet(self._style_input())
        layout.addWidget(self.combo_categorie)

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
        btn_annuler.clicked.connect(self.reject) 

        btn_valider = QPushButton("Ajouter")
        btn_valider.setStyleSheet(self._style_bouton(ROUGE_DEPENSE, "#FFFFFF"))
        btn_valider.clicked.connect(self._valider)

        boutons_layout.addWidget(btn_annuler)
        boutons_layout.addWidget(btn_valider)
        layout.addLayout(boutons_layout)

        # Affiche le solde dispo actuel
        self.label_solde.setText(
            f"Solde disponible : {get_solde_dispo():,.0f} Ar".replace(",", " "))

    
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

   
    def _charger_categories(self):
        """Remplit le QComboBox avec les catégories de la table Categorie."""
        sql = "SELECT id, nom FROM Categorie ORDER BY nom"
        try:
            with DBConnection() as conx:
                curseur = conx.cursor()
                curseur.execute(sql)
                for cat_id, nom in curseur.fetchall():
                    # addItem(texte_affiché, donnée_cachée)
                    self.combo_categorie.addItem(nom, cat_id)
        except Exception as e:
            print(f"Erreur chargement catégories : {e}")

    
    def _valider(self):
        txt_montant   = self.input_montant.text().strip()
        categorie     = self.combo_categorie.currentData()
        descriptions  = self.input_description.text().strip()

        if not txt_montant:
            QMessageBox.warning(self, "Champ vide", "Veuillez saisir un montant.")
            return
        try:
            montantd = Decimal(txt_montant)
        except InvalidOperation:
            QMessageBox.warning(self, "Montant invalide", "Le montant doit être un nombre valide.")
            return
        if montantd <= 0:
            QMessageBox.warning(self, "Montant invalide", "Le montant doit être supérieur à 0.")
            return

        if categorie is None:
            QMessageBox.warning(self, "Catégorie manquante", "Veuillez sélectionner une catégorie.")
            return

        succes = ajoutdepense(categorie, descriptions, montantd)

        if succes:
            QMessageBox.information(self, "Succès", "Dépense ajoutée avec succès.")
            self.accept() 
        else:
            QMessageBox.critical(self, "Erreur", "Impossible d'ajouter la dépense.\n""Vérifiez que le montant ne dépasse pas le solde disponible.")