from peewee import *
import TransformRule as tr
import Group as gr
import use_levenstein as ul
from datetime import datetime

# Получить правило по id
def get_rule_by_id(id):
    rule = tr.TransformRule.get(tr.TransformRule.rule_id == id)
    return rule

# Возвращает все правила
def get_all_rules():
    query = tr.TransformRule.select()
    rules_selected = query.dicts().execute()
    return rules_selected

def get_all_groups():
    query = gr.Group.select()
    groups = query.execute()
    return groups

# Возвращает id правила, если оно есть в базе, -1 иначе
def get_rule_id(rule):
    query = tr.TransformRule.select().where(tr.TransformRule.sample == rule[0] and tr.TransformRule.result == rule[1])
    rule = query.execute()
    if len(rule) > 0:
        return rule.rule_id
    else:
        return -1

# Создание правила в бд
def create_rule_from_strings(sample, result, group, priority):
    try:
        gr.Group.select().where(gr.Group.group_id == group).get()
    except DoesNotExist:
        gr.Group.create(group_id=group, group_name="")
    tr.TransformRule.create(sample=sample, result=result, group=group, priority=priority, timestamp=datetime.now())

# Создание правила в бд на основе пары
def create_rule(rule, group, priority):
    try:
        gr.Group.select().where(gr.Group.group_id == group).get()
    except DoesNotExist:
        gr.Group.create(group_id=group, group_name="")
    tr.TransformRule.create(sample=rule[0], result=rule[1], group=group, priority=priority, timestamp=datetime.now())

# Удаление правила по id
def delete_rule_by_id(id):
    rule = tr.TransformRule.get(tr.TransformRule.rule_id == id)
    rule.delete_instance()


# Возвращает все правила, примениемые к строке
def get_rules(string):
    query = tr.TransformRule.select()
    rules_selected = query.execute()
    rules = []
    for rule in rules_selected:
        blanks = rule.blanks == 1
        if ul.check_sample(rule.sample, string, blanks):
            rules.append(rule)
    return rules

# Возвращает правила, применимые к строке с указанными группой и приоритетом
def get_rules_by_parameters(string, group=-1, priority=-1):
    if group != -1 and priority != -1:
        query = tr.TransformRule.select().where(tr.TransformRule.group == group and tr.TransformRule.priority == priority)
    elif group != -1:
        query = tr.TransformRule.select().where(tr.TransformRule.group == group)
    elif priority != -1:
        query = tr.TransformRule.select().where(tr.TransformRule.priority == priority)
    else:
        query = tr.TransformRule.select()
    rules_selected = query.execute()
    rules = []
    for rule in rules_selected:
        blanks = rule.blanks == 1
        if ul.check_sample(rule.sample, string):
            rules.append(rule)
    return rules

# Создание группы в бд
def create_group(name):
    gr.Group.create(group_name=name)

# инициализация базы данных
def create_rule_base(name):
   database = SqliteDatabase(name + ".db")
   database.connect()
   database.create_tables([tr.TransformRule, gr.Group])
   gr.Group.create(group_id=1, group_name="Общая")