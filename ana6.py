# coding: utf-8

import music21 as m, numpy as n
from itertools import groupby, chain
import matplotlib.pyplot as plt
import pickle as pk

compositores = ['beethoven', 'mozart', 'scarlatti']
tss = []

for compositor in compositores:
    corpus = open('corpus_%s.txt' % compositor)
    linhas = corpus.readlines()
    hums = [l.split('/')[-1].replace('\n', '') for l in linhas]
    comps = {}
    
    # para cada sonata
    for hum in hums:
        print 'Sonata %s de %s' % (hum,compositor)
        print '-' * 80
        
        # importamos a sonata
        opus = m.converter.parse('corpus_%s/%s' % (compositor,hum))
        
        # procura quem é a clave de G
        ids_vozes = [voz.id for voz in opus.parts]
        
        if 'spine_0' in ids_vozes:
            voz_aguda = 'spine_0'
        elif 'spine_1' in ids_vozes:
            voz_aguda = 'spine_1'
        else:
            voz_aguda = 'spine_2'
        
        # selecionamos apenas a clave de G
        voz = opus.getElementById(voz_aguda)
        
        # pegamos todos os compassos
        compassos = voz.getElementsByClass('Measure')
        # percorremos cada compasso analisando as notas
        
        for compasso in compassos:
            ts = compasso.getContextByClass('TimeSignature').ratioString
            if ts not in comps.keys():
                comps[ts] = 0
            comps[ts] += 1
            
    tss.append(comps)

# plotamos o gráfico

fig = plt.figure(num=None, figsize=(15, 10))
plot = fig.add_subplot(111)

print tss
keys = set(list(chain(*tss))) # todas time signatures sem repeteco
ind = n.arange(len(keys)) # x das barras
width = 0.35 # tamanho das barras
colors = 'bg' # cores usadas (apenas duas, para beethoven e mozart)

f = open('d2.pkl', 'wb')
pk.dump(tss, f)
f.close()

# # beethoven
# ts = tss[0]
# vals = []
# for k in keys:
#     if k not in ts.keys(): # nao tem essa chave
#         vals.append(0)
#     else: # tem chave
#         vals.append(ts[k])
# rect0 = plot.bar(ind, vals, width, color=colors[0])

# # mozart
# ts = tss[1]
# vals = []
# for k in keys:
#     if k not in ts.keys(): # nao tem essa chave
#         vals.append(0)
#     else: # tem chave
#         vals.append(ts[k])
# rect1 = plot.bar(ind+width, vals, width, color=colors[1])

# plot.set_ylabel('Number of measures')
# plot.set_xlabel('Time signatures')
# plot.set_xticks(ind+width)
# plot.set_xticklabels(tuple(keys))
# plot.legend((rect0[0], rect1[0]),
#             tuple([x.capitalize() for x in compositores]))

# def autolabel(rects):
#     # attach some text labels
#     for rect in rects:
#         height = rect.get_height()
#         plot.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
#                 ha='center', va='bottom')

# autolabel(rect0)
# autolabel(rect1)

# fig.savefig('timesignatures_ambos.png')
