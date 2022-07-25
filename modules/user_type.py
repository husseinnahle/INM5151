from backports.strenum import StrEnum

class user_type(StrEnum):
    ADMIN = 'ADMIN',
    INSTRUCTOR = 'INSTRUCTOR',
    MEMBER = "MEMBER",
    STANDARD = "STANDARD"
