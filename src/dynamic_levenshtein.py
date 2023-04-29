import numpy as np
import build_rule_service as bs
import build_rule_by_steps as brs

def calc_lev_with_blanks(s1, s2):
    n = len(s1)
    m = len(s2)
    # Инициализация матрицы
    a = [[0 for x in range(m)] for y in range(n)]
    F = np.array(a)
    for i in reversed(range(n)):
        for j in reversed(range(m)):
            if s1[i] == s2[j] or s1[i].isupper() or (s1.isupper() and s2.isupper()):
                if i < n-1 and j < m-1:
                    F[i][j] = max(map(max, F[i+1:, j+1:])) + 1
                else:
                    F[i][j] = 1
    for line in F:
        print(line)

    rules = bs.build_rules(s1, s2, F, True)
    print(rules)
    return rules


def calc_lev_without_blanks(s1, s2):
    n = len(s1)
    m = len(s2)
    # Инициализация матрицы
    a = [[0 for x in range(m)] for y in range(n)]
    F = np.array(a)
    for i in reversed(range(n)):
        for j in reversed(range(m)):
            if s1[i] == s2[j] or s1[i].isupper() or (s1.isupper() and s2.isupper()):
                if i < n - 1 and j < m - 1:
                    if i == n-2 or j == m-2:
                        F[i][j] = F[i + 1][j + 1] + 1
                    else:
                        F[i][j] = max(max(map(max, F[i + 2:, j + 2:])), F[i + 1][j + 1]) + 1
                else:
                    F[i][j] = 1
    for line in F:
        print(line)

    rules = bs.build_rules(s1, s2, F, False)
    print(rules)
    return rules

# Построение правил для образца и строки
def calc_lev_with_blanks_for_sample(s1, s2):
    n = len(s1)
    m = len(s2)
    # Инициализация матрицы
    a = [[0 for x in range(m)] for y in range(n)]
    F = np.array(a)
    for i in reversed(range(n)):
        for j in reversed(range(m)):
            if s1[i] == s2[j] or s1[i].isupper() or (s1.isupper() and s2.isupper()):
                if i < n-1 and j < m-1:
                    F[i][j] = max(map(max, F[i+1:, j+1:])) + 1
                else:
                    F[i][j] = 1
    for line in F:
        print(line)

    rules = bs.build_rules_for_sample(s1, s2, F, True)
    print(rules)
    return rules

# Основной метод, в нём работает почти всё
def calc_lev_with_steps(s1, s2):
    n = len(s1)
    m = len(s2)
    # Инициализация матрицы
    a = [[0 for x in range(m)] for y in range(n)]
    F = np.array(a)
    for i in reversed(range(n)):
        for j in reversed(range(m)):
            if s1[i] == s2[j] or s1[i].isupper() or (s1.isupper() and s2.isupper()):
                if i < n - 1 and j < m - 1:
                    F[i][j] = max(map(max, F[i + 1:, j + 1:])) + 1
                else:
                    F[i][j] = 1
    for line in F:
        print(line)

    rules = brs.build_iterations(s1, s2, F)
    #print(rules)
    return rules



print(calc_lev_with_steps("XеYZрA", "геометрия"))
#print(calc_lev_with_steps("", "гXмеYий"))