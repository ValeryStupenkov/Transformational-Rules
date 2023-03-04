from peewee import *

# Здесь будет строка подключения
conn = PostgresqlDatabase('')

class BaseModel(Model):
    class Meta:
        database = conn

class Rule(BaseModel):
    rule_id = AutoField(column_name='RuleID')
    sample = TextField(column_name='Sample')
    result = TextField(column_name='Result')

    class Meta:
        table_name = 'Rule'
