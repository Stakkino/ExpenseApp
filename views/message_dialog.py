from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from utils.constants import *
import resources_rc 

class CustomMessageDialog(QDialog):
    def __init__(self, title, message, type="info", parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setFixedSize(350, 200)
        icons = {
            "error": ":/assets/icons/error.png",
            "warning": ":/assets/icons/alert.png",
            "success": ":/assets/icons/succes.png",
            "info": ":/assets/icons/info.png"
        }
        
        # Layout principal
        self.setStyleSheet(f"background-color: {FOND_SECONDAIRE}; border: 1px solid #374151;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Icon
        icon_label = QLabel()
        pixmap = QPixmap(icons.get(type, icons["info"]))
        if not pixmap.isNull():
            icon_label.setPixmap(pixmap.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Text
        msg_label = QLabel(message)
        msg_label.setWordWrap(True)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_label.setStyleSheet("font-size: 14px; color: #FFFFFF; font-family: sans-serif;")
        
        # Bouton OK
        btn = QPushButton("OK")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{ 
                background-color: {ACCENT_PRIMAIRE}; 
                color: white; 
                border-radius: 8px; 
                padding: 10px; 
                font-weight: bold; 
            }}
            QPushButton:hover {{ background-color: #2b82c9; }}
        """)
        btn.clicked.connect(self.accept)
        
        layout.addWidget(icon_label)
        layout.addWidget(msg_label)
        layout.addWidget(btn)