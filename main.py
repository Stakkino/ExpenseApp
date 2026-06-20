import sys
from PyQt6.QtWidgets import QApplication

from database.connection import DBConnection
from views.main_window import MainWindow

app = QApplication(sys.argv)

db = DBConnection()
conn = db.connect()

if conn:
    print("Connexion réussie !")

    window = MainWindow()
    window.show()

    conn.close()

    sys.exit(app.exec())

else:
    print("Échec de connexion.")