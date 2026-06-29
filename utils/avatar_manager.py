import os
import json

AVATAR_FILE = "data/avatars.json"
DEFAULT_AVATAR = "assets/avatars/family.png"


def creer_fichier():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(AVATAR_FILE):
        with open(AVATAR_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)

def lire_avatar(email):
    creer_fichier()
    with open(AVATAR_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(email, DEFAULT_AVATAR)


def enregistrer_avatar(email, chemin):
    creer_fichier()
    with open(AVATAR_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    data[email] = chemin
    with open(AVATAR_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)