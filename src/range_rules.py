import bd
import use_levenstein as ul
import random

# Реализация стратегии частное-общее, выбор более "сложных" правил
def get_least_common(string, group=-1, priority=-1):
    rules = bd.get_rules_by_parameters(string, group, priority)
    mp_rule = rules[0]
    for rule in rules:
        if ul.check_sample(rule, mp_rule):
            continue
        elif ul.check_sample(mp_rule, rule):
            mp_rule = rule
        else:
            if rule['Priority'] > mp_rule['Priority']:
                mp_rule = rule
    return mp_rule

# Реализация стратегии частное-общее, выбор более "простых" правил
def get_most_common(string, group=-1, priority=-1):
    rules = bd.get_rules(string, group, priority)
    mc_rule = rules[0]
    for rule in rules:
        if ul.check_sample(rule, mc_rule):
            mc_rule = rule
        elif ul.check_sample(mc_rule, rule):
            continue
        else:
            if rule['Priority'] > mc_rule['Priority']:
                mc_rule = rule
    return mc_rule

# Выбор случайного правила с заданными параметрами
def get_random_rule(string, group=-1, priority=-1):
    rules = bd.get_rules_by_parameters(string, group, priority)
    rule = random.choice(rules)
    return rule

# Выбор последнего добавленного правила
def get_latest_rule(string, group=-1, priority=-1):
    rules = bd.get_rules_by_parameters(string, group, priority)
    latest_rule = rules[0]
    for rule in rules:
        if rule['Timestamp'] > latest_rule['Timestamp']:
            latest_rule = rule

    return latest_rule






