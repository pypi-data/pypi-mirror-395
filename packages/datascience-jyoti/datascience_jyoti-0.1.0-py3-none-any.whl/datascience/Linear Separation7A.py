# PRACTICAL 7A
# Aim: Linear Separation Program

import numpy as np
import matplotlib.pyplot as plt

def create_distance_function(a, b, c):
    def distance(x, y):
        nom = a * x + b * y + c
        if nom == 0:
            pos = 0
        elif (nom < 0 and b < 0) or (nom > 0 and b > 0):
            pos = -1
        else:
            pos = 1
        return abs(nom) / np.sqrt(a**2 + b**2), pos
    return distance

points = [(3.5, 1.8), (1.1, 3.9)]

fig, ax = plt.subplots()
ax.set_xlabel("sweetness")
ax.set_ylabel("sourness")
ax.set_xlim([-1, 6])
ax.set_ylim([-1, 8])

X = np.arange(-0.5, 5, 0.1)

# Plot points
ax.plot(3.5, 1.8, "o", color="darkorange", markersize=10)
ax.plot(1.1, 3.9, "oy", markersize=10)

# Trying multiple slopes
step = 0.05
for x in np.arange(0, 1 + step, step):
    slope = np.tan(np.arccos(x))
    dist_fun = create_distance_function(slope, -1, 0)
    Y = slope * X

    results = [dist_fun(px, py)[1] for px, py in points]

    if results[0] != results[1]:
        ax.plot(X, Y, 'g-')
    else:
        ax.plot(X, Y, 'r-')

plt.show()
