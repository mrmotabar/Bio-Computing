import math
import random

n_layers = [2, 10, 10, 10, 1]
alpha = 1

x = []
x_in = []
delta_x = []
for i in range(len(n_layers)):
    x_in.append([0] * (n_layers[i] + 1))
    delta_x.append([0] * (n_layers[i] + 1))
    x.append([1])
    for j in range(n_layers[i]):
        x[-1].append(0)

w = []
for i in range(len(n_layers) - 1):
    w.append([])
    for j in range(n_layers[i] + 1):
        w[-1].append([0])
        for k in range(n_layers[i + 1]):
            w[-1][-1].append(random.random() - 0.5)

train_data = []
with open("train.txt", "r") as data_file:
    for line in data_file:
        train_data.append(list(map(float, line.split("\t"))))
        if train_data[-1][2] == 0:
            train_data[-1][2] = -1

test_data = []
with open("test.txt", "r") as data_file:
    for line in data_file:
        test_data.append(list(map(float, line.split("\t"))))
        if test_data[-1][2] == 0:
            test_data[-1][2] = -1

def f(x):
    return (2 / (1 + math.exp(-x))) - 1

def d_f(x):
    return (1 + f(x)) * (1 - f(x)) / 2

def cal_x():
    for i in range(1, len(n_layers)):
        for j in range(1, n_layers[i] + 1):
            x_in[i][j] = 0
            for k in range(n_layers[i - 1] + 1):
                x_in[i][j] += x[i - 1][k] * w[i - 1][k][j]
            x[i][j] = f(x_in[i][j])

def upd_weights():
    mx = 0
    for i in range(len(n_layers) - 1):
        for j in range(n_layers[i] + 1):
            for k in range(n_layers[i + 1] + 1):
                mx = max(mx, abs(alpha * delta_x[i + 1][k] * x[i][j]))
                w[i][j][k] += alpha * delta_x[i + 1][k] * x[i][j]
    return mx

def train():
    mx = 0
    for data in train_data:
        x[0][1] = data[0]
        x[0][2] = data[1]
        cal_x()
        for i in range(1, n_layers[-1] + 1):
            delta_x[-1][i] = (data[2] - x[-1][i]) * d_f(x_in[-1][i])
        for i in range(1, len(n_layers) - 1):
            for j in range(1, n_layers[i] + 1):
                for k in range(1, n_layers[i + 1] + 1):
                    delta_x[i][j] += delta_x[i + 1][k] * w[i][j][k]
                delta_x[i][j] *= d_f(x_in[i][j])
        mx = max(mx, upd_weights())
    return mx

ch = 1
while ch > 0.000000000000001:
    ch = train()
    alpha *= 0.9

""" 
t = 0
while t < 400:
    train()
    alpha *= 0.9
    t += 1
"""
out_file = open("weights.txt", "w")
out_file.write("layers:")
out_file.write(str(n_layers) + "\n")
out_file.write("w:")
out_file.write(str(w))
out_file.close()

out_file = open("wc-test.txt", "w")
correct_cnt = 0
for data in test_data:
    x[0][1] = data[0]
    x[0][2] = data[1]
    cal_x()
    if x[-1][1] > 0:
        x[-1][1] = 1
    else:
        x[-1][1] = -1
    if x[-1][1] != data[2]:
        out_file.write("Wrong\n")
    else:
        correct_cnt += 1
        out_file.write("Correct\n")
out_file.write(str((correct_cnt / len(test_data)) * 100))
out_file.close()
if (correct_cnt / len(test_data)) * 100 > 94:
    print("found1")

out_file = open("wc-train.txt", "w")
correct_cnt = 0
for data in train_data:
    x[0][1] = data[0]
    x[0][2] = data[1]
    cal_x()
    if x[-1][1] > 0:
        x[-1][1] = 1
    else:
        x[-1][1] = -1
    if x[-1][1] != data[2]:
        out_file.write("Wrong\n")
    else:
        correct_cnt += 1
        out_file.write("Correct\n")
out_file.write(str((correct_cnt / len(train_data)) * 100))
out_file.close()
if (correct_cnt / len(train_data)) * 100 > 94:
    print("found2")