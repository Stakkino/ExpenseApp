from PyQt6.QtWidgets import QDialog,QVBoxLayout,QLabel,QLineEdit,QPushButton
from PyQt6.QtCore import Qt

from utils.constants import *
from views.message_dialog import CustomMessageDialog


class OtpDialog(QDialog):
    def __init__(self, otp, parent=None):
        super().__init__(parent)
        self.otp = str(otp)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(320, 220)
        self.setStyleSheet(f"background-color:{FOND_SECONDAIRE};")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        titre = QLabel("Vérification Email")
        titre.setStyleSheet(f"""color:{TEXTE_PRINCIPAL};font-size:16px;font-weight:bold;""")
        self.input_code = QLineEdit()
        self.input_code.setPlaceholderText("Entrez le code reçu")
        self.input_code.setStyleSheet(
            f"""
            background-color:{FOND_INPUT};
            color:{TEXTE_PRINCIPAL};
            border:1px solid {BORDURE};
            border-radius:6px;
            padding:8px;
            """
        )

        btn = QPushButton("Valider")
        btn.setStyleSheet(
            f"""
            QPushButton{{
                background-color:{BLEU_ECONOMIE};
                color:white;
                border:none;
                border-radius:6px;
                padding:10px;
                font-weight:bold;
            }}
            """
        )

        btn.clicked.connect(self.verifier)

        layout.addWidget(titre)
        layout.addSpacing(15)
        layout.addWidget(self.input_code)
        layout.addSpacing(15)
        layout.addWidget(btn)

    def verifier(self):
        code = self.input_code.text().strip()
        if code == self.otp:
            self.accept()
            return
        CustomMessageDialog( "Erreur", "Code OTP incorrect.", "warning", self).exec()