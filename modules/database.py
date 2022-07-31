import sqlite3
import json
from .sujet import Sujet
from .user import User
from .request import Request
from .status import status


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
        cursor = connection.cursor()
        cursor.execute(
            'insert into user(username, email, salt, hash, progress, type) values(?, ?, ?, ?, ?, ?)',
            (user.name, user.email, user.salt, user.hash,
             json.dumps(user.progress), user.type))
        connection.commit()
        return cursor.lastrowid

    # Rechercher et retourner un utilisateur selon 'username'
    def read_user_username(self, username):
        cursor = self.get_connection().cursor()
        cursor.execute('select * from user where username=?', (username,))
        user = cursor.fetchone()
        if user is None:
            return None
        user_obj = User(user[0], user[1], user[2], user[3], user[4], user[6])
        user_obj.set_progress(json.loads(user[5]))
        return user_obj


    # Rechercher et retourner un utilisateur selon 'username'
    def read_users(self):
        cursor = self.get_connection().cursor()
        cursor.execute('select * from user')
        users = cursor.fetchall()
        if users is None:
            return None
        return (User(user[0], user[1], user[2], user[3], user[4], user[6]) for user in users)

    # Rechercher et retourner un utilisateur selon 'username'
    def delete_users(self,id):
        connection = self.get_connection()
        connection.execute('Delete FROM user where id = ?',(id,))
        connection.commit()


    # Mettre à jour la progression d'un utilisateur selon 'username'
    def update_user_progress(self, user: User):
        connection = self.get_connection()
        connection.execute('update user set progress = ? where username = ?',
                           (json.dumps(user.get_progress()), user.get_name()))
        connection.commit()

    # Mettre à jour les info du compte d'un utilisateur selon 'username'
    def update_user_info(self, user: User):
        connection = self.get_connection()
        connection.execute('update user set username = ?, email = ?, hash = ?, type = ?'
                           'where id = ?',
                           (user.name, user.email, user.hash, user.type, user.id))
        connection.commit()

    def update_user_membership(self, user: User):
        connection = self.get_connection()
        connection.execute('update user set type = ?'
                           'where id = ?',
                           (user.type, user.id))
        connection.commit()

    def insert_request(self, request, username):
        connection = self.get_connection()
        connection.execute('insert into request(username, first_name, last_name, speciality, cv, letter, status, date)'
                           'values(?, ?, ?, ?, ?, ?, ?, ?)',
                            (username, request.first_name, request.last_name,
                             ' '.join(request.speciality),
                             sqlite3.Binary(request.cv.read()),
                             sqlite3.Binary(request.letter.read()),
                             request.status, request.date))
        connection.commit()

    def read_request_username(self, username):
        cursor = self.get_connection().cursor()
        cursor.execute('select * from request where username = ?', (username,))
        requests = cursor.fetchall()
        return [Request(request[0], request[2], request[3], request[4].split(' '), request[5], request[6], status(request[7]), request[8]) for request in requests]
    
    def read_request_id(self, id):
        cursor = self.get_connection().cursor()
        cursor.execute('select * from request where id = ?', (id,))
        request = cursor.fetchone()
        return Request(request[0], request[2], request[3], request[4].split(' '), request[5], request[6], status(request[7]), request[8])