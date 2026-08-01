from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel,QLineEdit, QDateEdit, QPushButton
from PyQt6.QtCore import Qt, QDate
from email_validator import validate_email, EmailNotValidError

from database import *
from utils.constants import *
from utils import *
from utils.theme_manager import ThemeManager
theme = ThemeManager.theme()
from views import *


class InscriptionDialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self._configurer_fenetre()
        self._construire_ui()

    def _configurer_fenetre(self):
        self.setWindowTitle("ExApp")
        self.setFixedSize(450, 630)
        self.setStyleSheet(f"background-color: {theme['FOND_SECONDAIRE']};")

    def _construire_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        # ── Titre ──
        titre = QLabel("Inscription")
        titre.setStyleSheet(f"color: {theme['TEXTE_PRINCIPAL']}; font-size: 16px; font-weight: bold;")
        layout.addWidget(titre)

        # ── Champ Nom ──
        layout.addWidget(self._creer_label("Nom"))
        self.input_nom = QLineEdit()
        self.input_nom.setPlaceholderText("Ex: TOMBO")
        self.input_nom.setStyleSheet(self._style_input())
        layout.addWidget(self.input_nom)

        # ── Champ Prenom ──
        layout.addWidget(self._creer_label("Prénom"))
        self.input_prenom = QLineEdit()
        self.input_prenom.setPlaceholderText("Ex: Jean")
        self.input_prenom.setStyleSheet(self._style_input())
        layout.addWidget(self.input_prenom)

        # ── Champ Email ──
        layout.addWidget(self._creer_label("Email"))
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Ex: tombojean@gmail.com")
        self.input_email.setStyleSheet(self._style_input())
        layout.addWidget(self.input_email)

        # ── Champ Datenaissance ──
        layout.addWidget(self._creer_label("Date de naissance"))
        zao = QDate.currentDate()
        maxidate = zao.addYears(-7)
        self.input_datenaissance = QDateEdit()
        self.input_datenaissance.setCalendarPopup(True)
        self.input_datenaissance.setDisplayFormat("dd/MM/yyyy")
        self.input_datenaissance.setMaximumDate(maxidate)
        self.input_datenaissance.setDate(maxidate)
        self.input_datenaissance.setStyleSheet(f"""
            QDateEdit {{
                background-color: {theme['FOND_INPUT']};
                color: {theme['TEXTE_PRINCIPAL']};
                border: 1px solid {theme['BORDURE']};
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
            }}
            QCalendarWidget {{
                background-color: {theme['FOND_INPUT']};
                color: {theme['TEXTE_PRINCIPAL']};
                border: 1px solid {theme['BORDURE']};
                border-radius: 8px;
            }}
            QCalendarWidget QToolButton {{
                color: {theme['TEXTE_PRINCIPAL']};
                background-color: transparent;
                font-size: 13px;
                font-weight: bold;
                height: 30px;
            }}
            QCalendarWidget QMenu {{
                background-color: {theme['FOND_INPUT']};
                color: {theme['TEXTE_PRINCIPAL']};
            }}
            QCalendarWidget QAbstractItemView {{
                background-color: {theme['FOND_INPUT']};
                color: {theme['TEXTE_PRINCIPAL']};
                selection-background-color: {theme['BLEU_ECONOMIE']};
                selection-color: white;
                border-radius: 6px;
            }}
            QCalendarWidget QAbstractItemView:disabled {{
                color: #777777;
            }}
        """)
        layout.addWidget(self.input_datenaissance)
        self.label_info = QLabel("Réservé aux personnes de 7 ans et plus")
        self.label_info.setStyleSheet(f"font-size:11px; color:{theme['TEXTE_LABEL']}; margin-top:-2px; margin-bottom:10px")
        layout.addWidget(self.label_info)

        # ── Champ Mots de passe ──
        layout.addWidget(self._creer_label("Mots de passe"))
        self.input_mdp = QLineEdit()
        self.input_mdp.setPlaceholderText("**********")
        self.input_mdp.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_mdp.setStyleSheet(self._style_input())
        layout.addWidget(self.input_mdp)

        # ── Champ Confirmer Mots de passe ──
        layout.addWidget(self._creer_label("Confirmer Mots de passe"))
        self.input_cmdp = QLineEdit()
        self.input_cmdp.setPlaceholderText("**********")
        self.input_cmdp.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_cmdp.setStyleSheet(self._style_input())
        layout.addWidget(self.input_cmdp)

        layout.addStretch()

        # ── Boutons ──
        boutons_layout = QHBoxLayout()
        btn_retour = QPushButton("Retour")
        btn_retour.setStyleSheet(self._style_bouton(theme['FOND_INPUT'], theme['TEXTE_SECONDAIRE']))
        btn_retour.clicked.connect(self.reject)

        btn_valider = QPushButton("S'inscrire")
        btn_valider.setStyleSheet(self._style_bouton(theme['BLEU_ECONOMIE'], "#FFFFFF"))
        btn_valider.clicked.connect(self._valider)

        boutons_layout.addWidget(btn_retour)
        boutons_layout.addWidget(btn_valider)
        layout.addLayout(boutons_layout)


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
        nom           = self.input_nom.text().strip()
        prenom        = self.input_prenom.text().strip()
        email         = self.input_email.text().strip()
        datenaissance = self.input_datenaissance.date().toString("yyyy-MM-dd")
        mdp           = self.input_mdp.text().strip()
        cmdp          = self.input_cmdp.text().strip()

        if not nom or not email:
            CustomMessageDialog("Champ vide", "Veuillez saisir votre Nom ou votre Email.", "warning", self).exec()
            return
        if not mdp or not cmdp:
            CustomMessageDialog("Champ vide", "Veuillez remplir les champs de mots de passe.", "warning", self).exec()
            return
        if cmdp != mdp:
            CustomMessageDialog("Vérification", "Mots de passe non identique", "info", self).exec()
            return
        
        try:
            validate_email(email)
        except EmailNotValidError:
            CustomMessageDialog("Erreur","Adresse email invalide.","warning",self).exec()
            return

        otp = envoyer_otp(email)

        if not otp:
            CustomMessageDialog("Erreur","Impossible d'envoyer le code OTP.","error",self ).exec()
            return
        dialog = OtpDialog(otp, self)
        if not dialog.exec():
            return

        
        succes = incription(nom, prenom, email, datenaissance, mdp)

        if succes:
            CustomMessageDialog("Succès", "Incrire avec succès.", "success", self).exec()
            self.accept() 
        else:
            CustomMessageDialog("Erreur", "Impossible d'inscrire.\nVérifiez la connexion ou les champs !.", "error", self).exec()