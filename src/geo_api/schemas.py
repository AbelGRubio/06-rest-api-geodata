from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str = ''
    postal_code: str = ''
    city: str = '-'

    class Config:
        orm_mode = True


class ShowUserSchema(BaseModel):
    id: str = ''
    name: str = ''
    postal_code: str = ''
    city: str = '-'

    class Config:
        orm_mode = True