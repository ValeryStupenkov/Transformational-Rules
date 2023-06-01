import bd
import use_levenstein as us
import range_rules as rr
import TransformationalRule as tr


def create_rule(left, right, group=1, priority=1):
    '''
    Создать правило в базу данных
    :param left: условие применимости правила
    :param right: результат применения правила
    :param group: номер группы
    :param priority: приоритет
    :return: объект TransformationalRule
    '''
    bd.create_rule_from_strings(left, right, group, priority)
    return tr.TransformationalRule(left, right)

def get_rule_by_id(id):
    '''
    Получить правило по указанному id
    :param id:
    :return: правило
    '''
    result = bd.get_rule_by_id(id)
    rule = tr.TransformationalRule(result.sample, result.result)
    return rule

def get_rule(string, strategy, group=-1, priority=-1):
    '''
    Получить правило, подходящее для указанной строки с указанной стратегией
    :param string: строка
    :param strategy: стратегия выбора правил
    :param group: группа
    :param priority: приоритет
    :return: правило
    '''
    if not isinstance(strategy, rr.Strategy):
        raise TypeError('startegy must be an instance of Strategy Enum')

    if strategy == rr.Strategy.LEAST_COMMON:
        rule = rr.get_least_common(string, group, priority)
    elif strategy == rr.Strategy.MOST_COMMON:
        rule = rr.get_most_common(string, group, priority)
    elif strategy == rr.Strategy.TIMESTAMP:
        rule = rr.get_latest_rule(string, group, priority)
    elif strategy == rr.Strategy.RANDOM:
        rule = rr.get_random_rule(string, group, priority)
    if rule is None:
        print("Не нашлось подходящего правила")
        return tr.TransformationalRule("", "")

    return tr.TransformationalRule(rule.sample, rule.result)



# Получить все правила из базы
def get_all_rules():
    '''
    Получить все правила из базы
    '''
    rules = bd.get_all_rules()
    all_rules = []
    for rule in rules:
        rule_data = {}
        for key in rule.keys():
            rule_data[key] = rule[key]
        all_rules.append(rule_data)
    return all_rules

# Получить все группы из базы
def get_all_groups():
    '''
    Получить все группы из базы
    '''
    groups = bd.get_all_groups()
    all_groups = []
    for group in groups:
        group_data = {}
        for key in group.keys():
            group_data[key] = group[key]
        all_groups.append(group_data)
    return all_groups


def get_and_use_rule(string, strategy, group=1, priority=1):
    '''
    Получить подходящее правило с помощью выбранной стратегии ранжирования и вернуть результат его применения
    :param string: строка
    :param strategy: стратегия выбора правил
    :param group: группа
    :param priority: приоритет
    :return: результат применения правила
    '''
    if not isinstance(strategy, rr.Strategy):
        raise TypeError('startegy must be an instance of Strategy Enum')

    if strategy == rr.Strategy.LEAST_COMMON:
        rule = rr.get_least_common(string, group, priority)
    elif strategy == rr.Strategy.MOST_COMMON:
        rule = rr.get_most_common(string, group, priority)
    elif strategy == rr.Strategy.TIMESTAMP:
        rule = rr.get_latest_rule(string, group, priority)
    elif strategy == rr.Strategy.RANDOM:
        rule = rr.get_random_rule(string, group, priority)
    if rule is None:
        print("Не нашлось подходящего правила")
        return string
    # Получаем значения переменных
    vars = us.fill_variables(rule.sample, string)

    # Получаем результат
    result = us.get_result_of_rule(rule.result, vars)
    return result

# Вернуть результат применения правила к строке
# str string - входная строка
# TransformationalRule rule - правило
def use_rule(string, rule):
    '''
    Вернуть результат применения правила к строке
    :param string: входная строка
    :param rule: правило
    :return: результирующая строка
    '''
    # Получаем значения переменных
    vars = us.fill_variables(rule.left, string)
    # Получаем результат
    result = us.get_result_of_rule(rule.right, vars)
    return result


# sample1, sample2: dict() {"sample": vars}
def create_rules_from_samples(sample1, sample2):
    '''
    Получает образцы с переменными и на их основе создаёт новые правила
    '''
    s1 = list(sample1.keys())[0]
    s2 = list(sample2.keys())[0]
    rules = us.create_rule_from_samples(s1, s2, sample1[s1], sample2[s2])
    return rules

def generate_rules(s1, s2, blanks=True):
    '''
    Создание правил на основе двух входных строк
    :param s1:
    :param s2:
    :param blanks:
    :return: трансформационные правила
    '''
    rules = us.create_rules_from_strings(s1, s2, blanks)
    return rules

def save_rule(rule, group=1, priority=1):
    '''
    Сохранить правило в базу данных
    :param rule: правило
    :param group: номер группы
    :param priority: приоритет
    :return:
    '''
    bd.create_rule(rule, group, priority)

def save_rules(rules, group=1, priority=1):
    '''
    Сохранить группу правил в базу данных
    :param rules: правила
    :param group: номер группы
    :param priority: приоритет
    :return:
    '''
    for rule in rules:
        bd.create_rule(rule, group, priority)

def delete_rule_by_id(id):
    '''
    Удаление правила из базы по id
    :param id:
    '''
    bd.delete_rule_by_id(id)

def delete_rule(rule):
    '''
    Поиск правила и удаление его из базы
    :param rule: правило
    '''
    id = bd.get_rule_id(rule)
    if id == -1:
        raise Exception("В базе данных отсутствут указанное правило")
    else:
        bd.delete_rule_by_id(id)
        print("Правило удалено")


def check_rule_in_database(rule):
    '''
    Возвращает id правила в базе, если правило есть в ней, иначе -1
    '''
    id = bd.get_rule_id(rule)
    return id

# string name
# Создать файл бд с указанным именем
def initiate_rule_base(path=" "):
    '''
    Создать файл бд с указанным именем
    '''
    bd.create_rule_base("transformrules")
    print("База правил инициализирована")

# Проверка соответствия строки образцу
def check_sample(sample, string):
    '''
    Проверка соответствия строки образцу
    '''
    return us.check_sample(sample, string)

# Создать промежуточные образцы на основе двух строк
def create_samples(left, right, blanks=True):
    '''
    Создать промежуточные образцы на основе двух строк
    '''
    samples = us.create_new_samples(left, right, blanks)
    return samples


