from peewee import *

conn = SqliteDatabase('transformrules.bd')

class BaseModel(Model):
    class Meta:
        database = conn

class Group(BaseModel):
    group_id = AutoField(column_name='GroupID')
    group_name = TextField(column_name='Name')

    class Meta:
        table_name = 'Groups'