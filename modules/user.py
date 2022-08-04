import hashlib
import uuid
import re
from .user_type import user_type
from .user_level import user_level

def create_user(username: str, email: str, password: str, type: user_type,experience: int,level: user_level):
    try:
        _validate_user(username, email, password, type)  # ValueError
    except ValueError as error:
        raise ValueError(error)
    salt = uuid.uuid4().hex
    hash = hashlib.sha512(str(password + salt).encode("utf-8")).hexdigest()
    return User(0, username, email, salt, hash, type, experience,level)


def modify_user(user, username, email, password):
    try:
        if password is None:
            _verify_username(username)
            _verify_email(email)
        else:
            _validate_user(username, email, password)  # ValueError
    except ValueError as error:
        raise ValueError(error)
    hash = ""
    if password is not None:
        salt = user.get_salt()
        hash = hashlib.sha512(str(password + salt).encode("utf-8")).hexdigest()
    user._modify_info(username, email, hash)


def _validate_user(username, email, password, type):
    if username == "" or email == "" or password == "":
        raise ValueError("All fields are required")
    try:
        _verify_username(username)
        _verify_email(email)
        _verify_password(password)
        _verify_type(type)
    except ValueError as error:
        raise ValueError(error)


def _verify_username(username):
    if len(username) < 6:
        raise ValueError("The username should have 6 characters or more")


def _verify_password(password):
    if len(password) < 8:
        raise ValueError("The password should have 8 characters or more")


def _verify_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(regex, email):
        raise ValueError("Invalid email")


def _verify_type(type):
    if type not in [type.value for type in user_type]:
        raise ValueError("Invalid type")


def validate_support_form(name, email, message):
    if name == "" or email == "" or message == "":
        raise ValueError("All fields are required")
    try:
        _verify_email(email)
    except ValueError as error:
        raise ValueError(error)


class User:
    def __init__(self, id: int, username: str, email: str, salt: str,   hash: str, type: user_type,experience: int,
                 level: user_level):
        self.id = id
        self.name = username
        self.email = email
        self.salt = salt
        self.hash = hash
        self.type = type
        self.progress = {}
        self.experience = experience
        self.level = level

    def update_progress(self, sujet, sous_sujet, resultat):
        if sujet not in self.progress:
            self.progress[sujet] = {sous_sujet: resultat}
            return
        if (sous_sujet in self.progress[sujet]
                and self.progress[sujet][sous_sujet] == "E"):
            self.progress[sujet][sous_sujet] = resultat
        elif sous_sujet not in self.progress[sujet]:
            self.progress[sujet][sous_sujet] = resultat
    def add_xp(self, xp):
        self.experience += xp
        if (self.experience + xp > 10):
            self.level = user_level.INITIATE

    def get_name(self):
        return self.name

    def get_progress(self):
        return self.progress

    def get_experience(self):
        return self.experience

    def get_level(self):
        return self.level
    
    def get_salt(self):
        return self.salt

    def set_progress(self, progress):
        self.progress = progress

    def set_experience(self, experience):
        self.experience = experience

    def _modify_info(self, name, email, hash):
        self.name = name
        self.email = email
        if hash != "":
            self.hash = hash

    def make_member(self):
        self.type = user_type.MEMBER

    def session(self):
        session = {
            "name": self.name,
            "type": self.type,
            "email": self.email,
            "progress": self.progress,
            "experience": self.experience,
            "level": self.level,
        }
        return session
