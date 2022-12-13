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

    rules = build_rules(s1, s2, F, vars, True)
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

    rules = build_rules(s1, s2, F, vars, False)
    print(rules)
    #print(vars)

def build_rules(s1, s2, F, vars, blanks):
    n = len(s1)
    m = len(s2)
    prev_i = 0
    prev_j = 0
    results = {}
    i = 0
    j = 0
    counted_lev_distance = max(map(max, F))
    for i in range(n):
        for j in range(m):
            if F[i][j] == counted_lev_distance:
                vars = {"X": ("", ""), "Y": ("", ""), "Z": ("", "")}
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
                    for key in vars.keys():
                        if vars[key] == ("", ""):
                            if i != 0:
                                vars[key] = (s1[0:i], "")
                            if j != 0:
                                vars[key] = (vars[key][0], s2[0:j])
                            res += key
                            break
                res += s1[i]
                i, j = find_max_pos(F[i+1:, j+1:], n, m, blanks)
            # проверка чтобы не выходить за границы
            elif (i == n-2 or j == m-2) or (i == n-1 or j == m-1):
                # случай для заполнения переменных
                if i != prev_i+1 or j != prev_j+1:
                    for key in vars.keys():
                        if vars[key] == ("", ""):
                            if i != prev_i + 1:
                                vars[key] = (s1[prev_i+1:i], "")
                            if j != prev_j + 1:
                                vars[key] = (vars[key][0], s2[prev_j+1:j])
                            res += key
                            break
                res += s1[i]
                prev_i, prev_j = i, j
                i += 1
                j += 1
            # случай для заполнения переменных
            elif i == prev_i+1 and j == prev_j+1:
                res += s1[i]
                prev_i, prev_j = i, j
                i, j = find_max_pos(F[i + 1:, j + 1:], n, m, blanks)
            elif i != prev_i+1 or j != prev_j+1:
                for key in vars.keys():
                    if vars[key] == ("", ""):
                        if i != prev_i+1:
                            vars[key] = (s1[prev_i+1:i], "")
                        if j != prev_j+1:
                            vars[key] = (vars[key][0], s2[prev_j+1:j])
                        res += key
                        break
                res += s1[i]
                prev_i, prev_j = i, j
                i, j = find_max_pos(F[i + 1:, j + 1:], n, m, blanks)
    return res



def find_max_pos(a, n, m, blanks):
    if blanks:
        i, j = unravel_index(a.argmax(), a.shape)
    else:
        tmp = a[1:, 1:]
        if a[0][0] > tmp.max():
            i, j = 0, 0
        else:
            i, j = unravel_index(tmp.argmax(), tmp.shape)
            i += 1
            j += 1
    shape = a.shape
    i += n-shape[0]
    j += m-shape[1]
    return i, j


calc_lev_with_blanks("гомеопатия", "геометрия")
calc_lev_without_blanks("гомеопатия", "геометрия")
#calc_lev_without_blanks("баXан", "баклан")