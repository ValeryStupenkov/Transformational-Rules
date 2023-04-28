from peewee import *
import Group as gr

# Здесь будет строка подключения
conn = SqliteDatabase('transformrules.db')

class TransformRule(Model):
    rule_id = AutoField()
    sample = TextField()
    result = TextField()
    group = ForeignKeyField(gr.Group, backref='Rules')
    priority = IntegerField()
    blanks = IntegerField()
    timestamp = DateTimeField()

    class Meta:
        database = conn
        table_name = 'Rules'
