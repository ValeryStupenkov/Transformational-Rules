from peewee import *

conn = SqliteDatabase('transformrules.db')


class Group(Model):
    group_id = AutoField()
    group_name = TextField()

    class Meta:
        database = conn
        table_name = 'Groups'