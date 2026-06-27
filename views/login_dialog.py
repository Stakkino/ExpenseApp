from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel,QLineEdit, QPushButton,QMessageBox
from PyQt6.QtCore import Qt
from session import Session
from database import verifier_utilisateur
from database.connection import DBConnection
from utils.constants import *
import bcrypt

class LoginDialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self._configurer_fenetre()
        self._construire_ui()

    def _configurer_fenetre(self):
        self.setWindowTitle("Expense Application")
        self.setFixedSize(380, 300)
        self.setStyleSheet(f"background-color: {FOND_SECONDAIRE};")

    def _construire_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        # ── Titre ──
        titre = QLabel("Connexion")
        titre.setStyleSheet(f"color: {TEXTE_PRINCIPAL}; font-size: 16px; font-weight: bold;")
        layout.addWidget(titre)

        # ── Champ Email ──
        layout.addWidget(self._creer_label("Email"))
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Ex: tombojean@gmail.com")
        self.input_email.setStyleSheet(self._style_input())
        layout.addWidget(self.input_email)

        # ── Champ Mots de passe ──
        layout.addWidget(self._creer_label("Mots de passe"))
        self.input_mdp = QLineEdit()
        self.input_mdp.setPlaceholderText("**********")
        self.input_mdp.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_mdp.setStyleSheet(self._style_input())
        layout.addWidget(self.input_mdp)

        layout.addStretch()

        # ── Boutons ──
        boutons_layout = QHBoxLayout()
        btn_retour = QPushButton("Retour")
        btn_retour.setStyleSheet(self._style_bouton(FOND_INPUT, TEXTE_SECONDAIRE))
        btn_retour.clicked.connect(self.reject)

        btn_valider = QPushButton("Se connecter")
        btn_valider.setStyleSheet(self._style_bouton(BLEU_ECONOMIE, "#FFFFFF"))
        btn_valider.clicked.connect(self._valider)

        boutons_layout.addWidget(btn_retour)
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
        email         = self.input_email.text().strip()
        mdp           = self.input_mdp.text().strip()

        if not email or not mdp:
            QMessageBox.warning(self, "Champs vides", "Veuillez remplir les champs email et mots de passe.")
            return
        utilisateur = verifier_utilisateur(email, mdp)

        if utilisateur:
            Session.connecter(utilisateur[0:5])
            #QMessageBox.information(self, "Succès", f"Bienvenu, Tongasoa {Session.utilisateur_prenom} !")
            self.accept()
        else:
            QMessageBox.critical(self, "Erreur", "Vérifiez l'email ou le mot de passe !.")