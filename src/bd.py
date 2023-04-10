from peewee import *
import TransformRule as tr
import Group
import use_levenstein as ul
from datetime import datetime
import sqlite3

# Получить правило по id
def get_rule_by_id(id):
    rule = tr.TransformRule.get(tr.TransformRule.rule_id == id)
    return rule

# Возвращает все правила
def get_all_rules():
    query = tr.TransformRule.select()
    rules_selected = query.dicts().execute()
    return rules_selected

# Возвращает id правила, если оно есть в базе, -1 иначе
def get_rule_id(rule):
    query = tr.TransformRule.select().where(tr.TransformRule.sample == rule[0] and tr.TransformRule.result == rule[1])
    rule = query.dicts().execute()
    if len(rule) > 0:
        return rule[0]['RuleId']
    else:
        return -1

# Создание правила в бд
def create_rule_from_strings(sample, result, group=1, priority=1):
    tr.TransformRule.create(sample=sample, result=result, group=group, priority=priority, timestamp=datetime.now())

# Создание правила в бд на основе пары
def create_rule(rule, group=1, priority=1):
    tr.TransformRule.create(sample=rule[0], result=rule[1], group=group, priority=priority, timestamp=datetime.now())

# Удаление правила по id
def delete_rule_by_id(id):
    rule = tr.TransformRule.get(tr.TransformRule.rule_id == id)
    rule.delete_instance()


# Возвращает все правила, примениемые к строке
def get_rules(string):
    query = tr.TransformRule.select().where(ul.check_sample(string, tr.TransformRule.sample) == True)
    rules_selected = query.dicts().execute()
    return rules_selected

def get_rules_by_parameters(string, group=-1, priority=-1):
    if group != -1 and priority != -1:
        query = tr.TransformRule.select().where(
            ul.check_sample(string, tr.TransformRule.sample) == True and tr.TransformRule.group == group and tr.TransformRule.priority==priority)
    elif group != -1:
        query = tr.TransformRule.select().where(
            ul.check_sample(string, tr.TransformRule.sample) == True and tr.TransformRule.group == group)
    elif priority != -1:
        query = tr.TransformRule.select().where(
            ul.check_sample(string, tr.TransformRule.sample) == True and tr.TransformRule.priority == priority)
    else:
        query = tr.TransformRule.select().where(
            ul.check_sample(string, tr.TransformRule.sample) == True)
    rules_selected = query.dicts().execute()
    return rules_selected

# Создание группы в бд
def create_group(name):
    Group.create(group_name=name)

# инициализация базы данных с указанным именем
def create_rule_base(name):
    fullname = name + ".bd"
    connection = sqlite3.connect('transformrules.db')

    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Rules
         (RULEID INT PRIMARY KEY     NOT NULL,
         SAMPLE           TEXT    NOT NULL,
         RESULT           TEXT     NOT NULL,
         GROUPID            INT,
         PRIORITY INT,
         TIMESTAMP TIMESTAMP);''')
    connection.commit()

    cursor.execute(''' CREATE TABLE IF NOT EXISTS Groups
    ( GROUPID INT PRIMARY KEY    NOT NULL,
     NAME             TEXT      NOT NULL
    );''')
    connection.commit()

    connection.close()
