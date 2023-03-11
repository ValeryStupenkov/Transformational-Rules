import dynamic_levenshtein as ld

#Правила должны храниться в виде пар, в коде должны быть в виде tuple

# Метод для проверки соответствия левой части правила образцу
def check_sample(sample, rule):
    rules = ld.calc_lev_with_steps(sample, rule)
    for rule in rules.keys():
        if sample == rule:
            return True
    return False

# Метод для создания новых образцов на основе двух обычных строк
def create_new_samples(s1, s2, blanks):
    if blanks:
        samples = ld.calc_lev_with_blanks(s1, s2)
    else:
        samples = ld.calc_lev_without_blanks(s1, s2)
    return samples

# Создание новых образцов на основе существующих образцов
def create_new_samples(sample, s):
    samples = ld.calc_lev_with_steps(sample, s)
    return samples

# Создание более общих образцов
def find_most_common(s1, s2):
    results = ld.calc_lev_with_steps(s1, s2)
    return results

# Метод для создания правила "руками"
def create_rule(sample, result):
    return (sample, result)

# rule это tuple вида (sample, result)
def create_common_rules(rule1, rule2):
    new_samples = create_new_samples(rule1[0], rule2[0])
    new_results = create_new_samples(rule1[1], rule2[1])
    new_rules = []
    # Объединение полученных образцов в правила
    for sample in new_samples:
        for result in new_results:
            new_rules += (sample, result)

    return new_rules
