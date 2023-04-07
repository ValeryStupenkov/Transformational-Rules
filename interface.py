import bd
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

    # Получаем значения переменных
    vars = us.fill_variables(rule[0], string)

    # Получаем результат
    rule = us.get_result_of_rule(rule[1], vars)
    return rule

# Получает образцы с переменными и на ихх основе создаёт новые правила
# sample1, sample2: dict() {"sample": vars}
def create_new_rules(sample1, sample2):
    s1 = list(sample1.keys())[0]
    s2 = list(sample2.keys())[0]
    rules = us.create_rule_from_samples(s1, s2, sample1[s1], sample2[s2])
    return rules

def create_common_rules(rule1, rule2):
    rules = us.create_rule_from_rules(rule1, rule2)
    return rules

# Создание правил на основе двух входных строк
def create_rules(s1, s2, blanks=True):
    rules = us.create_rules_from_strings(s1, s2, blanks)
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
def check_rule_in_database(rule):
    id = bd.get_rule_id(rule)
    return id

# string name
# Создать файл бд с указанным именем
def initiate_rule_base(name):
    bd.create_rule_base(name)
    print("База правил инициализирована")

# Проверка соответствия строки образцу
def check_sample(sample, string):
    return us.check_sample(sample, string)

#print(create_rules("систематическая", "периодическая", True))

# TODO разобраться, как исправить коллизии в переменных
#print(create_common_rule(("сXстематY", "перXодY"), ("систXматY ", "пXриодY")))
sample1 = {"XомеYия": {"X":"ге", "Y":"тр"}}
sample2 = {"гXмеYия": {"X":"о", "Y":"опат"}}
print(create_common_rules(sample1, sample2))
