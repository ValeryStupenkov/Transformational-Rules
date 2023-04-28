from peewee import *

import Group
import TransformRule

def create_rule_base(name):
   database = SqliteDatabase(name + ".db")
   database.create_tables([TransformRule, Group])
