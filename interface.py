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
    bd.create_rule_from_strings(left, right, group, priority)
    return (left, right)

# Получить правило по указанному id
def get_rule_by_id(id):
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
            new_rules.append(tuple([left, right]))
    #for rule in new_rules:
    #    bd.create_rule(rule, group)
    return new_rules

# Создание правил на основе двух входных строк
def create_rules(s1, s2, blanks=True, group=1, priority=1):
    # Получаем шаблоны с переменными в виде словаря, где шаблон - ключ
    if blanks:
        samples = ds.calc_lev_with_blanks(s1, s2)
    else:
        samples = ds.calc_lev_without_blanks(s1, s2)

    rules = []
    # Составляем правила, записываем в список пар
    for s in samples.keys():
        # s - образец; sample[s] - словарь с переменными
        rules.append(us.make_rule_from_sample(s, samples[s]))

    #for rule in rules:
    #    bd.create_rule(rule, group, priority)

    return rules

# Создать правило в базу данных
# Параметры:
# (string, string) rule - правило
# int group - номер группы
# int priority - приоритет
def save_rule(rule, group=1, priority=1):
    bd.create_rule(rule, group, priority)

# Создать правило в базу данных
# Параметры:
# [(string, string)] rules - правила
# int group - номер группы
# int priority - приоритет
def save_rules(rules, group=1, priority=1):
    for rule in rules:
        bd.create_rule(rule, group, priority)

# int id
# Удаление правила из базы по id
def delete_rule_by_id(id):
    bd.delete_rule_by_id(id)

# (string, string) rule
# Поиск правила и удаление его из базы
def delete_rule(rule):
    id = bd.get_rule_id(rule)
    if id == -1:
        raise Exception("В базе данных отсутствут указанное правило")
    else:
        bd.delete_rule_by_id(id)
        print("Правило удалено")


# (string, string) rule
# Возвращает id правила в базе, если правило есть в ней, иначе -1
def check_rule(rule):
    id = bd.get_rule_id(rule)
    return id

# string name
# Создать файл бд с указанными именем
def initiate_rule_base(name):
    bd.create_rule_base(name)
    print("База правил инициализирована")


#print(create_rules("геометрия", "гомеопатия"))
# TODO разобраться, как исправить коллизии в переменных
print(create_common_rule(("XомеYия", "XомеYий"), ("гXмеYия", "гXмеYий")))