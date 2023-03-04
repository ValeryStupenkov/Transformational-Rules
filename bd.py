from peewee import *
import TransformRule
import use_levenstein as ul

def get_rule_by_id(id):
    rule = TransformRule.get(TransformRule.rule_id == id)
    return rule

# В этом разделе должна быть и реализация стратегий ранжировния

# Просто возвращает первое совпавшее правило
def get_rule(string):
    query = TransformRule.select()
    rules_selected = query.dicts().execute()
    for rule in rules_selected:
        if ul.check_sample(string, rule['sample']):
            return rule

# Создание правила в бд
def create_rule(sample, result):
    TransformRule.create(sample=sample, result=result)

# Удаление правила по id
def delete_rule_by_id(id):
    rule = TransformRule.get(TransformRule.rule_id == id)
    rule.delete_instance()


# Возвращает все правила, примениемые к строке
def get_rules(string):
    query = TransformRule.select().where(ul.check_sample(string, TransformRule.sample) == True)
    rules_selected = query.dicts().execute()
    return rules_selected