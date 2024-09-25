from pydantic import BaseModel
import datetime
import json


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
    timestamp: datetime.datetime or str

    class Config:
        orm_mode = True
        from_attributes = True

    def __dict__(self):
        dict_ = dict(self)
        # dict_['timestamp'] = dict_['timestamp'].strftime("%I:%M %p, %d/%m")
        return dict_

    def to_json(self):
        dict_ = dict(self)
        dict_['timestamp'] = str(dict_['timestamp'])
        return json.dumps(dict_)
