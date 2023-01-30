import numpy as np
from numpy import unravel_index
import BuildRuleService as bs

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


#calc_lev_with_blanks("гомеопатия", "геометрия")
calc_lev_without_blanks("гомеопатия", "геометрия")
calc_lev_without_blanks("баран", "баклан")
calc_lev_with_blanks_for_sample("баXан", "баран")
