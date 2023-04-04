from peewee import *

# Здесь будет строка подключения
conn = SqliteDatabase('transformrules.bd')

class BaseModel(Model):
    class Meta:
        database = conn

class TransformRule(BaseModel):
    rule_id = AutoField(column_name='RuleID')
    sample = TextField(column_name='Sample')
    result = TextField(column_name='Result')
    group = IntegerField(column_name='Group')
    priority = IntegerField(column_name='Priority')
    timestamp = DateField(column_name='TimeStamp')

    class Meta:
        table_name = 'Rules'
