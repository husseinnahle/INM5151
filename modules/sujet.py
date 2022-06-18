class Sujet:
    def __init__(self, id: int, nom: str, info: dict):
        self.id = id
        self.nom = nom
        self.info = info

    def get_nom(self):
        return self.nom

    def get_quiz(self, sous_sujet, numero):
        quiz = {
            "Question": self.info[sous_sujet]["Quiz"]["Question"][numero],
            "Choix": self.info[sous_sujet]["Quiz"]["Choix"][numero],
            "Reponse": self.info[sous_sujet]["Quiz"]["Reponse"][numero]
        }
        return quiz

    def to_json(self):
        sujet = {
            "Id": self.id,
            "Nom": self.nom,
            "Information": self.info
        }
        return sujet
