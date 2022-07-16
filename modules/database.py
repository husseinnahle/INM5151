import sqlite3
import json
from .sujet import Sujet
from .user import User


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

    # Inserer un utilisateur
    def insert_user(self, user):
        connection = self.get_connection()
        connection.execute('insert into user'
                           '(username, email, salt, hash, progress)'
                           'values(?, ?, ?, ?, ?)',
                           (user.name, user.email, user.salt, user.hash,
                            json.dumps(user.progress)))
        connection.commit()

    # Rechercher et retourner un utilisateur selon 'username'
    def read_user_username(self, username):
        cursor = self.get_connection().cursor()
        cursor.execute('select * from user where username=?', (username,))
        user = cursor.fetchone()
        if user is None:
            return None
        user_obj = User(user[0], user[1], user[2], user[3], user[4])
        user_obj.set_progress(json.loads(user[5]))
        return user_obj

    # Mettre à jour la progression d'un utilisateur selon 'username'
    def update_user_progress(self, user: User):
        connection = self.get_connection()
        connection.execute('update user set progress = ? where username = ?',
                           (json.dumps(user.get_progress()), user.get_name()))
        connection.commit()

    # Mettre à jour les info du compte d'un utilisateur selon 'username'
    def update_user_info(self, user: User):
        connection = self.get_connection()
        connection.execute('update user set username = ?, email = ?, hash = ?'
                           'where id = ?',
                           (user.name, user.email, user.hash, user.id))
        connection.commit()
