
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax1 = fig.add_subplot(111)
#ax2 = ax1.twiny()

x = [i for i in range(1, 31)]

y_1 = [48.3, 47.1, 46.8, 47.0, 46.6, 46.7, 47.3, 47.9, 46.6, 47.1, 47.4, 46.7, 47.0, 46.5, 46.6, 47.0, 53.2, 46.6, 46.2, 47.3, 46.4, 46.5, 46.5, 46.7, 47.0, 46.7, 46.4, 46.5, 47.7, 47.6]
y_2 = [79.2, 75.2, 75.2, 75.0, 75.1, 75.4, 75.1, 74.8, 74.8, 74.9, 74.6, 74.7, 75.6, 75.1, 75.0, 75.1, 74.7, 74.9, 74.8, 74.8, 75.2, 74.5, 75.4, 74.7, 75.0, 74.7, 74.9, 75.2, 74.9, 75.3]
y_3 = [48.3, 47.1, 46.8, 47.0, 46.6, 46.7, 47.3, 47.9, 46.6, 47.1, 47.4, 46.7, 47.0, 46.5, 46.6, 47.0, 53.2, 46.6, 46.2, 47.3, 46.4, 46.5, 46.5, 46.7, 47.0, 46.7, 46.4, 46.5, 47.7, 47.6]
#for i in range(len(y_2)): y_2[i] += 15
for i in range(len(y_3)): y_3[i] = 45 + y_3[i] % 1
y_4 = [65.0 for i in range(0, 30)] 


ax1.plot(x, y_1, '-o', label='host_4 ', color='green', zorder=10)
ax1.plot(x, y_2, '-o', label='host_3', color='red')
ax1.plot(x, y_3, '-o', label='host_2', color='orange')
ax1.plot(x, y_4, label='Temps de réponse exigé', color='blue')

ax1.set_xlabel("Exécutions")

#new_tick_locations = np.array([.045, .19, .345, .5, .645, .8, 0.955])

#ax2.set_xlim(ax1.get_xlim())
#ax2.set_xticks(new_tick_locations)
#ax2.set_xticklabels([30, 60, 90, 120, 150, 180, 210])
#ax2.set_xlabel(r"Nombre de requêtes par seconde")

fig.text(0.04, 0.5, 'Temps de réponse (ms)', va='center', rotation='vertical')

ax1.legend(loc='lower right')

plt.ylim(-10, 110)

plt.show()

"""
with open('test1_host3_ping.txt') as f:
    lines = f.readlines()

for i in range(0, len(lines)) :
    if lines[i] != '\n' :
        lines[i] = float(lines[i][0:4])

print(lines)

with open('test1_host4_ping.txt') as f:
    lines = f.readlines()

for i in range(0, len(lines)) :
    if lines[i] != '\n' :
        lines[i] = float(lines[i][0:4])

print(lines)

"""