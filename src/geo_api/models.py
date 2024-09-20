from peewee import Model, CharField, IntegerField

from .configuration import DATABASE


class ApiUser(Model):
    name = CharField(unique=True)
    city = IntegerField()
    postal_code = CharField()

    class Meta:
        database = DATABASE
