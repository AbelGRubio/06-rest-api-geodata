from pydantic import BaseModel
import datetime

class UserSchema(BaseModel):
    name: str = ''
    postal_code: str = ''
    city: str = '-'

    class Config:
        orm_mode = True
        from_attributes = True


class ShowUserSchema(BaseModel):
    id: int = 0
    name: str = ''
    postal_code: str = ''
    city: str = '-'

    class Config:
        orm_mode = True
        from_attributes = True


class MessageSchema(BaseModel):
    user_id: str = ''
    content: str = ''
    timestamp: datetime.datetime

    class Config:
        orm_mode = True
        from_attributes = True
