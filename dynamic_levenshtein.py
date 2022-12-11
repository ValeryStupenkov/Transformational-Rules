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

    vars = {"X": ("", ""), "Y": ("", ""), "Z": ("", "")}
    rule = build_rule(s1, s2, F, vars, True)
    print(rule)
    print(vars)




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

    vars = {"X": ("", ""), "Y":("", ""), "Z":("", "")}
    rule = build_rule(s1, s2, F, vars, False)
    print(rule)
    print(vars)

def build_rule(s1, s2, F, vars, blanks):
    n = len(s1)
    m = len(s2)
    prev_i = 0
    prev_j = 0
    res = ""
    i = 0
    j = 0
    while i < n and j < m:
        if F[i][j] != 0:
            if i == 0 or j == 0:
                res += s1[i]
                i, j = find_max_pos(F[i+1:, j+1:], n, m, blanks)
            elif (i == n-2 or j == m-2) or (i == n-1 or j == m-1):
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


#calc_lev_with_blanks("гомеопатия", "геометрия")
calc_lev_without_blanks("гомеопатия", "геометрия")
#calc_lev_without_blanks("баXан", "баклан")