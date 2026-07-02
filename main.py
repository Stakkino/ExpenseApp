import sys
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QPoint

from views.main_window import MainWindow
from views.login_dialog import LoginDialog      
from views.incription_dialog import InscriptionDialog 
from utils.constants import *

class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(400, 500)
        self.setStyleSheet(f"background-color: {FOND_SECONDAIRE}; border-radius: 12px;")
        self._old_pos = None
        self._init_ui()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._old_pos = event.globalPosition().toPoint()
    def mouseMoveEvent(self, event):
        if self._old_pos is not None:
            delta = QPoint(event.globalPosition().toPoint() - self._old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self._old_pos = event.globalPosition().toPoint()
    def mouseReleaseEvent(self, event):
        self._old_pos = None

    def _init_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 15, 20, 30)
        layout_principal.setSpacing(20)

        top_bar = QHBoxLayout()
        top_bar.setAlignment(Qt.AlignmentFlag.AlignLeft)
        btn_close = QPushButton()
        btn_close.setFixedSize(12, 12)
        btn_close.setStyleSheet("""
            QPushButton { background-color: #ff5f56; border: none; border-radius: 6px; }
            """)
        btn_close.clicked.connect(self.close)
        top_bar.addWidget(btn_close)
        layout_principal.addLayout(top_bar)

        layout_principal.addStretch()

        self.logo_label = QLabel()
        pixmap = QPixmap("assets/icons/logo3.png")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(160, 160, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(self.logo_label)

        title_app = QLabel("ExpenseApp")
        title_app.setStyleSheet(f"color: {TEXTE_PRINCIPAL}; font-size: 24px; font-weight: bold;")
        title_app.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(title_app)

        subtitle = QLabel("Gérez vos finances en toute simplicité")
        subtitle.setStyleSheet(f"color: {TEXTE_SECONDAIRE}; font-size: 13px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(subtitle)

        layout_principal.addStretch()

        #----------------se connecter--------------
        self.btn_login = QPushButton("Se connecter")
        self.btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_login.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT_PRIMAIRE};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 20px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: #2b82c9; }}
        """)
        self.btn_login.clicked.connect(self._ouvrir_login)
        layout_principal.addWidget(self.btn_login)

        # -------------------S'inscrire-----------------------
        self.btn_register = QPushButton("Créer un compte (S'inscrire)")
        self.btn_register.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_register.setStyleSheet(f"""
            QPushButton {{
                background-color: {FOND_INPUT};
                color: {TEXTE_PRINCIPAL};
                border: 1px solid {BORDURE};
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {FOND_CARTE}; }}
        """)
        self.btn_register.clicked.connect(self._ouvrir_inscription)
        layout_principal.addWidget(self.btn_register)

    def _ouvrir_login(self):
        self.hide()
        dialog = LoginDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted: 
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            self.show()  

    def _ouvrir_inscription(self):
        self.hide()
        dialog = InscriptionDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._ouvrir_login()
        else:
            self.show()

def main():
    app = QApplication(sys.argv)
    welcome = WelcomeWindow()
    welcome.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()