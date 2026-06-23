from dataclasses import dataclass
from datetime import datetime, date

@dataclass
class Utilisateur:
    nom : str
    prenom : str
    email : str 
    datenaissance : date
    mdp : str
    id : int = None
    creat : datetime = None