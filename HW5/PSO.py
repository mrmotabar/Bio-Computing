#from math import sin, cos, tan
from mpmath import mp
precision = 100
mp.dps = precision
from random import random
import copy


def f(l):
    x = l[0]
    y = l[1]
    #return abs(mp.sin(x) * mp.cos(y) * mp.exp(abs(1 - (mp.sqrt(x * x + y * y) / mp.pi))))
    return x * mp.sin(mp.pi * mp.cos(x) * mp.tan(y)) * (mp.sin(x / y) / (1 + mp.cos(y / x)))


def normalize(x):
    global f_range
    while x > f_range:
        x -= 2 * f_range
    while x < -f_range:
        x += 2 * f_range
    return x


#start
f_range = 100
number_of_particles = 100
number_of_generations = 100
w = 0.8
c1 = 0.7
c2 = 0.9
x = [[(random() * 2 - 1) * f_range, (random() * 2 - 1) * f_range] for _ in range(number_of_particles)]
v = [[random() * 2 - 1, random() * 2 - 1] for _ in range(number_of_particles)]
p_best = [[f(x[i]), x[i][:]] for i in range(number_of_particles)]
g_best = copy.deepcopy(p_best[0])
for i in range(1, number_of_particles):
    if p_best[i][0] > g_best[0]:
        g_best = copy.deepcopy(p_best[i])

while number_of_generations:
    #print(number_of_generations)
    print(g_best)
    for i in range(number_of_particles):
        r1 = random()
        r2 = random()
        v[i][0] = w * v[i][0] + c1 * r1 * (p_best[i][1][0] - x[i][0]) + c2 * r2 * (g_best[1][0] - x[i][0])
        v[i][1] = w * v[i][1] + c1 * r1 * (p_best[i][1][1] - x[i][1]) + c2 * r2 * (g_best[1][1] - x[i][1])
        x[i][0] = x[i][0] + v[i][0]
        x[i][1] = x[i][1] + v[i][1]
        x[i] = [normalize(x[i][0]), normalize(x[i][1])]
        if f(x[i]) > p_best[i][0]:
            p_best[i] = [f(x[i]), x[i]]
        if p_best[i][0] > g_best[0]:
            g_best = copy.deepcopy(p_best[i])
    number_of_generations -= 1

print(g_best)