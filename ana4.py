# coding: utf-8

import music21 as m, numpy as n
from itertools import groupby

# importamos Piano Sonata No. 1 in F  minor, Op. 2, No. 1 [1793-5]
opus = m.converter.parse('corpus/sonata27-2.krn')

# vozes
print [voz.id for voz in opus.parts]
# spine_2 => G
# spine_0 => F

# qual voz queremos?
voz = opus.getElementById('spine_0')

# quais compassos? começa contar por 0...
compassos = voz.measures(1, 1000)

# percorremos cada compasso analisando as notas
comps = []
for compasso in compassos.getElementsByClass(m.stream.Measure)[:20]:
    print 'Compasso:', compasso.measureNumber
    notas = []
    # percorremos cada nota do compasso
    for nota in compasso.notes:
        # consideramos apenas notas
        if type(nota) == m.note.Note:
            # guardamos o valor MIDI da nota
            notas.append(nota.midi)
            print nota, nota.midi
    # guardamos todas as notas desse compasso em uma lista
    comps.append(notas)

# limpamos os repetidos consecutivos dos compassos
for i in xrange(len(comps)):
    comps[i] = [x[0] for x in groupby(comps[i])]

# limpamos os repetidos "das pontas"
for i in xrange(len(comps)-1):
    if len(comps[i]) > 0 and len(comps[i+1]) > 0:
        j = 0
        while (comps[i][-1] == comps[i+1][j]):
            del comps[i+1][j]
            
            if j == len(comps[i+1]):
                break
            j += 1

notas = sum(comps, [])

inters = [x-y for x,y in zip(notas, notas[1:])]

# [comp_ini, nota_ini, comp_fim, nota_fim, inter_comp-inter_scar]

intervalos_scar = [[9, -2, -2, -5],
                   [2, 2, -2, -2, 2, 2, -2, -2],
                   [4, 3, 5, 7, -3, -4],
                   [1, 4, -7]]

MAX_TOLERANCIA = 12

CC = []
for inter_scar in intervalos_scar:
    C = []
    for tol in xrange(MAX_TOLERANCIA):
        for i in xrange(len(inters)):
            inter = inters[i:i+len(inter_scar)]
            if len(inter) < len(inter_scar):
                break
            inci = sum([inter[j]-tol < inter_scar[j] < inter[j]+tol for j in range(len(inter_scar))])
            if inci == len(inter_scar):
                C.append([0, 0, 0, 0, [inter[k]-inter_scar[k] for k in xrange(len(inter))]])
    CC.append(C)

# CC = []
# for inter_scar in intervalos_scar:
#     C = []
#     for tol in xrange(MAX_TOLERANCIA):
#         for i in xrange(len(comps)):
#             comp = comps[i]
#             inter_comp = [x-y for x,y in zip(comp, comp[1:])]
#             if len(inter_scar) > len(inter_comp):
#                 # faltaram notas nesse compasso, precisamos pegar de outros
#                 necessarios = len(inter_scar) - len(inter_comp)
#                 qtds = []
#                 for k in xrange(i+1, len(comps)):
#                     necessarios = necessarios - len(comps[k])
#                     qtds.append(comps[k])
#                     if necessarios <= 0:
#                         break
#                 # coletamos as quantidades de notas faltantes
#                 notas 

#             inci = sum([inter_comp[j]-tol < inter_scar[j] < inter_comp[j]+tol for j in range(len(inter_scar))])
#             if inci == len(inter_scar):
#                 C.append([comp_ini, nota_ini, comp_fim, nota_fim, inter_comp-inter_scar])

