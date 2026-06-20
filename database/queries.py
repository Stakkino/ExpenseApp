from database.connection import DBConnection
from decimal import Decimal


#-----------------LES METHODES GET--------------------
#-----------------------------------------------------
#-------------------LES CALCULES----------------------
def get_solde() -> Decimal:
    sql = "SELECT COALESCE(SUM(montantr), 0) FROM Recette"
    try :
        with DBConnection() as conx:
            curseur = conx.cursor()
            curseur.execute(sql)
            return Decimal(curseur.fetchone()[0])
    except Exception as e:
        print(f"Erreur de Coonexion DB : {e}")
        return 0.0

#-------------------------------------------------------
def get_total_depense() -> Decimal:
    sql = "SELECT COALESCE(SUM(montantd), 0) FROM Depense"
    try :
        with DBConnection() as conx:
            curseur = conx.cursor()
            curseur.execute(sql)
            return Decimal(curseur.fetchone()[0])
    except Exception as e:
        print(f"Erreur de Coonexion DB : {e}")
        return 0.0

#--------------------------------------------------------
def get_total_economie() -> Decimal:
    sql = """
        SELECT COALESCE(SUM(montante), 0)
        FROM Economie
        """
    try :
        with DBConnection() as conx:
            curseur = conx.cursor()
            curseur.execute(sql)
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
#-------------------------RECETTE-------------------------
def ajoutrecette(montantr: Decimal, descriptions: str) -> bool:
    montantr = abs(montantr)
    if montantr == 0:         
        return False
    
    sql = """
        INSERT INTO Recette (montantr, descriptions)
        VALUES (%s, %s)
        """
    try :
        with DBConnection() as conx:
            curseur = conx.cursor()
            curseur.execute(sql, (montantr, descriptions))
            conx.commit()
            return True
    except Exception as e:
        print(f"Erreur Ajouter Recette : {e}")
        return False


#----------------------------DEPENSE----------------------------
def ajoutdepense(categorie: int, descriptions: str, montantd: Decimal) -> bool:
    montantd = abs(montantd)
    if montantd == 0:         
        return False

    solde_dispo = get_solde_dispo()
    if montantd > solde_dispo :
        print(f"Solde Dispo est insuffisant : {solde_dispo} Ar")
        return False

    sql = """
        INSERT INTO Depense (categorie, descriptions, montantd)
        VALUES (%s, %s, %s)
        """
    try : 
        with DBConnection() as conx:
            curseur = conx.cursor()
            curseur.execute(sql, (categorie, descriptions, montantd))
            conx.commit()
            return True
    except Exception as e:
        print(f"Erreur Ajouter Dépense : {e}")
        return False


#--------------------------ECONOMIE-----------------------------
def actionconomie(types: str, montante: Decimal, descriptions: str) -> bool:
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
        INSERT INTO Economie(types, montante, descriptions)
        VALUES (%s, %s, %s)
        """
    try :
        with DBConnection() as conx:
            curseur = conx.cursor()
            curseur.execute(sql, (types, montante, descriptions))
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
        ORDER BY dater DESC
    """
    try :
        with DBConnection() as conx:
            curseur = conx.cursor()
            curseur.execute(sql)
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
        ORDER BY d.dated DESC
        """
    try :
        with DBConnection() as conx:
            curseur = conx.cursor()
            curseur.execute(sql)
            return curseur.fetchall()
    except Exception as e:
        print(f"Erreur des listes de Depense : {e}")
        return []

#---------------------ECONOMIE--------------------
def get_all_economie() -> list:
    sql = """
        SELECT id, types, montante, descriptions, datee
        FROM Economie
        ORDER BY datee DESC
        """
    try :
        with DBConnection() as conx:
            curseur = conx.cursor()
            curseur.execute(sql)
            return curseur.fetchall()
    except Exception as e:
        print(f"Erreur des listes d'Economie : {e}")
        return []