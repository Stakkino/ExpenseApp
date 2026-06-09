from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class Recette:
    montantr : Decimal
    descriptions : str
    id : int = None
    dater : datetime = None