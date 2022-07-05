import hashlib
import uuid
import re

def create_user(username, email, password):
  try:
    _validate_user(username, email, password)  # ValueError
  except ValueError as error:
    raise ValueError(error)
  salt = uuid.uuid4().hex
  hash = hashlib.sha512(str(password + salt).encode("utf-8")).hexdigest()
  return User(0, username, email, salt, hash)

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

class User:
  def __init__(self, id: int, username: str, email: str, salt: str, hash: str):
    self.id = id
    self.name = username
    self.email = email
    self.salt = salt
    self.hash = hash

  def session(self):
    session = {
      "name": self.name,
      "email": self.email
    }
    return session