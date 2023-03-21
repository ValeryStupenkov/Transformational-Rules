from peewee import *
import TransformRule
import Group
import use_levenstein as ul
from datetime import datetime

# Получить правило по id
def get_rule_by_id(id):
    rule = TransformRule.get(TransformRule.rule_id == id)
    return rule

# Возвращает все правила
def get_all_rules():
    query = TransformRule.select()
    rules_selected = query.dicts().execute()
    return rules_selected

# Создание правила в бд
def create_rule(sample, result, group=1, priority=1):
    TransformRule.create(sample=sample, result=result, group=group, priority=priority, timestamp=datetime.now())

# Создание правила в бд на основе пары
def create_rule(rule, group=1, priority=1):
    TransformRule.create(sample=rule[0], result=rule[1], group=group, priority=priority, timestamp=datetime.now())

# Удаление правила по id
def delete_rule_by_id(id):
    rule = TransformRule.get(TransformRule.rule_id == id)
    rule.delete_instance()


# Возвращает все правила, примениемые к строке
def get_rules(string):
    query = TransformRule.select().where(ul.check_sample(string, TransformRule.sample) == True)
    rules_selected = query.dicts().execute()
    return rules_selected

def get_rules_by_parameters(string, group=-1, priority=-1):
    if group != -1 and priority != -1:
        query = TransformRule.select().where(
            ul.check_sample(string, TransformRule.sample) == True and TransformRule.group == group and TransformRule.priority==priority)
    elif group != -1:
        query = TransformRule.select().where(
            ul.check_sample(string, TransformRule.sample) == True and TransformRule.group == group)
    elif priority != -1:
        query = TransformRule.select().where(
            ul.check_sample(string, TransformRule.sample) == True and TransformRule.priority == priority)
    else:
        query = TransformRule.select().where(
            ul.check_sample(string, TransformRule.sample) == True)
    rules_selected = query.dicts().execute()
    return rules_selected

# Создание группы в бд
def create_group(name):
    Group.create(group_name=name)