import bd
import use_levenstein as ul
import random

# Реализация стратегии частное-общее, выбор более "сложных" правил
def get_least_common(string, group=-1, priority=-1):
    rules = bd.get_rules_by_parameters(string, group, priority)
    if len(rules) == 0:
        return None
    mp_rule = rules[0]
    for rule in rules:
        if ul.check_sample(rule.sample, mp_rule.sample):
            continue
        elif ul.check_sample(mp_rule.sample, rule.sample):
            mp_rule = rule
        else:
            if rule.priority > mp_rule.priority:
                mp_rule = rule
    return mp_rule

# Реализация стратегии частное-общее, выбор более "простых" правил
def get_most_common(string, group=-1, priority=-1):
    rules = bd.get_rules_by_parameters(string, group, priority)
    mc_rule = rules[0]
    for rule in rules:
        if ul.check_sample(rule.sample, mc_rule.sample):
            mc_rule = rule
        elif ul.check_sample(mc_rule.sample, rule.sample):
            continue
        else:
            if rule.priority > mc_rule.priority:
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
        if rule.timestamp > latest_rule.timestamp:
            latest_rule = rule
    return latest_rule






