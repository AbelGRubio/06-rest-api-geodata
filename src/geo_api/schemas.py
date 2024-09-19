from pydantic import BaseModel


class UserParameters(BaseModel):
    user: str = ''
    postal_code: str = ''


class UserFullParameters(BaseModel):
    user: str = ''
    postal_code: str = ''
    city: str = ''
