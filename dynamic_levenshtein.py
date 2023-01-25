import numpy as np
from numpy import unravel_index

def calc_lev_with_blanks(s1, s2):
    n = len(s1)
    m = len(s2)
    # Инициализация матрицы
    a = [[0 for x in range(m)] for y in range(n)]
    F = np.array(a)
    for i in reversed(range(n)):
        for j in reversed(range(m)):
            if s1[i] == s2[j] or s1[i].isupper() or s2.isupper():
                if i < n-1 and j < m-1:
                    F[i][j] = max(map(max, F[i+1:, j+1:])) + 1
                else:
                    F[i][j] = 1
    for line in F:
        print(line)

    rules = build_rules(s1, s2, F, True)
    print(rules)
    #print(vars)




def calc_lev_without_blanks(s1, s2):
    n = len(s1)
    m = len(s2)
    # Инициализация матрицы
    a = [[0 for x in range(m)] for y in range(n)]
    F = np.array(a)
    for i in reversed(range(n)):
        for j in reversed(range(m)):
            if s1[i] == s2[j] or s1[i].isupper() or s2.isupper():
                if i < n - 1 and j < m - 1:
                    if i == n-2 or j == m-2:
                        F[i][j] = F[i + 1][j + 1] + 1
                    else:
                        F[i][j] = max(max(map(max, F[i + 2:, j + 2:])), F[i + 1][j + 1]) + 1
                else:
                    F[i][j] = 1
    for line in F:
        print(line)

    rules = build_rules(s1, s2, F, False)
    print(rules)
    return rules

# Пострение правил на основе двух строк
def build_rules(s1, s2, F, blanks):
    n = len(s1)
    m = len(s2)
    results = {}
    i = 0
    j = 0
    counted_lev_distance = max(map(max, F))
    for i in range(n):
        for j in range(m):
            if F[i][j] == counted_lev_distance:
                vars = {"X": ("", ""), "Y": ("", ""), "Z": ("", ""),
                        "A": ("", ""), "B": ("", ""), "C": ("", ""),
                        "D": ("", ""), "E": ("", ""), "F": ("", ""), "G": ("", "")}
                res = build_rule(s1, s2, F, vars, blanks, i, j)
                results[res] = vars
    return results


def build_rule(s1, s2, F, vars, blanks, i, j):
    n = len(s1)
    m = len(s2)
    prev_i = i
    prev_j = j
    res = ""
    while i < n and j < m:
        if F[i][j] != 0:
            # максимальный элемент
            if i == prev_i or j == prev_j:
                if i != 0 or j != 0:
                    # цикл добавления переменной в случае если начало не совпадает
                    for key in vars.keys():
                        if vars[key] == ("", ""):
                            if i != 0:
                                vars[key] = (s1[0:i], "")
                            if j != 0:
                                vars[key] = (vars[key][0], s2[0:j])
                            res += key
                            break
                res += s2[j]
                i, j = find_max_pos(F[i+1:, j+1:], n, m, blanks)
            # проверка чтобы не выходить за границы
            elif (i == n-2 or j == m-2) or (i == n-1 or j == m-1):
                # случай для заполнения переменных
                if i != prev_i+1 or j != prev_j+1:
                    # цикл добавления переменной
                    for key in vars.keys():
                        if vars[key] == ("", ""):
                            if i != prev_i + 1:
                                vars[key] = (s1[prev_i+1:i], "")
                            if j != prev_j + 1:
                                vars[key] = (vars[key][0], s2[prev_j+1:j])
                            res += key
                            break
                res += s2[j]
                prev_i, prev_j = i, j
                i += 1
                j += 1
            # Случай, при котором всё ок
            elif i == prev_i+1 and j == prev_j+1:
                res += s2[j]
                prev_i, prev_j = i, j
                i, j = find_max_pos(F[i + 1:, j + 1:], n, m, blanks)
                # случай для заполнения переменных (обычный)
            elif i != prev_i+1 or j != prev_j+1:
                # цикл добавления переменной
                for key in vars.keys():
                    if vars[key] == ("", ""):
                        if i != prev_i+1:
                            vars[key] = (s1[prev_i+1:i], "")
                        if j != prev_j+1:
                            vars[key] = (vars[key][0], s2[prev_j+1:j])
                        res += key
                        break
                res += s2[j]
                prev_i, prev_j = i, j
                i, j = find_max_pos(F[i + 1:, j + 1:], n, m, blanks)
    return res



def find_max_pos(a, n, m, blanks):
    shape = a.shape
    max_elem = a.max()
    max_i = 0
    max_j = 0
    if blanks:
        for i in range(shape[0]):
            for j in range(shape[1]):
                if a[i][j] == max_elem:
                    max_i = i
                    max_j = j
                    break
    else:
        tmp = a[1:, 1:]
        if a[0][0] >= tmp.max():
            max_i, max_j = 0, 0
        else:
            max_elem = tmp.max()
            for i in range(shape[0]-1):
                for j in range(shape[1]-1):
                    if tmp[i][j] == max_elem:
                        max_i = i
                        max_j = j
                        break
            shape = (shape[0]-1, shape[1]-1)
    max_i += n-shape[0]
    max_j += m-shape[1]
    print(max_i, max_j)
    return max_i, max_j

# Экспериментальная часть !!!!!!!!!!
# Вариант build_rule с возможностью сопоставлять переменные (экспериментальный)
def build_rule_with_variables(s1, s2, F, vars, blanks, i, j):
    n = len(s1)
    m = len(s2)
    prev_i = i
    prev_j = j
    res = ""
    while i < n and j < m:
        if F[i][j] != 0:
            # максимальный элемент
            if i == prev_i or j == prev_j:
                if i != 0 or j != 0:
                    # цикл добавления переменной в случае если начало не совпадает
                    for key in vars.keys():
                        if vars[key] == ("", ""):
                            if i != 0:
                                vars[key] = (s1[0:i], "")
                            if j != 0:
                                vars[key] = (vars[key][0], s2[0:j])
                            res += key
                            break
                res += s2[j]
                i, j = find_max_pos(F[i+1:, j+1:], n, m, blanks)
            # проверка чтобы не выходить за границы
            elif (i == n-2 or j == m-2) or (i == n-1 or j == m-1):
                # случай для заполнения переменных
                if i != prev_i+1 or j != prev_j+1:
                    # цикл добавления переменной
                    for key in vars.keys():
                        if vars[key] == ("", ""):
                            if i != prev_i + 1:
                                vars[key] = (s1[prev_i+1:i], "")
                            if j != prev_j + 1:
                                vars[key] = (vars[key][0], s2[prev_j+1:j])
                            res += key
                            break
                res += s2[j]
                prev_i, prev_j = i, j
                i += 1
                j += 1
            # Случай, при котором всё ок
            elif i == prev_i+1 and j == prev_j+1:
                # эксперименитальная часть
                if s1[i].isupper():
                    for key in vars.keys():
                        if vars[key] == ("", ""):
                            vars[key] = ("", s2[j])
                            res += key
                            break
                else:
                    res += s2[j]
                # конец эксп части
                prev_i, prev_j = i, j
                i, j = find_max_pos(F[i + 1:, j + 1:], n, m, blanks)
                # случай для заполнения переменных (обычный)
            elif i != prev_i+1 or j != prev_j+1:
                # цикл добавления переменной
                for key in vars.keys():
                    if vars[key] == ("", ""):
                        if i != prev_i+1:
                            vars[key] = (s1[prev_i+1:i], "")
                        if j != prev_j+1:
                            vars[key] = (vars[key][0], s2[prev_j+1:j])
                        res += key
                        break
                # эксперименитальная часть
                if s1[i].isupper():
                    for key in vars.keys():
                        if vars[key] == ("", ""):
                            vars[key] = ("", s2[j])
                            res += key
                            break
                else:
                    res += s2[j]
                # конец эксп части
                prev_i, prev_j = i, j
                i, j = find_max_pos(F[i + 1:, j + 1:], n, m, blanks)
    return res

def calc_lev_with_blanks_exp(s1, s2):
    n = len(s1)
    m = len(s2)
    # Инициализация матрицы
    a = [[0 for x in range(m)] for y in range(n)]
    F = np.array(a)
    for i in reversed(range(n)):
        for j in reversed(range(m)):
            if s1[i] == s2[j] or s1[i].isupper() or s2.isupper():
                if i < n-1 and j < m-1:
                    F[i][j] = max(map(max, F[i+1:, j+1:])) + 1
                else:
                    F[i][j] = 1
    for line in F:
        print(line)

    rules = build_rules_with_variables(s1, s2, F, True)
    print(rules)
    #print(vars)

# Пострение правил на основе двух строк
# Эксп
def build_rules_with_variables(s1, s2, F, blanks):
    n = len(s1)
    m = len(s2)
    results = {}
    i = 0
    j = 0
    counted_lev_distance = max(map(max, F))
    for i in range(n):
        for j in range(m):
            if F[i][j] == counted_lev_distance:
                vars = {"X": ("", ""), "Y": ("", ""), "Z": ("", ""),
                        "A": ("", ""), "B": ("", ""), "C": ("", ""),
                        "D": ("", ""), "E": ("", ""), "F": ("", ""), "G": ("", "")}
                res = build_rule_with_variables(s1, s2, F, vars, blanks, i, j)
                res = join_variables(res, vars)
                results[res] = vars
    return results

def join_variables(s, vars):
    n = len(s)
    res = ""
    for i in reversed(range(1, n)):
        if s[i].isupper() and s[i-1].isupper():
            vars[s[i-1]] = (vars[s[i-1]][0]+vars[s[i]][0], vars[s[i-1]][1]+vars[s[i]][1])
            vars[s[i]] = ("", "")
        else:
            res += s[i]
    res += s[0]
    return res[::-1]



#calc_lev_with_blanks("гомеопатия", "геометрия")
calc_lev_without_blanks("гомеопатия", "геометрия")
calc_lev_without_blanks("баран", "баклан")
calc_lev_with_blanks_exp("баXан", "баклан")
