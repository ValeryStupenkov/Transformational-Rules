variables = ["X", "Y", "Z", "A", "B", "C", "D", "E", "F",
             "G", "H", "I", "J", "K", "L", "M", "N", "O",
             "P", "Q", "R", "S", "T", "U", "V", "W"]

def build_iterations(s1, s2, F):
    n = len(s1)
    m = len(s2)
    results = {}
    begins = find_max_poses(F, n, m)
    samples = {}
    for begin in begins:
        # Первый шаг алгоритма
        prev_i = -1
        prev_j = -1
        max_i = 0
        max_j = 0
        tmp_vars = {}
        first_step_res = build_rule_step("", s1, s2, tmp_vars, prev_i, prev_j, begin)
        results[first_step_res] = [begin, tmp_vars]

        while max_i < n and max_j < m:
            tmp_dict = {}
            for key in results:
                prev_i = results[key][0][0]
                prev_j = results[key][0][1]
                # Дошли до края матрицы
                if prev_i == n-1 or prev_j == m-1:
                    # Добавить переменную в конец в случае необходимости
                    if prev_i < n-1 or prev_j < m-1:
                        k = new_variable(results[key][1])
                        new_key = key + k
                        if prev_i == n - 1:
                            results[key][1][k] = ("", s2[prev_j + 1:])
                        elif prev_j == m - 1:
                            results[key][1][k] = (s1[prev_i + 1:], "")
                        tmp_dict[new_key] = [[results[key][0][0]+1, results[key][0][1]+1], results[key][1]]
                    else:
                        tmp_dict[key] = [[results[key][0][0] + 1, results[key][0][1] + 1], results[key][1]]
                    continue
                elif prev_i == n or prev_j == m:
                    tmp_dict[key] = results[key]
                    continue
                else:
                    maxes = find_max_poses(F[results[key][0][0]+1:, results[key][0][1]+1:], n, m)

                for max in maxes:
                    tmp_vars = results[key][1].copy()

                    # условия для остановки вычислений
                    if max[0] != n and max[1] != m and F[max[0]][max[1]] == 0:
                        k = new_variable(tmp_vars)
                        tmp_vars[k] = (s1[prev_i + 1:], s2[prev_j + 1:])
                        tmp_dict[key + k] = [[n, m], tmp_vars]
                        continue
                    elif max[0] != n and max[1] == m:
                        k = new_variable(tmp_vars)
                        tmp_vars[k] = (s1[max[0]:], "")
                        tmp_dict[key + k] = [[n, m], tmp_vars]
                        continue
                    elif max[0] == n and max[1] != m:
                        k = new_variable(tmp_vars)
                        tmp_vars[k] = ("", s2[max[1]:])
                        tmp_dict[key + k] = [[n, m], tmp_vars]
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
        for key in results:
            samples[key] = results[key]

    # Перевод из внутреннего представления
    rules = {}
    for key in samples.keys():
        tmp_v = samples[key][1]
        rules[key] = tmp_v

    return rules




def find_max_poses(a, n, m):
    shape = a.shape
    max_elem = a.max()
    maxes = []
    for i in range(shape[0]):
        for j in range(shape[1]):
            if a[i][j] == max_elem:
               maxes.append([i, j])
    for max in maxes:
        max[0] += n-shape[0]
        max[1] += m-shape[1]
    # Отладочная печать
    #print(maxes)
    return maxes


def build_rule_step(res, s1, s2, vars, prev_i, prev_j, max):
    i = max[0]
    j = max[1]
    # максимальный элемент
    if prev_i == -1 and prev_j == -1:
        if i != 0 or j != 0:
            # добавление переменной в случае если начало не совпадает
            key = new_variable(vars)
            vars[key] = ("", "")
            if i != 0:
                vars[key] = (s1[0:i], "")
            if j != 0:
                vars[key] = (vars[key][0], s2[0:j])
            res += key
        if res != "":
            last_char = res[-1]
        else:
            last_char = " "
        if s1[i].isupper():
            if last_char.isupper():
                vars[last_char] = (vars[last_char][0] + s1[i], vars[last_char][1] + s2[j])
            else:
                key = new_variable(vars)
                vars[key] = (s1[i], s2[j])
                res += key
        else:
            res += s2[j]

    # Случай, при котором всё ок
    elif i == prev_i + 1 and j == prev_j + 1:
        if s1[i].isupper():
            key = new_variable(vars)
            vars[key] = (s1[i], s2[j])
            res += key
        else:
            res += s2[j]

    # случай для заполнения переменных (обычный)
    elif i != prev_i + 1 or j != prev_j + 1:
        # цикл добавления переменной
        if res != "":
            last_char = res[-1]
        else:
            last_char = " "
        if last_char.isupper():
            if i != prev_i + 1:
                vars[last_char] = (vars[last_char][0] + s1[prev_i + 1:i], vars[last_char][1])
            if j != prev_j + 1:
                vars[last_char] = (vars[last_char][0], vars[last_char][1] + s2[prev_j + 1:j])
        else:
            key = new_variable(vars)
            vars[key] = ("", "")
            if i != prev_i + 1:
                vars[key] = (s1[prev_i + 1:i], "")
            if j != prev_j + 1:
                vars[key] = (vars[key][0], s2[prev_j + 1:j])
            res += key
        # Здесь в конце res всегда переменная, так что просто дописываем в неё
        last_char = res[-1]
        if s1[i].isupper():
            vars[last_char] = (vars[last_char][0] + s1[i], vars[last_char][1] + s2[j])
        else:
            res += s2[j]
    return res


def new_variable(vars):
    for key in variables:
        if not key in vars:
            return key
        else:
            continue

