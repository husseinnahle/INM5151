class Sujet:
    def __init__(self, id: int, nom: str, info: dict):
        self.id = id
        self.nom = nom
        self.info = info

    def get_nom(self):
        return self.nom

    def get_quiz_reponse(self, sous_sujet, numero):
        quiz = self.info["Sous-sujet"][sous_sujet]["Quiz"]
        return quiz["Reponse"][numero]
    
    def get_quiz_question(self, sous_sujet, numero):
        quiz = self.info["Sous-sujet"][sous_sujet]["Quiz"]
        return {"Question": quiz["Question"][numero],
                    "Choix": quiz["Choix"][numero]}
            
    def to_json(self):
        sujet = {
            "Id": self.id,
            "Nom": self.nom,
            "Information": self.info
        }
        return sujet
