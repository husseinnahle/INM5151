import sqlite3
import json
from .sujet import Sujet


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/database.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    # Inserer un sujet
    def insert_sujet(self, id, nom, informations):
        connection = self.get_connection()
        connection.execute('insert or ignore into sujet'
                           '(id, nom, informations)'
                           'values(?, ?, ?)',
                           (id, nom, informations))
        connection.commit()

    # Retourner tous les sujets
    def read_all_sujet(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('select * from sujet')
        sujets = cursor.fetchall()
        return (Sujet(sujet[0], sujet[1], json.loads(sujet[2]))
                for sujet in sujets)

    # Rechercher et retourner un sujet selon 'nom'
    def read_sujet_nom(self, nom: str):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute('select * from sujet '
                       'where nom=?', (nom,))
        sujet = cursor.fetchone()
        return Sujet(sujet[0], sujet[1], json.loads(sujet[2]))