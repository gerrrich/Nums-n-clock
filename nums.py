import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter


def p(a, b, c, d, t):
    x = a[0] * (1 - t) ** 3 + 3 * b[0] * (1 - t) ** 2 * t + 3 * c[0] * (1 - t) * t ** 2 + d[0] * t ** 3
    y = a[1] * (1 - t) ** 3 + 3 * b[1] * (1 - t) ** 2 * t + 3 * c[1] * (1 - t) * t ** 2 + d[1] * t ** 3
    return [x, y]


def s(dig, seg):
    return digits['digit_' + str(dig)]['segment_' + str(seg)]


def c(a, b, t):
    return [a[0] * (1 - t) + b[0] * t, a[1] * (1 - t) + b[1] * t]


def coord(num, n):
    return p(c(s(num, j)[0], s((num + 1) % n, j)[0], u / fr),
             c(s(num, j)[1], s((num + 1) % n, j)[1], u / fr),
             c(s(num, j)[2], s((num + 1) % n, j)[2], u / fr),
             c(s(num, j)[3], s((num + 1) % n, j)[3], u / fr), i / k)


with open('digits.json', 'r') as f:
    digits = json.load(f)

back_color = np.array([0, 0, 0], dtype=np.uint8)
color = np.array([255, 0, 0], dtype=np.uint8)

height = 500
width = 500

image = np.zeros((height, width, 3), dtype=np.uint8)
image[:, :] = back_color
fig = plt.figure(figsize=(15, 15))
k = 300
fr = 50
frames = []

for num in range(10):
    for u in range(fr + 1):
        for j in range(4):
            for i in range(k + 1):
                xy = coord(num, 10)
                x = round(xy[1])
                y = round(xy[0])
                image[x, y] = color
                image[x + 1, y] = color  # повысил жирность цифр
                image[x, y + 1] = color
                image[x - 1, y] = color
                image[x, y - 1] = color
        im = plt.imshow(image)
        frames.append([im])
        image[:, :] = back_color

ani = animation.ArtistAnimation(fig, frames, interval=1, blit=True, repeat_delay=0)
writer = PillowWriter(fps=24)
ani.save("nums.gif", writer=writer)

plt.show()
