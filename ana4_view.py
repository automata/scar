# coding: utf-8

import music21 as m, numpy as n
from itertools import groupby
import matplotlib.pyplot as plt
import pickle as pk

compositores = ['Beethoven', 'Mozart']

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plot.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

f = open('d1.pkl', 'rb')
qtd_notas_ambos, fator, cos,intervalos_scar, ids_scar, sonatas_ambos = pk.load(f)
f.close()


width = 0.35 # tamanho das barras
cores = 'bg'

fig = plt.figure(num=None, figsize=(80, 10))
for tol in range(0,4):
    fig.clf()
    plot = fig.add_subplot(111)
    corte = 0
    # beethoven
    ids = []
    ys = []
    i = 0
    for foo in cos[0][tol]:
        if foo > corte:
            ys.append(foo/fator)
            ids.append(i)
        i += 1
    ids = n.array(ids)
    ys = [x/fator for x in cos[0][tol]]
    ind = n.arange(len(ys))
    rect0 = plot.bar(ind, ys,
                     width, color=cores[0])
    # mozart
    ys = [x/fator for x in cos[1][tol]]
    ind2 = n.arange(len(ys))
    rect1 = plot.bar(ind2+width, ys,
                     width, color=cores[1])
    plot.set_ylabel('Occurrences')
    plot.set_xlabel('Motifs')
    plot.set_xticks(ind+width)
    plot.set_xticklabels(ids_scar)

    autolabel(rect0)
    autolabel(rect1)
    plot.legend((rect0[0], rect1[0]),
               tuple([x.capitalize() for x in compositores]))

    fig.autofmt_xdate()

    if tol == 0:
        plot.set_title('Strict')
    else:
        plot.set_title('Tolerance of $\pm%s$' % tol)
    
    fig.savefig('tolerancias_ambos_tol%s.png' % tol)

# sonatas beethoven
width = 0.35 # tamanho das barras
cores = 'rgbc'

sonatas = sonatas_ambos[0]

### tolerancia +-1
cortes = [5, 50, 300, 700]
for tol in xrange(1,5):
    corte = cortes[tol-1]
    s = [x[tol] for x in sonatas if x[tol] > corte]
    ind = n.arange(len(s))
    fig = plt.figure(figsize=(20,10))
    plot = fig.add_subplot(111)
    rect = plot.bar(ind, s, width)
    
    plot.set_ylabel('Occurrences')
    plot.set_xlabel('Sonatas')
    plot.set_xticks(ind+(width/2))
    plot.set_xticklabels([x[0][:-4] for x in sonatas if x[tol] > corte])
    autolabel(rect)
    if tol == 1:
        plot.set_title('Strict')
    else:
        plot.set_title('Tolerance of $\pm%s$' % (tol-1))
    fig.autofmt_xdate()
    fig.savefig('sonatas_beethoven_tol%s.png' % (tol-1))



# sonatas mozart
width = 0.35 # tamanho das barras
cores = 'rgbc'

sonatas = sonatas_ambos[1]

### tolerancia +-1
cortes = [5, 50, 300, 700]
cortes = [0]*4
for tol in xrange(1,5):
    corte = cortes[tol-1]
    s = [x[tol] for x in sonatas if x[tol] > corte]
    ind = n.arange(len(s))
    fig = plt.figure(figsize=(20,10))
    plot = fig.add_subplot(111)
    rect = plot.bar(ind, s, width, color='g')
    
    plot.set_ylabel('Occurrences')
    plot.set_xlabel('Sonatas')
    plot.set_xticks(ind+(width/2))
    plot.set_xticklabels([x[0][:-4] for x in sonatas if x[tol] > corte])
    autolabel(rect)
    if tol == 1:
        plot.set_title('Strict')
    else:
        plot.set_title('Tolerance of $\pm%s$' % (tol-1))
    fig.autofmt_xdate()
    fig.savefig('sonatas_mozart_tol%s.png' % (tol-1))



