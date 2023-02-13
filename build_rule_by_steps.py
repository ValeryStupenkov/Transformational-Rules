import numpy as np
import build_rule_service as bs

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

    rules = build_iterations(s1, s2, F)
    #print(rules)
    return rules


def build_iterations(s1, s2, F):
    n = len(s1)
    m = len(s2)
    vars = {"X": ("", ""), "Y": ("", ""), "Z": ("", ""),
            "A": ("", ""), "B": ("", ""), "C": ("", ""),
            "D": ("", ""), "E": ("", ""), "F": ("", ""), "G": ("", "")}
    results = {"": [[0, 0], vars]}
    begins = find_max_poses(F, n, m, True)
    for begin in begins:
        # first step
        prev_i = 0
        prev_j = 0
        max_i = prev_i
        max_j = prev_j
        tmp_dict = {}
        tmp_vars = vars
        first_step_res = build_rule_step("", s1, s2, tmp_vars, prev_i, prev_j, begin)
        tmp_dict[first_step_res] = [begin, tmp_vars]
        results = tmp_dict
        # Доработать условие цикла
        while max_i < n and max_j < m:
            tmp_dict = {}
            for key in results:
                prev_i = results[key][0][0]
                prev_j = results[key][0][1]
                # В этом if косяк !
                '''
                if prev_i == n-2 or prev_j == m-2:
                    maxes = [[prev_i+1, prev_j+1]]
                '''
                if prev_i == n-1 or prev_j == m-1:
                    tmp_dict[key] = [[results[key][0][0]+1, results[key][0][1]+1], results[key][1]]
                    continue
                elif prev_i == n or prev_j == m:
                    tmp_dict[key] = results[key]
                    continue
                else:
                    maxes = find_max_poses(F[results[key][0][0]+1:, results[key][0][1]+1:], n, m, True)

                for max in maxes:
                    tmp_vars = results[key][1].copy()

                    # условия для остановки вычислений
                    if max[0] != n and max[1] != m and F[max[0]][max[1]] == 0:
                        for k in tmp_vars.keys():
                            if tmp_vars[k] == ("", ""):
                                tmp_vars[k] = (s1[max[0]:], s2[max[1]:])
                                tmp_dict[key+k] = [[n, m], tmp_vars]
                                break
                        continue
                    elif max[0] != n and max[1] == m:
                        for k in tmp_vars.keys():
                            if tmp_vars[k] == ("", ""):
                                tmp_vars[k] = (s1[max[0]:], "")
                                tmp_dict[key+k] = [[n, m], tmp_vars]
                                break
                        continue
                    elif max[0] == n and max[1] != m:
                        for k in tmp_vars.keys():
                            if tmp_vars[k] == ("", ""):
                                tmp_vars[k] = ("", s2[max[1]:])
                                tmp_dict[key+k] = [[n, m], tmp_vars]
                                break
                        continue

                    step_res = build_rule_step(key, s1, s2, tmp_vars, prev_i, prev_j, max)
                    tmp_dict[step_res] = [[max[0], max[1]], tmp_vars]
            results = tmp_dict
            # Вычислить max_i и max_j
            max_i = n
            max_j = m
            for key in results:
                if results[key][0][0] < max_i:
                    max_i = results[key][0][0]
                if results[key][0][1] < max_j:
                    max_j = results[key][0][1]

    print(results)
    # Перевод из внутреннего представления и склеивание переменных
    rules = {}
    for key in results.keys():
        rule = bs.join_variables(key, results[key][1])
        rules[rule] = results[key][1]

    return rules




def find_max_poses(a, n, m, blanks):
    shape = a.shape
    max_elem = a.max()
    maxes = []
    if blanks:
        for i in range(shape[0]):
            for j in range(shape[1]):
                if a[i][j] == max_elem:
                    maxes.append([i, j])
    else:
        tmp = a[1:, 1:]
        if a[0][0] >= tmp.max():
            maxes.append([0, 0])
        else:
            max_elem = tmp.max()
            for i in range(shape[0]-1):
                for j in range(shape[1]-1):
                    if tmp[i][j] == max_elem:
                        maxes.append([i, j])
            shape = (shape[0]-1, shape[1]-1)
    for max in maxes:
        max[0] += n-shape[0]
        max[1] += m-shape[1]
    print(maxes)
    return maxes


def build_rule_step(res, s1, s2, vars, prev_i, prev_j, max):
    i = max[0]
    j = max[1]
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
    # Случай, при котором всё ок
    elif i == prev_i + 1 and j == prev_j + 1:
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

    # случай для заполнения переменных (обычный)
    elif i != prev_i + 1 or j != prev_j + 1:
        # цикл добавления переменной
        for key in vars.keys():
            if vars[key] == ("", ""):
                if i != prev_i + 1:
                    vars[key] = (s1[prev_i + 1:i], "")
                if j != prev_j + 1:
                    vars[key] = (vars[key][0], s2[prev_j + 1:j])
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

    return res



print(calc_lev_with_steps("гомXпатия", "геометXия"))