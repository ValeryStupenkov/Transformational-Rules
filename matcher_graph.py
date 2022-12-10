import networkx as nx

def find_edges(matrix, i, j, n, m, G):
    for i_g in range(i + 1, n):
        for j_g in range(j + 1, m):
            if matrix[i_g][j_g] == 1:
                G.add_edge(str(i) + "," + str(j), str(i_g) + "," + str(j_g))

# Получает все максимальные пути из графа
def extractor(G, s1, s2):
    nodes = list(G.nodes)
    all_paths = []
    for src in nodes:
        for dst in nodes:
            for path in nx.all_simple_paths(G, src, dst):
                all_paths.append(path)
    #print(all_paths)
    max_len = max(len(path) for path in all_paths)
    #print(max_len)
    max_paths = []
    for path in all_paths:
        if len(path) == max_len:
            max_paths.append(path)
    #print(max_paths)
    result = []
    for path in max_paths:
        res, variables = path_to_string(path, s1, s2)
        result.append(tuple([res, variables]))
    return result

def path_to_string(path, s1, s2):
    cur_pos = 0
    res = ""
    variables = {"X": "", "Y": "", "Z": ""}
    for node in path:
        node_pos = int(node[2])
        if cur_pos == node_pos or cur_pos == node_pos-1:
            if (s1[int(node[0])].isupper()):
                for key in variables.keys():
                    if variables[key] == "":
                        res = res + key
                        variables[key] = s2[node_pos]
                        break
            else:
                res = res + s2[node_pos]
            cur_pos = node_pos
        else:
            if (res[-1].isupper()):
                variables[res[-1]] += s2[cur_pos+1:node_pos+1]
            else:
                for key in variables.keys():
                    if variables[key] == "":
                        res = res + key
                        if (s1[int(node[0])].isupper()):
                            variables[key] = s2[cur_pos+1:node_pos+1]
                        else:
                            variables[key] = s2[cur_pos + 1:node_pos]
                            res = res + s2[node_pos]
                        break

            cur_pos = node_pos
    #print(res)
    #print(variables)
    return res, variables

def match(s1, s2):
    n = len(s1)
    m = len(s2)
    # Инициализация матрицы
    matrix = [[0 for x in range(m)] for y in range(n)]
    #print(matrix)
    for i in range(n):
        for j in range(m):
            if s1[i] == s2[j]:
                matrix[i][j] = 1
            elif s1[i].isupper():
                matrix[i][j] = 1
            elif s2[j].isupper():
                matrix[i][j] = 1

    G = nx.DiGraph()
    for i in range(n-1):
        for j in range(m-1):
            if matrix[i][j] == 1:
                find_edges(matrix, i, j, n, m, G)
            j += 1
    #print(G.edges)
    paths = nx.all_simple_paths(G, '0,0', '5,6')
    #print(list(paths))
    return extractor(G, s1, s2)

def check_sample(sample, s):
    # check if there is sample in results from match
    results = match(sample, s)
    for r in results:
        if sample == r[0]:
            return r[0], r[1]
    return "", {}

def transform_rule(sample, variables):
    result = ""
    vars = {"X": "", "Y": "", "Z": ""}
    for i in range(len(sample)):
        if sample[i].isupper():
            result += variables[sample[i]]
        elif sample[i].islower():
            if i > 0 and result[-1].isupper():
                vars[result[-1]] += sample[i]
            else:
                for k in vars.keys():
                    if vars[k] == "":
                        vars[k] += sample[i]
                        result += k
                        break
    return result

def find_sample(s1, s2):
    # find common sample from two strings
    results = match(s1, s2)
    print(results)
    transform_rules = []
    for r in results:
        new_samp1 = transform_rule(r[0], r[1])
        tmp_r = check_sample(r[0], s1)
        new_samp2 = transform_rule(tmp_r[0], tmp_r[1])
        transform_rules.append(tuple([new_samp1, new_samp2]))
    return transform_rules

def find_common_sample(sample1, sample2):
    # find most common sample of two samples
    results = match(sample1, sample2)
    for r in results:
        if sample1 == r[0]:
            return sample1
        elif sample2 == r[0]:
            return sample2
    return ""

result = find_sample("баклан", "барабан")
m = match("баXаYн", "баклан")
print(result)
print(m)
