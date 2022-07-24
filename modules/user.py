import hashlib
import uuid
import re


def create_user(username, email, password, id_type):
    try:
        _validate_user(username, email, password)  # ValueError
    except ValueError as error:
        raise ValueError(error)
    salt = uuid.uuid4().hex
    hash = hashlib.sha512(str(password + salt).encode("utf-8")).hexdigest()
    return User(0, username, email, salt, hash, id_type)


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


def make_member(user):
    user.set_member(True)


def _validate_user(username, email, password):
    if username == "" or email == "" or password == "":
        raise ValueError("All fields are required")
    try:
        _verify_username(username)
        _verify_email(email)
        _verify_password(password)
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


def validate_support_form(name, email, message):
    if name == "" or email == "" or message == "":
        raise ValueError("All fields are required")
    try:
        _verify_email(email)
    except ValueError as error:
        raise ValueError(error)


class User:
    def __init__(self, id: int, username: str, email: str, salt: str,
                 hash: str, id_type: int):
        self.id = id
        self.name = username
        self.email = email
        self.salt = salt
        self.hash = hash
        self.id_type = id_type
        self.member = False
        self.progress = {}

    def update_progress(self, sujet, sous_sujet, resultat):
        if sujet not in self.progress:
            self.progress[sujet] = {sous_sujet: resultat}
            return
        if (sous_sujet in self.progress[sujet]
                and self.progress[sujet][sous_sujet] == "E"):
            self.progress[sujet][sous_sujet] = resultat
        elif sous_sujet not in self.progress[sujet]:
            self.progress[sujet][sous_sujet] = resultat

    def get_name(self):
        return self.name

    def get_progress(self):
        return self.progress

    def get_salt(self):
        return self.salt

    def set_progress(self, progress):
        self.progress = progress

    def _modify_info(self, name, email, hash):
        self.name = name
        self.email = email
        if hash != "":
            self.hash = hash

    def set_member(self, value):
        self.member = value

    def session(self):
        session = {
            "name": self.name,
            "member": self.member,
            "email": self.email,
            "progress": self.progress,
            "type": self.id_type
        }
        return session
