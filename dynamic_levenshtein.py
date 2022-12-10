import numpy as np

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

    vars = {"X": "", "Y":"", "Z":""}

    for i in range(n):
        for j in range(m):
            if F[i][j] != 0:
                break


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



#calc_lev_with_blanks("гомеопатия", "геометрия")
#calc_lev_without_blanks("гомеопатия", "геометрия")
calc_lev_without_blanks("баXан", "баклан")