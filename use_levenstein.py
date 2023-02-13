import dynamic_levenshtein as ld

#Правила должны храниться в виде пар, в коде должны быть в виде tuple
# Метод для проверки соответствия левой части правили образцу
def check_sample(sample, rule):
    rules = ld.calc_lev_with_blanks_for_sample(sample, rule)
    for rule in rules.keys():
        if sample == rule:
            return True
    return False

# Метод для создания новых правил
def create_new_rules(s1, s2, blanks):
    if blanks:
        rules = ld.calc_lev_with_blanks(s1, s2)
    else:
        rules = ld.calc_lev_without_blanks(s1, s2)
    return rules

# Создание новых шаблонов
def create_new_sample(sample, s):
    rules = ld.calc_lev_with_blanks_for_sample(sample, s, True)
    return rules
