from database.connection import DBConnection

db = DBConnection()
conn = db.connect()

if conn:
    print("Connexion réussie !")
    db.close()
else:
    print("Échec de connexion.")