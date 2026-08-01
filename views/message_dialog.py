from PyQt6.QtWidgets import QDialog,QVBoxLayout,QLabel,QPushButton,QWidget
from PyQt6.QtCore import Qt,QPropertyAnimation
from PyQt6.QtGui import QPixmap
from BlurWindow.blurWindow import blur

from utils.constants import *
from utils.theme_manager import ThemeManager
theme = ThemeManager.theme()
import resources_rc


class CustomMessageDialog(QDialog):
    ICONS = {
        "success": ":/assets/icons/succes.png",
        "error": ":/assets/icons/error.png",
        "warning": ":/assets/icons/alert.png",
        "info": ":/assets/icons/info.png",
    }

    BORDERS = {
        "success":"#2ECC71",
        "error":"#E74C3C",
        "warning":"#F1C40F",
        "info":"#3498DB",
    }

    def __init__(self,title,message,type="info",parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(300,240)
        self.setWindowFlags(Qt.WindowType.Dialog |Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("""QDialog{background: transparent;border: none;}""")
        border=self.BORDERS.get(type,"#3498DB")
        root=QVBoxLayout(self)
        root.setContentsMargins(0,0,0,0)
        root.setSpacing(0)

        card=QWidget()
        card.setObjectName("card")
        card.setStyleSheet(f"""
        #card{{
            background-color:rgba(36,36,36,245);
            border:2px solid {border};
            border-radius:18px;
        }}

        QLabel{{
            border:none;
            color:white;
            background:transparent;
        }}

        QPushButton{{
            background:{theme['ACCENT_PRIMAIRE']};
            color:white;
            border:none;
            border-radius:8px;
            padding:8px 22px;
            font:600 13px 'Segoe UI';
        }}

        QPushButton:hover{{
            background:#2b82c9;
        }}
        """)
        root.addWidget(card)

        layout=QVBoxLayout(card)
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon=QLabel()
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pix=QPixmap(self.ICONS.get(type,self.ICONS["info"]))
        if not pix.isNull():
            icon.setPixmap(
                pix.scaled(
                    42,42,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )

        titleLabel=QLabel(title)
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titleLabel.setStyleSheet("""
        QLabel{
            color:white;
            font:700 17px 'Segoe UI';
            border:none;
        }
        """)

        msg=QLabel(message)
        msg.setWordWrap(True)
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg.setStyleSheet("""
        QLabel{
            color:#E8E8E8;
            font:14px 'Segoe UI';
            border:none;
        }
        """)

        ok=QPushButton("OK")
        ok.setFixedWidth(110)
        ok.clicked.connect(self.accept)

        layout.addStretch()
        layout.addWidget(icon)
        layout.addWidget(titleLabel)
        layout.addWidget(msg)
        layout.addSpacing(8)
        layout.addWidget(ok,alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        self.setWindowOpacity(0)
        self.anim=QPropertyAnimation(self,b"windowOpacity")
        self.anim.setDuration(180)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()

    def keyPressEvent(self,event):
        if event.key() in (Qt.Key.Key_Return,Qt.Key.Key_Enter,Qt.Key.Key_Escape):
            self.accept()
        else:
            super().keyPressEvent(event)
