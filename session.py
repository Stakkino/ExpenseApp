class Session:
    utilisateur_id = None
    utilisateur_nom = None
    utilisateur_prenom = None
    utilisateur_email = None
    utilisateur_datenaissance = None
    avatar = "assets/avatars/family.png" 

    @classmethod
    def connecter(cls, utilisateur):
        cls.utilisateur_id = utilisateur[0]
        cls.utilisateur_nom = utilisateur[1]
        cls.utilisateur_prenom = utilisateur[2]
        cls.utilisateur_email = utilisateur[3]
        cls.utilisateur_datenaissance = utilisateur[4]

    @classmethod
    def deconnecter(cls):
        cls.utilisateur_id = None
        cls.utilisateur_nom = None
        cls.utilisateur_prenom = None
        cls.utilisateur_email = None
        cls.utilisateur_datenaissance = None
        cls.avatar = "assets/avatars/family.png"

    @classmethod
    def est_connecte(cls):
        return cls.utilisateur_id is not None