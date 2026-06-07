import mysql.connector 
from mysql.connector import Error

from config import DB_CONFIG

class DBConnection:
    def __init__(self):
        self.config = DB_CONFIG
        self.connection = None
    
    def connect(self):
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**self.config)
            return self.connection
        except Error as e:
            print(f"Erreur de connexion à MySQL : {e}")
            return None
        
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connexion à la base de données fermée.")

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()