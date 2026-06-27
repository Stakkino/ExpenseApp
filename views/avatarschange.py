# import os
# from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QDateEdit, QPushButton, QMessageBox
# from PyQt6.QtCore import Qt, QDate
# from PyQt6.QtGui import QIcon

# from database import modification_info
# from utils.constants import *
# from session import Session
# from config import DB_CONFIG 




# # ── CHANGER AVATAR (Selector) ──
#         layout.addWidget(self._creer_label("Choisir un Avatar"))
#         self.combo_avatar = QComboBox()
#         self.combo_avatar.setStyleSheet(self._style_input())
        
#         dossier_avatar = "assets/avatars"
#         if os.path.exists(dossier_avatar):
#             for fichier in os.listdir(dossier_avatar):
#                 if fichier.lower().endswith(('.png', '.jpg', '.jpeg')):
#                     chemin_feno = os.path.join(dossier_avatar, fichier)
#                     self.combo_avatar.addItem(QIcon(chemin_feno), fichier, chemin_feno)
        
#         avatar_anketriny = DB_CONFIG.get("avatar", "young-man.png").split("/")[-1]
#         index = self.combo_avatar.findText(avatar_anketriny)
#         if index >= 0:
#             self.combo_avatar.setCurrentIndex(index)
            
#         layout.addWidget(self.combo_avatar)





# chemin_avatar = self.combo_avatar.currentData()
# if chemin_avatar:
#                 DB_CONFIG["avatar"] = chemin_avatar