import json
import math

with open('Y:\Student Handout\Input data\level0.json', 'r') as f1:
    data = json.load(f1)
#print(data)

matrix = []
for node, info in data["neighbourhoods"].items():
    matrix.append(info["distances"] + [data["restaurants"]["r0"]["neighbourhood_distance"][int(node[1:])]])
 
def algo(matrix, s):
    n = len(matrix)
    inf = 99999999999999
    weight = 0
    path = [0] * n
    visited_path = {}

    start = s
    visited_path[start] = 1

    for i in range(n-1):
        next = -1
        minw = inf

        for j in range(n):
            if start!=j and j not in visited_path:
                if matrix[start][j] < minw:
                    minw = matrix[start][j]
                    next = j
        path[i] = next
        weight += minw
        visited_path[next] = 1
        start = next
    
    stop = path[-1]
    lastw = matrix[stop][0]
    weight += lastw
    visited_path[s] = 1
    
    return path, weight


p,q = algo(matrix, 0)
print(p)
print(q)
ans = {"v0": {"path": ["r0"] + [f"n{i}" for i in p] + ["r0"]}}
print(ans)

with open("level0_output.json", "w+") as f2:
        json.dump(ans, f2)

