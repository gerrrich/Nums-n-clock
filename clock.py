import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime
import gc

with open('digits.json', 'r') as f:
    dig = json.load(f)

digits = []
for i in range(10):
    di = []
    for j in range(4):
        di.append(dig['digit_' + str(i)]['segment_' + str(j)])
    digits.append(di)


def C(a, b, t):
    return [a[0] * (1 - t) + b[0] * t, a[1] * (1 - t) + b[1] * t]


def P(a, b, c, d, t):
    t11 = (1 - t) ** 2
    t1 = t11 * (1 - t)
    t2 = t11 * t
    t22 = t ** 2
    t3 = (1 - t) * t22
    t4 = t22 * t

    x = a[0] * t1 + 3 * b[0] * t2 + 3 * c[0] * t3 + d[0] * t4
    y = a[1] * t1 + 3 * b[1] * t2 + 3 * c[1] * t3 + d[1] * t4
    return [x, y]


frames = 20


def change(num1, num2, offset):
    k = 15

    changed = []
    for l in range(frames):
        x = []
        y = []
        for j in range(4):
            for i in range(k + 1):
                xy = P(C(digits[num1][j][0], digits[num2][j][0], l / frames),
                       C(digits[num1][j][1], digits[num2][j][1], l / frames),
                       C(digits[num1][j][2], digits[num2][j][2], l / frames),
                       C(digits[num1][j][3], digits[num2][j][3], l / frames), i / k)
                x.append(1 - xy[1] / 500)
                y.append(xy[0] / 500 + offset)

        changed.append([x, y])
    return changed


result_sec1 = []
for i in range(10):
    result_sec1.append(change(i, (i + 1) % 10, 5))

result_sec2 = []
for i in range(6):
    result_sec2.append(change(i, (i + 1) % 6, 4))

result_min1 = []
for i in range(10):
    result_min1.append(change(i, (i + 1) % 10, 3))

result_min2 = []
for i in range(6):
    result_min2.append(change(i, (i + 1) % 6, 2))

result_hour1 = []
for i in range(10):
    result_hour1.append(change(i, (i + 1) % 10, 1))
result_hour1.append(change(3, 0, 1))

result_hour2 = []
for i in range(3):
    result_hour2.append(change(i, (i + 1) % 3, 0))

gc.collect()

fig = plt.figure(figsize=(16, 4))
ax = plt.axes(xlim=(0, 6), ylim=(0, 1))

separator1, = ax.plot([], [], lw=2, color='b')
separator2, = ax.plot([], [], lw=2, color='b')
separator3, = ax.plot([], [], lw=2, color='b')
separator4, = ax.plot([], [], lw=2, color='b')

line, = ax.plot([], [], lw=2, color='r')
line2, = ax.plot([], [], lw=2, color='r')
line3, = ax.plot([], [], lw=2, color='m')
line4, = ax.plot([], [], lw=2, color='m')
line5, = ax.plot([], [], lw=2, color='g')
line6, = ax.plot([], [], lw=2, color='g')


def init():
    now = datetime.datetime.now()
    sec2 = now.second // 10
    min1 = now.minute % 10
    min2 = now.minute // 10
    hour1 = now.hour % 10
    hour2 = now.hour // 10

    separator1.set_data([4, 4], [0.1, 0.4])
    separator2.set_data([4, 4], [0.6, 0.9])
    separator3.set_data([2, 2], [0.1, 0.4])
    separator4.set_data([2, 2], [0.6, 0.9])

    line.set_data([], [])

    x2 = result_sec2[sec2][0][1]
    y2 = result_sec2[sec2][0][0]
    line2.set_data(x2, y2)

    x3 = result_min1[min1][0][1]
    y3 = result_min1[min1][0][0]
    line3.set_data(x3, y3)

    x4 = result_min2[min2][0][1]
    y4 = result_min2[min2][0][0]
    line4.set_data(x4, y4)

    x5 = result_hour1[hour1][0][1]
    y5 = result_hour1[hour1][0][0]
    line5.set_data(x5, y5)

    x6 = result_hour2[hour2][0][1]
    y6 = result_hour2[hour2][0][0]
    line6.set_data(x6, y6)

    return line, line2, line3, line4, line5, line6,


ch = 1000000 / frames


def animate(i):
    now = datetime.datetime.now()
    mic = int(int(now.microsecond) // ch)
    sec1 = now.second % 10
    sec2 = now.second // 10
    min1 = now.minute % 10
    min2 = now.minute // 10
    hour1 = now.hour % 10
    hour2 = now.hour // 10

    x1 = result_sec1[sec1][mic][1]
    y1 = result_sec1[sec1][mic][0]
    line.set_data(x1, y1)

    if sec1 == 9:
        x2 = result_sec2[sec2][mic][1]
        y2 = result_sec2[sec2][mic][0]
        line2.set_data(x2, y2)

    if sec2 == 5 and sec1 == 9:
        x3 = result_min1[min1][mic][1]
        y3 = result_min1[min1][mic][0]
        line3.set_data(x3, y3)

    if min1 == 9 and sec2 == 5 and sec1 == 9:
        x4 = result_min2[min2][mic][1]
        y4 = result_min2[min2][mic][0]
        line4.set_data(x4, y4)

    if (not (hour2 == 2 and hour1 == 3)) and min2 == 5 and min1 == 9 and sec2 == 5 and sec1 == 9:
        x5 = result_hour1[hour1][mic][1]
        y5 = result_hour1[hour1][mic][0]
        line5.set_data(x5, y5)

    if hour1 == 9 and min2 == 5 and min1 == 9 and sec2 == 5 and sec1 == 9:
        x6 = result_hour2[hour2][mic][1]
        y6 = result_hour2[hour2][mic][0]
        line6.set_data(x6, y6)

    if hour2 == 2 and hour1 == 3 and min2 == 5 and min1 == 9 and sec2 == 5 and sec1 == 9:
        x5 = result_hour1[10][mic][1]
        y5 = result_hour1[10][mic][0]
        line5.set_data(x5, y5)

        x6 = result_hour2[2][mic][1]
        y6 = result_hour2[2][mic][0]
        line6.set_data(x6, y6)

    return line, line2, line3, line4, line5, line6,


anim = animation.FuncAnimation(fig, animate, init_func=init, interval=1, blit=True)
plt.show()
print('ok')
