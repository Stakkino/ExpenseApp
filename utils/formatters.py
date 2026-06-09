from decimal import Decimal


def format_montant(valeur) -> str:
    try:
        valeur = Decimal(str(valeur))
        entier = int(valeur)
        partie_entiere = f"{entier:,}".replace(",", " ")
        return f"{partie_entiere} Ar"
    except Exception:
        return "0 Ar"