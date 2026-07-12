from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import resources_rc

class CustomMessageDialog(QDialog):
    def __init__(self, title, message, type="info", parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(350, 200)
        
        # Famaritana ny icon araka ny type
        icons = {
            "error": ":/assets/icons/error.png",
            "warning": ":/assets/icons/alert.png",
            "success": ":/assets/icons/succes.png",
            "info": ":/assets/icons/info.png"
        }
        
        layout = QVBoxLayout(self)
        self.setStyleSheet("background-color: #ffffff; border-radius: 15px;")
        
        # Icon
        icon_label = QLabel()
        pixmap = QPixmap(icons.get(type, icons["info"])).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio)
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Text
        msg_label = QLabel(message)
        msg_label.setWordWrap(True)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_label.setStyleSheet("font-size: 14px; color: #333; margin: 10px; font-family: sans-serif;")
        
        # Button
        btn = QPushButton("OK")
        btn.setStyleSheet("""
            QPushButton { background-color: #3D9BE9; color: white; border-radius: 8px; padding: 8px; font-weight: bold; }
            QPushButton:hover { background-color: #2b82c9; }
        """)
        btn.clicked.connect(self.accept)
        
        layout.addWidget(icon_label)
        layout.addWidget(msg_label)
        layout.addWidget(btn)