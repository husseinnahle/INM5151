from .status import status
from datetime import datetime

def create_request(first_name, last_name, speciality, cv, letter):
  if first_name == '' or last_name == '' or len(speciality) == 0 or cv is None or letter is None:
    raise ValueError("All fields are requiered")
  date = datetime.now().strftime("%d %B %Y - %I:%M%p")
  return Request(0, first_name, last_name, speciality, cv, letter, status.PENDING, date)

class Request:
  def __init__(self, id: int, first_name: str, last_name: str, speciality: list, cv, letter, status: status, date):
    self.id = id
    self.first_name = first_name
    self.last_name = last_name
    self.speciality = speciality
    self.cv = cv
    self.letter = letter
    self.status = status
    self.date = date  
  