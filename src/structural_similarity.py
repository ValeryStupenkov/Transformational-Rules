import modified_structural_similarity as mss

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
                vars = {}
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
            if prev_i == 0 and prev_j == 0:
                if i != 0 or j != 0:
                    # добавление переменной в случае если начало не совпадает
                    key = mss.new_variable(vars)
                    vars[key] = ("", "")
                    if i != 0:
                        vars[key] = (s1[0:i], "")
                    if j != 0:
                        vars[key] = (vars[key][0], s2[0:j])
                    res += key
                res += s2[j]
                i, j = find_max_pos(F[i+1:, j+1:], n, m, blanks)
            # проверка чтобы не выходить за границы
            elif (i == n-2 or j == m-2) or (i == n-1 or j == m-1):
                # случай для заполнения переменных
                if i != prev_i+1 or j != prev_j+1:
                    # добавление переменной
                    key = mss.new_variable(vars)
                    vars[key] = ("", "")
                    if i != prev_i + 1:
                        vars[key] = (s1[prev_i + 1:i], "")
                    if j != prev_j + 1:
                        vars[key] = (vars[key][0], s2[prev_j + 1:j])
                    res += key
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
                # добавление переменной
                key = mss.new_variable(vars)
                vars[key] = ("", "")
                if i != prev_i + 1:
                    vars[key] = (s1[prev_i + 1:i], "")
                if j != prev_j + 1:
                    vars[key] = (vars[key][0], s2[prev_j + 1:j])
                res += key
                res += s2[j]
                prev_i, prev_j = i, j
                i, j = find_max_pos(F[i + 1:, j + 1:], n, m, blanks)

            # Доп часть для проверки конца
            if i != n and j != m and F[i][j] == 0:
                # добавление переменной
                key = mss.new_variable(vars)
                vars[key] = (s1[i:], s2[j:])
                res += key
                break
            elif i != n and j == m:
                # добавление переменной
                key = mss.new_variable(vars)
                vars[key] = (s1[i:], "")
                res += key
            elif i == n and j != m:
                # добавление переменной
                key = mss.new_variable(vars)
                vars[key] = ("", s2[j:])
                res += key
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
    return max_i, max_j

# Проход по реверснутой строке и склеивание соседних переменных
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