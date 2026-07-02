import os
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDateEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, QDate

from database import modification_info
from utils.constants import *
from session import Session
from config import DB_CONFIG 

class ProfilDialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self._configurer_fenetre()
        self._construire_ui()

    def _configurer_fenetre(self):
        self.setWindowTitle("Expense Application")
        self.setFixedSize(380, 500) 
        self.setStyleSheet(f"background-color: {FOND_SECONDAIRE};")

    def _construire_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        # ── Titre ──
        titre = QLabel("Modification Info")
        titre.setStyleSheet(f"color: {TEXTE_PRINCIPAL}; font-size: 16px; font-weight: bold;")
        layout.addWidget(titre)

        # ── Champ Nom ──
        layout.addWidget(self._creer_label("Nom"))
        self.input_nom = QLineEdit()
        self.input_nom.setText(f"{Session.utilisateur_nom}") 
        self.input_nom.setStyleSheet(self._style_input())
        layout.addWidget(self.input_nom)

        # ── Champ Prenom ──
        layout.addWidget(self._creer_label("Prénom"))
        self.input_prenom = QLineEdit()
        self.input_prenom.setText(f"{Session.utilisateur_prenom}")
        self.input_prenom.setStyleSheet(self._style_input())
        layout.addWidget(self.input_prenom)

        # ── Champ Email ──
        layout.addWidget(self._creer_label("Email"))
        self.input_email = QLineEdit()
        self.input_email.setText(f"{Session.utilisateur_email}")
        self.input_email.setStyleSheet(self._style_input())
        layout.addWidget(self.input_email)

        # ── Champ Datenaissance ──
        layout.addWidget(self._creer_label("Date de naissance"))
        try:
            daty_session = QDate.fromString(str(Session.utilisateur_datenaissance), "yyyy-MM-dd")
            if not daty_session.isValid():
                daty_session = QDate.currentDate().addYears(-7)
        except:
            daty_session = QDate.currentDate().addYears(-7)

        self.input_datenaissance = QDateEdit()
        self.input_datenaissance.setCalendarPopup(True)
        self.input_datenaissance.setDisplayFormat("dd/MM/yyyy")
        self.input_datenaissance.setDate(daty_session)
        self.input_datenaissance.setStyleSheet(self._style_input())
        layout.addWidget(self.input_datenaissance)
        
        self.label_info = QLabel("Réservé aux personnes de 7 ans et plus")
        self.label_info.setStyleSheet(f"font-size:11px; color:{TEXTE_LABEL}; margin-top:-2px; margin-bottom:10px")
        layout.addWidget(self.label_info)

        layout.addStretch()

        # ── Boutons ──
        boutons_layout = QHBoxLayout()
        btn_annuler = QPushButton("Annuler")
        btn_annuler.setStyleSheet(self._style_bouton(FOND_INPUT, TEXTE_SECONDAIRE))
        btn_annuler.clicked.connect(self.reject)

        btn_valider = QPushButton("Sauvegarder")
        btn_valider.setStyleSheet(self._style_bouton(BLEU_ECONOMIE, "#FFFFFF"))
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
        nom           = self.input_nom.text().strip()
        prenom        = self.input_prenom.text().strip()
        email         = self.input_email.text().strip()
        datenaissance = self.input_datenaissance.date().toString("yyyy-MM-dd")
        

        if not nom or not email:
            QMessageBox.warning(self, "Champ vide", "Veuillez saisir votre Nom ou votre Email.")
            return
        
        succes = modification_info(nom, prenom, email, datenaissance)

        if succes:
            Session.utilisateur_nom = nom
            Session.utilisateur_prenom = prenom
            Session.utilisateur_email = email
            Session.utilisateur_datenaissance = datenaissance
            
            QMessageBox.information(self, "Succès", "Modifié avec succès.")
            self.accept() 
        else:
            QMessageBox.critical(self, "Erreur", "Impossible de modifier.\nVérifiez la connexion ou les champs !.")