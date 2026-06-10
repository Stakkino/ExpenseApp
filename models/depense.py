from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class Depense:
    categorie : int
    descriptions : str
    montantd : Decimal
    id : int = None
    dated : datetime = None