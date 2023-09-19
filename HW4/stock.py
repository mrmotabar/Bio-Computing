import math
import random


def gen_neighbor(l):
    ind1 = random.randint(0, len(l) - 1)
    ind2 = random.randint(0, len(l) - 1)
    l[ind1], l[ind2] = l[ind2], l[ind1]
    return l


def fitness(l, st_len):
    ret = 0
    s = 0
    for i in l:
        if s + i > st_len:
            ret += 1
            s = i
        else:
            s += i
    if s != 0:
        ret += 1
    return ret


#print(fitness([], ))
#exit()
st_len = 5600
req_order = [1520, 2150, 1880, 1520, 2150, 1820, 2150, 2050, 2140, 2140, 1710, 1820, 2150, 1380, 2140, 2150, 1820, 2050, 2100, 1380, 1880, 1880, 1520, 1930, 1710, 2140, 1880, 2050, 1710, 2150, 2000, 1710, 1820, 1560, 2150, 1930, 2000, 1880, 1380, 2050, 1930, 1710, 1820, 1710, 2200, 2050, 1560, 1930, 1930, 2050, 1560, 1380, 1520, 1520, 1520, 2100, 1560, 1520, 2150, 2000, 2000, 2140, 1560, 1880, 2200, 2140, 1930, 2000, 2050, 1520, 1880, 2200, 1520, 1930, 1520, 1710, 1710, 2150, 2100, 2200, 1820, 1820, 2200, 1380, 1880, 1880, 1710, 2140, 1820, 2100, 1380, 1880, 2140, 1820, 1930, 1880, 1880, 1520, 2000, 2050, 2140, 1380, 1380, 1380, 2150, 1380, 2150, 1820, 1820, 2140, 1560, 1710, 1520, 1560, 2140, 2200, 2200, 1880, 2200, 1710, 1930, 2100, 2200, 1820, 1520, 2140, 2100, 1380, 1520, 2140, 2050, 2100, 2200, 2140, 1820, 1820, 1380, 1880, 2140, 2150, 1930, 2100, 2150, 1380, 1710, 1380, 1380, 1520, 2200, 1380, 1560, 1930, 1820, 1930, 1380, 2140, 1520, 2050, 1710, 1880, 1560, 1520, 2150, 1880, 1520, 2100, 1560, 1710, 2150, 1930, 2000, 1930, 1520, 2200, 2200, 1560, 1820, 2100, 2150, 1880, 2000, 1820, 1380, 1930, 2100, 1880, 2200, 1560, 1380, 2100, 1520, 2000, 2200, 2000, 2100, 2050, 1930, 1520, 2200, 2200, 2050, 2100, 1380, 1930, 1820, 1520, 2150, 1520, 1520, 1380, 2200, 1380, 1930, 1930, 2150, 1930, 2200, 2200, 1520]
#print(len(req_order))
#random.shuffle(req_order)
#req_fit = fitness(req_order, st_len)
opt_order = []
opt_fit = 1e7 
#temp = 1000000
alpha = 0.7
k = 1
run = 1
while run > 0:
    temp = 1000000
    random.shuffle(req_order)
    req_fit = fitness(req_order, st_len)
    while temp > 10:
        if req_fit < opt_fit:
            opt_order = req_order
            opt_fit = req_fit
        neighbor = gen_neighbor(req_order[:])
        neighbor_fit = fitness(neighbor, st_len)
        if(neighbor_fit < req_fit):
            req_fit = neighbor_fit
            req_order = neighbor[:]
        else:
            if random.random() < math.e ** (-(neighbor_fit - req_fit) / (k * temp)):
                req_fit = neighbor_fit
                req_order = neighbor[:]
        temp *= alpha


    gen = 10000
    neighbor_t = 10
    while gen > 0:
        if req_fit < opt_fit:
            opt_order = req_order
            opt_fit = req_fit
        help_order = req_order[:]
        help_fit = req_fit
        for i in range(neighbor_t):
            neighbor = gen_neighbor(req_order[:])
            neighbor_fit = fitness(neighbor, st_len)
            if neighbor_fit < help_fit:
                help_fit = neighbor_fit
                help_order = neighbor[:]
        req_order = help_order[:]
        req_fit = help_fit
        gen -= 1
    run -= 1

print(opt_fit)
print(opt_order)
#print(len(opt_order))