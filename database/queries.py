from database.connection import DBConnection
from decimal import Decimal
from session import Session
from datetime import date
import bcrypt


#-----------------LES METHODES GET--------------------
#-----------------------------------------------------
#-----------------------LOGIN-------------------------
def verifier_utilisateur(email: str, mdp:str) -> bool:
    sql = """SELECT id,nom,prenom,email,datenaissance,mdp 
            FROM Utilisateur
            WHERE email = %s
        """
    try:
        with DBConnection() as conx:
            curseur = conx.cursor()
            curseur.execute(sql,(email))
            utilisateur = curseur.fetchone()
            curseur.close()

            if utilisateur and utilisateur[4] == mdp:
                return utilisateur
            return None
    except Exception as e:
        print(f"Erreur de Coonexion DB : {e}")
        return False
                  
#-------------------LES CALCULES----------------------
def get_solde() -> Decimal:
    sql = "SELECT COALESCE(SUM(montantr), 0) FROM Recette WHERE utilisateur = %s"
    try :
        with DBConnection() as conx:
            curseur = conx.cursor()
            curseur.execute(sql, (Session.utilisateur_id,))
            return Decimal(curseur.fetchone()[0])
    except Exception as e:
        print(f"Erreur de Coonexion DB : {e}")
        return 0.0

#-------------------------------------------------------
def get_total_depense() -> Decimal:
    sql = "SELECT COALESCE(SUM(montantd), 0) FROM Depense WHERE utilisateur = %s"
    try :
        with DBConnection() as conx:
            curseur = conx.cursor()
            curseur.execute(sql, (Session.utilisateur_id,))
            return Decimal(curseur.fetchone()[0])
    except Exception as e:
        print(f"Erreur de Coonexion DB : {e}")
        return 0.0

#--------------------------------------------------------
def get_total_economie() -> Decimal:
    sql = """
        SELECT COALESCE(SUM(montante), 0)
        FROM Economie
        WHERE utilisateur = %s
        """
    try :
        with DBConnection() as conx:
            curseur = conx.cursor()
            curseur.execute(sql, (Session.utilisateur_id,))
            return Decimal(curseur.fetchone()[0])
    except Exception as e:
        print(f"Erreur de Coonexion DB : {e}")
        return 0.0

#---------------------------------------------------------
def get_solde_dispo() -> Decimal:
    try :
        with DBConnection() as conx:
            curseur = conx.cursor()
            solde = get_solde()
            depense = get_total_depense()
            economie = get_total_economie()
            return solde - depense - economie
    except Exception as e:
        print(f"Erreur de Coonexion DB : {e}")
        return 0.0






#--------------------LES METHODES SET---------------------
#---------------------------------------------------------
#----------------------UTILISATEUR------------------------
def incription(nom : str, prenom : str, email : str, datenaissance : date, mdp : str) -> bool :
    a = mdp.encode('utf-8')
    b = bcrypt.gensalt()
    mdp = bcrypt.hashpw(a,b)

    sql = """ INSERT INTO Utilisateur (nom, prenom, email, datenaissance, mdp)
              VALUES = %s, %s, %s, %s, %s
        """
    try:
        with DBConnection() as conx:
            curseur = conx.cursor()
            curseur.execute(sql, (nom, prenom, email, datenaissance, mdp))
            conx.commit()
            return True
    except Exception as e:
        print(f"Erreur Ajouter Recette : {e}")
        return False

#------------------MISE A JOUR PROFIL---------------------
def modification_info(nom:str, prenom:str, email:str, datenaissance:date) -> bool:
    sql = """ UPDATE Utilisateur
              SET nom = %s, prenom = %s, email = %s, datenaissance = %s
              WHERE id = %s
        """ 
    try:
        with DBConnection() as conx:
            curseur = conx.cursor()
            curseur.execute(sql, (nom,prenom,email,datenaissance,Session.utilisateur_id))
            conx.commit()
            return True
    except Exception as e:
        print(f"Erreur de Modification Profil : {e}")
        return False

#-------------------------RECETTE-------------------------
def ajoutrecette(montantr: Decimal, descriptions: str) -> bool:
    utilisateur = Session.utilisateur_id
    montantr = abs(montantr)
    if montantr == 0:         
        return False
    
    sql = """
        INSERT INTO Recette (utilisateur, montantr, descriptions)
        VALUES (%s,%s, %s)
        """
    try :
        with DBConnection() as conx:
            curseur = conx.cursor()
            curseur.execute(sql, (utilisateur,montantr, descriptions))
            conx.commit()
            return True
    except Exception as e:
        print(f"Erreur Ajouter Recette : {e}")
        return False


#----------------------------DEPENSE----------------------------
def ajoutdepense(categorie: int, descriptions: str, montantd: Decimal) -> bool:
    utilisateur = Session.utilisateur_id
    montantd = abs(montantd)
    if montantd == 0:         
        return False

    solde_dispo = get_solde_dispo()
    if montantd > solde_dispo :
        print(f"Solde Dispo est insuffisant : {solde_dispo} Ar")
        return False

    sql = """
        INSERT INTO Depense (utilisateur, categorie, descriptions, montantd)
        VALUES (%s, %s, %s, %s)
        """
    try : 
        with DBConnection() as conx:
            curseur = conx.cursor()
            curseur.execute(sql, (utilisateur, categorie, descriptions, montantd))
            conx.commit()
            return True
    except Exception as e:
        print(f"Erreur Ajouter Dépense : {e}")
        return False


#--------------------------ECONOMIE-----------------------------
def actionconomie(types: str, montante: Decimal, descriptions: str) -> bool:
    utilisateur = Session.utilisateur_id
    montante = abs(montante)
    if montante == 0:          
        return False

    if types == 'Ajouter':
        solde_dispo = get_solde_dispo()
        if montante > solde_dispo:
            print(f"Solde Dispo est insuffisant : {solde_dispo} Ar")
            return False
    
    if types == 'Retrait':
        solde_economie = get_total_economie()
        if montante > solde_economie:
            print(f"Solde Économie est insuffisant : {solde_economie} Ar")
            return False
        montante = - montante

    sql = """
        INSERT INTO Economie(utilisateur, types, montante, descriptions)
        VALUES (%s, %s, %s, %s)
        """
    try :
        with DBConnection() as conx:
            curseur = conx.cursor()
            curseur.execute(sql, (utilisateur, types, montante, descriptions))
            conx.commit()
            return True
    except Exception as e:
        print(f"Erreur Action sur Économie : {e}")
        return False





#-------------------LES METHODES LISTEs---------------
#-----------------------------------------------------
#-----------------------RECETTE-----------------------
def get_all_recette() -> list:
    sql = """
        SELECT id, montantr, descriptions, dater
        FROM Recette
        WHERE utilisateur = %s
        ORDER BY dater DESC
    """
    try :
        with DBConnection() as conx:
            curseur = conx.cursor()
            curseur.execute(sql, (Session.utilisateur_id))
            return curseur.fetchall()
    except Exception as e:
        print(f"Erreur des listes de Recette : {e}")
        return []

#-----------------------DEPENSE------------------------
def get_all_depense() -> list:
    sql = """
        SELECT d.id, c.nom, d.descriptions, d.montantd, d.dated
        FROM Depense d
        JOIN Categorie c ON d.categorie = c.id
        WHERE utilisateur = %s
        ORDER BY d.dated DESC
        """
    try :
        with DBConnection() as conx:
            curseur = conx.cursor()
            curseur.execute(sql, (Session.utilisateur_id))
            return curseur.fetchall()
    except Exception as e:
        print(f"Erreur des listes de Depense : {e}")
        return []

#---------------------ECONOMIE--------------------
def get_all_economie() -> list:
    sql = """
        SELECT id, types, montante, descriptions, datee
        FROM Economie
        WHERE utilisateur = %s
        ORDER BY datee DESC
        """
    try :
        with DBConnection() as conx:
            curseur = conx.cursor()
            curseur.execute(sql, (Session.utilisateur_id))
            return curseur.fetchall()
    except Exception as e:
        print(f"Erreur des listes d'Economie : {e}")
        return []