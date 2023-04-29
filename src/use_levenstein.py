import dynamic_levenshtein as ds

# Правила должны храниться в виде пар, в коде должны быть в виде tuple

# Метод для проверки соответствия левой части правила образцу
def check_sample(sample, rule):
    rules = ds.calc_lev_with_steps(sample, rule)
    for r in rules.keys():
        if sample == r:
            return True
    return False

# Метод для создания новых образцов на основе двух обычных строк
def create_new_samples(s1, s2, blanks):
    if blanks:
        samples = ds.calc_lev_with_blanks(s1, s2)
    else:
        samples = ds.calc_lev_without_blanks(s1, s2)
    return samples

# Создание новых образцов на основе существующих образцов
def create_new_samples(sample, s):
    samples = ds.calc_lev_with_steps(sample, s)
    return samples

# Создание более общих образцов
def find_most_common(s1, s2):
    results = ds.calc_lev_with_steps(s1, s2)
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
            res += vars[sample[i]][1]
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

# Создание правил на основе двух входных строк
def create_rules_from_strings(s1, s2, blanks):
    if blanks:
        samples = ds.calc_lev_with_blanks(s1, s2)
    else:
        samples = ds.calc_lev_without_blanks(s1, s2)

    rules = []
    # Составляем правила, записываем в список пар
    for s in samples.keys():
        # s - образец; sample[s] - словарь с переменными
        rules.append(make_rule_from_sample(s, samples[s]))
    return rules

# Создаёт правила на основе существующих
#TODO fix или удалить
def create_rule_from_rules(rule1, rule2):
    left_samples = ds.calc_lev_with_steps(rule1[0], rule2[0])
    right_samples = ds.calc_lev_with_steps(rule1[1], rule2[1])
    new_rules = []
    for left in left_samples.keys():
        for right in right_samples.keys():
            new_rules.append(tuple([left, right]))
    return new_rules

# Возвращает заполненные переменные
def fill_variables(sample, string):
    samples = ds.calc_lev_with_steps(sample, string)
    vars = samples[sample]
    return vars

# Создаёт более общие правила на основе образцов
def create_rule_from_samples(sample1, sample2, vars1, vars2):
    rules = []
    new_samples = ds.calc_lev_with_steps(sample1, sample2)
    for sample in new_samples.keys():
        tmp_vars = new_samples[sample]
        for key in tmp_vars.keys():
            tmp_vars[key] = (insert_variables_values(tmp_vars[key][0], vars1), insert_variables_values(tmp_vars[key][1], vars2))
        rules.append(make_rule_from_sample(sample, tmp_vars))
    return rules

# string s
# dict vars
# Вставляет значения переменных в строку
def insert_variables_values(s, vars):
    res = ""
    for i in range(len(s)):
        if s[i].isupper():
            res += vars[s[i]]
        else:
            res += s[i]
    return res