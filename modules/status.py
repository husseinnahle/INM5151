from backports.strenum import StrEnum

class status(StrEnum):
    ACCEPTED = 'ACCEPTED',
    REFUSED = 'REFUSED'
    PENDING = 'PENDING'
