from peewee import Model, CharField, IntegerField, TextField, DateTimeField

from .configuration import DATABASE
from datetime import datetime


class ApiUser(Model):
    name = CharField(unique=True)
    city = IntegerField()
    postal_code = CharField()

    class Meta:
        database = DATABASE


class Message(Model):

    user_id = CharField()
    content = TextField()
    timestamp = DateTimeField(default=datetime.now)

    class Meta:
        database = DATABASE
        table_name = "messages"


class UserConf(Model):
    user_id = CharField(unique=True)
    json = CharField()
    last_update = DateTimeField(default=datetime.now)

    class Meta:
        database = DATABASE
