import bd
import dynamic_levenshtein as ds
import use_levenstein as us
import range_rules as rr
from enum import Enum


class Strategy(Enum):
    MOST_COMMON = "most_common"
    LEAST_COMMON = "least_common"
    TIMESTAMP = "timestamp"
    RANDOM = "random"

# Создать правило в базу данных
# Параметры:
# string left - условие применимости правила
# string right - результат применения правила
# int group - номер группы
# int priority - приоритет
def create_rule(left, right, group=1, priority=1):
    bd.create_rule(left, right, group, priority)
    return (left, right)

# Получить правило по указанному id
def get_rule(id):
    rule = bd.get_rule_by_id(id)
    return rule

# Получить правило, подходящее для указанной строки с указанной стратегией
# Параметры:
# string - строка
# strategy - enum стратегии выбора правил
# TODO
def get_rule(string, strategy, group=1, priority=1):
    if not isinstance(strategy, Strategy):
        raise TypeError('startegy must be an instance of Strategy Enum')
    return string

# Получить все правила из базы
def get_all_rules():
    rules = bd.get_all_rules()
    return rules

#TODO
# Получить подходящее правило с помощью выбранной стратегии ранжирования и вернуть результат его применения
def use_rule(string, strategy, group=1, priority=1):
    if not isinstance(strategy, Strategy):
        raise TypeError('startegy must be an instance of Strategy Enum')

    if strategy == Strategy.LEAST_COMMON:
        rule = rr.get_least_common(string, group, priority)
    elif strategy == Strategy.MOST_COMMON:
        rule = rr.get_most_common(string, group, priority)
    elif strategy == Strategy.TIMESTAMP:
        rule = rr.get_latest_rule(string, group, priority)
    elif strategy == Strategy.RANDOM:
        rule = rr.get_random_rule(string, group, priority)

    # Вернёт словарь с образцами и переменными
    samples = ds.calc_lev_with_steps(rule[0], string)
    # Получаем значения переменных
    vars = samples[rule[0]]

    # Получаем результат
    rule = us.get_result_of_rule(rule[1], vars)
    return rule


# TODO Создание общих правил на основе двух сущеcтвующих
def create_common_rule(rule1, rule2, blanks=True, group=1):
    left_samples = ds.calc_lev_with_steps(rule1[0], rule2[0])
    right_samples = ds.calc_lev_with_steps(rule1[1], rule2[1])
    new_rules = []
    for left in left_samples.keys():
        for right in right_samples.keys():
            new_rules += (left, right)
    for rule in new_rules:
        bd.create_rule(rule, group)
    return new_rules

