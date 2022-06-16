class Sujet:
    def __init__(self, id: int, nom: str, informations: dict):
        self.id = id
        self.nom = nom
        self.informations = informations

    def to_json(self):
        sujet = {
            "Id": self.id,
            "Nom": self.nom,
            "Information": self.informations
        }
        return sujet
