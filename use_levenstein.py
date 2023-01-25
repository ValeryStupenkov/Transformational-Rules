import dynamic_levenshtein as levdist

#Правила должны храниться в виде пар, в коде должны быть в виде tuple
# Метод для проверки соответствия левой части правили образцу
def check_sample(sample, rule, blanks):
    if blanks:
        rules = levdist.calc_lev_with_blanks(sample, rule[0])
    else:
        rules = levdist.calc_lev_without_blanks(sample, rule[0])
    for rule in rules.keys():
        if sample == rule:
            return True
    return False

# Метод для создания новых правил
def create_new_rules(s1, s2, blanks):
    if blanks:
        rules = levdist.calc_lev_with_blanks(s1, s2)
    else:
        rules = levdist.calc_lev_without_blanks(s1, s2)
    return rules