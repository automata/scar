# coding: utf-8
# plota gráfico com dados (tss) obtidos em ana5.py

import music21 as m, numpy as n
from itertools import groupby, chain
import matplotlib.pyplot as plt

compositores = ['beethoven', 'mozart']
tss = [{'10/4': 1,
        '7/4': 3,
        '9/16': 191,
        '5/4': 2,
        '2/4': 5109,
        '12/16': 209,
        '4/4': 2849,
        '6/4': 3,
        '3/4': 4189,
        '9/8': 255,
        '12/8': 264,
        '3/8': 880,
        '2/2': 1976,
        '17/16': 1,
        '6/8': 1907},

       {'2/4': 1696,
        '4/4': 1683,
        '16/4': 1,
        '3/4': 1872,
        '3/8': 575,
        '2/2': 353,
        '6/8': 848}]

# plotamos o gráfico

fig = plt.figure(num=None, figsize=(15, 10))
plot = fig.add_subplot(111)

keys = set(list(chain(*tss))) # todas time signatures sem repeteco
ind = n.arange(len(keys)) # x das barras
width = 0.35 # tamanho das barras
colors = 'bg' # cores usadas (apenas duas, para beethoven e mozart)

# beethoven
ts = tss[0]
vals0 = []
for k in keys:
    if k not in ts.keys(): # nao tem essa chave
        vals0.append(0)
    else: # tem chave
        vals0.append(ts[k])

# mozart
ts = tss[1]
vals1 = []
for k in keys:
    if k not in ts.keys(): # nao tem essa chave
        vals1.append(0)
    else: # tem chave
        vals1.append(ts[k])

r = sum(vals0) / sum(vals1)

# proporcao
vals0p = [x/r for x in vals0]
vals1p = [x/r for x in vals1]

rect0 = plot.bar(ind, vals0p, width, color=colors[0])
rect1 = plot.bar(ind+width, vals1p, width, color=colors[1])

plot.set_ylabel('Number of measures')
plot.set_xlabel('Time signatures')
plot.set_xticks(ind+width)
plot.set_xticklabels(tuple(keys))
plot.legend((rect0[0], rect1[0]),
            tuple([x.capitalize() for x in compositores]))

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plot.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

autolabel(rect0)
autolabel(rect1)

fig.savefig('timesignatures_ambos.png')
