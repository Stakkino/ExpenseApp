from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class Economie:
    types : str
    montante : Decimal
    descriptions : str
    id : int = None
    datee : datetime = None