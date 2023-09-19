import math
import random
from itertools import permutations
import matplotlib.pyplot as plt
from datetime import datetime

file_num = "3"
cities_cord = [tuple(list(map(float, line.split()))[1:]) for line in open(file_num + ".tsp", "r").readlines()]
#random.shuffle(cities_cord)

def caldis(x, y):
    return math.sqrt((cities_cord[x][0] - cities_cord[y][0]) ** 2 + (cities_cord[x][1] - cities_cord[y][1]) ** 2)

dis = [[caldis(i, j) for j in range(len(cities_cord))] for i in range(len(cities_cord))]

n_layers = [2, len(cities_cord)]
alpha = 1

w = [[cities_cord[random.randint(0, len(cities_cord) - 1)][i] for j in range(n_layers[1])] for i in range(n_layers[0])]
alpha = 1
R = 5


def calfit(per):
    ret = 0
    for i in range(len(per) - 1):
        ret += dis[per[i]][per[i + 1]]
    return ret

def bt_solve(cities):
    ret = cities
    val = calfit(cities)
    for per in permutations(cities):
        temp = calfit(per)
        if temp < val:
            val = temp
            ret = per
    return ret

def D_min(c):
    min_arg = 0
    min_val = sum([(w[i][0] - cities_cord[c][i]) ** 2 for i in range(n_layers[0])])
    for j in range(1, n_layers[1]):
        temp = sum([(w[i][j] - cities_cord[c][i]) ** 2 for i in range(n_layers[0])])
        if temp < min_val:
            min_arg = j
            min_val = temp
    return min_arg

t_gen = 239
while t_gen > 0:
    for c in range(len(cities_cord)):
        min_arg = D_min(c)
        for k in range(min_arg - R, min_arg + R + 1):
            j = k % n_layers[1]
            for t in range(0, n_layers[0]):
                w[t][j] = w[t][j] + alpha * (cities_cord[c][t] - w[t][j])
    alpha *= 0.9
    #if random.random() <= (R / t_gen):
    #    R = max(0, R - 1)
    if t_gen % 30 == 0:
        R = max(0, R - 1)
    t_gen -= 1

classes = []
for i in range(len(cities_cord)):
    classes.append([])
for c in range(len(cities_cord)):
    classes[D_min(c)].append(c)
solution = []
for i in range(len(classes)):
    if len(classes[i]) > 0:
        solution += bt_solve(classes[i])
print(solution)
print(calfit(solution) + dis[solution[0]][solution[-1]])
x = [cities_cord[solution[i]][0] for i in range(len(cities_cord))] + [cities_cord[solution[0]][0]]
y = [cities_cord[solution[i]][1] for i in range(len(cities_cord))] + [cities_cord[solution[0]][1]]
color = [D_min(solution[i]) for i in range(len(cities_cord))] + [D_min(solution[i])]
figure, axis = plt.subplots(1, 2)
axis[0].plot(x, y, color='black', linewidth = 3, marker='o', markerfacecolor='blue', markersize=12)

axis[1].scatter(x, y, c = color)

#plt.plot(x, y, color='black', linewidth = 3, marker='o', markerfacecolor='blue', markersize=12)
#plt.scatter(x, y, c = color)
#plt.show()

plt.savefig("vis" + file_num +".jpg")