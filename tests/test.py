
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()

x = [i for i in range(1, 8)]

y_1 = [33.0, 34.75, 39.8, 40.775, 42.4, 43.349999999999994, 44.385714285714286]
y_2 = [37.2, 39.55, 43.6, 46.025, 49.46, 2459.1666666666665, 2577.1428571428573]
y_5 = [45.8, 48.25, 5821, 5821, 5821, 5821, 5821]
y_3 = [65.0 for i in range(0, 7)] 


ax1.plot(x, y_2, '-o', label='host_4 avec 3.6 Mbit/s', color='green')
ax1.plot(x, y_5, '-o', label='host_4 avec 1.6 Mbit/s', color='red')
ax1.plot(x, y_1, '-o', label='host_4 avec 8 Mbit/s', color='orange')
ax1.plot(x, y_3, label='Temps de réponse exigé', color='blue')

ax1.set_xlabel("Nombre d'utilisateurs simultanés")

new_tick_locations = np.array([.045, .19, .345, .5, .645, .8, 0.955])

#ax2.set_xlim(ax1.get_xlim())
ax2.set_xticks(new_tick_locations)
ax2.set_xticklabels([30, 60, 90, 120, 150, 180, 210])
ax2.set_xlabel(r"Nombre de requêtes par seconde")

fig.text(0.04, 0.5, 'Temps de réponse (ms)', va='center', rotation='vertical')

ax1.legend(loc='lower right')

plt.ylim(-10, 110)

plt.show()

"""
with open('test2_host3_8Mbit.txt') as f:
    lines = f.readlines()

sum = 0
cnt = 0
y = []
for i in range(0, len(lines)) :
    if lines[i] != '\n' :
        lines[i] = float(lines[i][0:4])
        sum += lines[i]
        cnt += 1
    else : 
        if i != 0 : 
            y.append(sum / cnt)
        sum = 0
        cnt = 0
y.append(sum / cnt)

print(y)

with open('test2_host3_7Mbit.txt') as f:
    lines = f.readlines()

sum = 0
cnt = 0
y = []
for i in range(0, len(lines)) :
    if lines[i] != '\n' :
        lines[i] = float(lines[i][0:4])
        sum += lines[i]
        cnt += 1
    else : 
        if i != 0 : 
            y.append(sum / cnt)
        sum = 0
        cnt = 0
y.append(sum / cnt)

print(y)

with open('test2_host3_3Mbit.txt') as f:
    lines = f.readlines()

sum = 0
cnt = 0
y = []
for i in range(0, len(lines)) :
    if lines[i] != '\n' :
        lines[i] = float(lines[i][0:4])
        sum += lines[i]
        cnt += 1
    else : 
        if i != 0 : 
            y.append(sum / cnt)
        sum = 0
        cnt = 0
y.append(sum / cnt)

print(y)

with open('test2_host3_1Mbit.txt') as f:
    lines = f.readlines()

sum = 0
cnt = 0
y = []
for i in range(0, len(lines)) :
    if lines[i] != '\n' :
        lines[i] = float(lines[i][0:4])
        sum += lines[i]
        cnt += 1
    else : 
        if i != 0 : 
            y.append(sum / cnt)
        sum = 0
        cnt = 0
y.append(sum / cnt)

print(y)

"""
