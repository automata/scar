# coding: utf-8
# plota gráfico com dados (tss) obtidos em ana5.py

import music21 as m, numpy as n
from itertools import groupby, chain
import matplotlib.pyplot as plt
import pickle as pk
from fractions import Fraction

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plot.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

compositores = ['beethoven', 'mozart', 'scarlatti']
f = open('d2.pkl', 'rb')
tss = pk.load(f)
f.close()

# plotamos o gráfico beethoven e mozart

fig = plt.figure(num=None, figsize=(15, 10))
plot = fig.add_subplot(111)

keys = set(list(chain(*tss))) # todas time signatures sem repeteco
keys = sorted([(k, float(Fraction(k))) for k in keys], key=lambda x: x[1])
ind = n.arange(len(keys)) # x das barras
width = 0.35 # tamanho das barras
colors = 'bg' # cores usadas (apenas duas, para beethoven e mozart)
print keys
# beethoven
ts = tss[0]
vals0 = []
for k in keys:
    if k[0] not in ts.keys(): # nao tem essa chave
        vals0.append(0)
    else: # tem chave
        vals0.append(ts[k[0]])

# mozart
ts = tss[1]
vals1 = []
for k in keys:
    if k[0] not in ts.keys(): # nao tem essa chave
        vals1.append(0)
    else: # tem chave
        vals1.append(ts[k[0]])

rect0 = plot.bar(ind, vals0, width, color=colors[0])
rect1 = plot.bar(ind+width, vals1, width, color=colors[1])

plot.set_ylabel('Number of measures')
plot.set_xlabel('Time signatures')
plot.set_xticks(ind+width)
plot.set_xticklabels(tuple([k[0] for k in keys]))
plot.legend((rect0[0], rect1[0]),
            tuple([x.capitalize() for x in compositores]))

autolabel(rect0)
autolabel(rect1)

fig.savefig('timesignatures_beethoven_mozart.png')

###################################

# plotamos o gráfico beethoven, mozart e scarlatti

fig = plt.figure(num=None, figsize=(15, 10))
plot = fig.add_subplot(111)

keys = set(list(chain(*tss))) # todas time signatures sem repeteco
keys = sorted([(k, float(Fraction(k))) for k in keys], key=lambda x: x[1])

ind = n.arange(len(keys)) # x das barras
width = 0.30 # tamanho das barras
colors = 'bgr' # cores usadas (apenas duas, para beethoven e mozart)

# beethoven
ts = tss[0]
vals0 = []
for k in keys:
    if k[0] not in ts.keys(): # nao tem essa chave
        vals0.append(0)
    else: # tem chave
        vals0.append(ts[k[0]])

# mozart
ts = tss[1]
vals1 = []
for k in keys:
    if k[0] not in ts.keys(): # nao tem essa chave
        vals1.append(0)
    else: # tem chave
        vals1.append(ts[k[0]])

# scarlatti
ts = tss[2]
vals2 = []
for k in keys:
    if k[0] not in ts.keys(): # nao tem essa chave
        vals2.append(0)
    else: # tem chave
        vals2.append(ts[k[0]])

rect0 = plot.bar(ind, vals0, width, color=colors[0])
rect1 = plot.bar(ind+width, vals1, width, color=colors[1])
rect2 = plot.bar(ind+(2*width), vals2, width, color=colors[2])

plot.set_ylabel('Number of measures')
plot.set_xlabel('Time signatures')
plot.set_xticks(ind+(width*2))
plot.set_xticklabels(tuple([k[0] for k in keys]))
plot.legend((rect0[0], rect1[0], rect2[0]),
            tuple([x.capitalize() for x in compositores]))

autolabel(rect0)
autolabel(rect1)
autolabel(rect2)

fig.savefig('timesignatures_scarlatti.png')
