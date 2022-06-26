class Sujet:
    def __init__(self, id: int, nom: str, info: dict):
        self.id = id
        self.nom = nom
        self.info = info

    def get_nom(self):
        return self.nom

    def get_sous_sujet(self, sous_sujet):
        for item in self.info["Sous-sujet"]:
            if item["Nom"] == sous_sujet:
                return item
        raise ValueError("Le sous-sujet " + sous_sujet + " n'existe pas.")

    def get_sous_sujet_index(self, sous_sujet):
        for index, item in enumerate(self.info["Sous-sujet"]):
            if item["Nom"] == sous_sujet:
                return index
        raise ValueError("Le sous-sujet " + sous_sujet + " n'existe pas.")

    def get_quiz_reponse(self, sous_sujet_index, numero):
        return self.info["Sous-sujet"][sous_sujet_index]["Quiz"][numero]["Reponse"]

    def get_quiz_question(self, sous_sujet_index, numero):
        quiz = self.info["Sous-sujet"][sous_sujet_index]["Quiz"]
        return {"Question": quiz[numero]["Question"], "Choix": quiz[numero]["Choix"]}

    def to_json(self):
        sujet = {
            "Id": self.id,
            "Nom": self.nom,
            "Information": self.info
        }
        return sujet
