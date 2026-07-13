from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from utils.constants import *
import resources_rc 

class CustomMessageDialog(QDialog):
    icons = {
            "error": ":/assets/icons/error.png",
            "warning": ":/assets/icons/alert.png",
            "success": ":/assets/icons/circle-check.png",
            "info": ":/assets/icons/info.png"
        }
    
    def __init__(self, title, message, type="info", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setFixedSize(360, 170)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {FOND_SECONDAIRE};
                border-radius: 10px;
            }}
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(8)

        icon_label = QLabel()
        icon_label.setFixedSize(40, 40)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        icon_path = self.icons.get(type, self.icons["info"])
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            icon_label.setPixmap(pixmap.scaled(40,40,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation))
        msg_label = QLabel(message)
        msg_label.setWordWrap(True)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        msg_label.setContentsMargins(0, 0, 0, 0)

        msg_label.setStyleSheet("""
            QLabel{
                color: white;
                font-size:14px;
                font-family:Segoe UI;
                border:none;
                margin:0px;
                padding:0px;
            }
        """)
        content_layout.addWidget(icon_label)
        content_layout.addWidget(msg_label, 1)

        btn = QPushButton("OK")
        btn.setFixedSize(90, 32)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT_PRIMAIRE};
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #2b82c9;
            }}
            QPushButton:pressed {{
                background-color: #1d6fa5;
            }}
            """)
        btn.clicked.connect(self.accept)

        main_layout.addLayout(content_layout)
        main_layout.addStretch()
        main_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)