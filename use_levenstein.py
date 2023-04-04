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

# Вернуть правую часть правила с подставленными значениями переменных
def get_result_of_rule(sample, vars):
    res = ""
    for i in range(len(sample)):
        if sample[i].isupper():
            res += vars[sample[i]]
        else:
            res += sample[i]
    return res

# Создание правила на основе образца и значений переменных
def make_rule_from_sample(s, vars):
    tmp_vars = {"X": "", "Y": "", "Z": "",
            "A": "", "B": "", "C": "",
            "D": "", "E": "", "F": "", "G": ""}
    last_var = "X"
    res1 = ""
    res2 = ""
    for i in range(len(s)):
        # Вместо переменной ставим её значение
        if s[i].isupper():
            res1 += vars[s[i]][0]
            res2 += vars[s[i]][1]
        # Вместо символов ставим переменные
        elif i == 0 and s[i].islower():
            for k in tmp_vars.keys():
                if tmp_vars[k] == "":
                    tmp_vars[k] += s[i]
                    res1 += k
                    res2 += k
                    last_var = k
                    break
        # Вместо символов дописываем в переменную
        elif s[i-1].islower() and s[i].islower():
            tmp_vars[last_var] += s[i]
        # Вместо символа идущего после вставки значения пишем переменную
        elif s[i-1].isupper() and s[i].islower():
            for k in tmp_vars.keys():
                if tmp_vars[k] == "":
                    res1 += k
                    res2 += k
                    tmp_vars[k] += s[i]
                    last_var = k
                    break
    res = tuple([res1, res2])
    print(tmp_vars)
    return res

