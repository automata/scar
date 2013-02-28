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
comp = []
for compasso in compassos.getElementsByClass(m.stream.Measure):
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
    comp.extend(notas)

# portanto, comp tem todas as notas, de todos os compassos, em ordem

# vamos calcular os intervalos (em semitons) das notas da opus de beethoven
intervalos_bee = [x-y for x,y in zip(comp, comp[1:])]
while 1:
    try:
        intervalos_bee.remove(0)
    except:
        break


# vamos procurar por esses intervalos usados por scarlatti no opus de beethoven
# K12:     -5 +9 -2 -2 -5 | +2 -2 -2 -3 | +0 -1 -2 -4 | +0 -2 -2
# K135:    +2 +2 -2 -2 +2 +2 -2 -2
# K6:      +4 +3 +5 +7 -3 -4
# K13 C22: +1 +4 -7
#intervalos_scar = [[-5, 9, -2, -2, -5, 2, -2, -2, -3, -1, -2, -4, -2, -2],
intervalos_scar = [[9, -2, -2, -5],
                   [2, 2, -2, -2, 2, 2, -2, -2],
                   [4, 3, 5, 7, -3, -4],
                   [1, 4, -7]]

# vamos armazenar em encontrados as quantidades de motivos encontrados em
# beethoven
encontrados = []
onde=[]
# para cada motivo do scarlatti...
for inte in intervalos_scar:
    conta_encontrados = 0
    onde.append([])
    # vamos procurar em todos os trechos possíveis das notas do beethoven
    for i in xrange(len(intervalos_bee)):
        trecho = intervalos_bee[i:len(inte)+i]
        if len(trecho) == len(inte):
            print "Procurando %s em %s: %s" % (inte, intervalos_bee, trecho)
            # quando os intervalos baterem, somamos 1 aos encontrados
            if list((n.array(inte)>0)*2-1) == list((n.array(trecho)>0)*2-1):
            #if inte == trecho:
                conta_encontrados = conta_encontrados + 1
                onde[-1].append(i)
            if list((n.array(inte)>0)*2-1) == -1*list((n.array(trecho)>0)*2-1):
            #if inte == [-t for t in trecho]:
                conta_encontrados = conta_encontrados + 1
                onde[-1].append(i)
    encontrados.append(conta_encontrados)

# portanto, encontrados é uma lista com a quantidade de cada motivo encontrado

# apenas mostramos na tela quantos motivos encontramos e quais são
for i in xrange(len(intervalos_scar)):
    print 'Encontrados %s motivos iguais a %s.' % (encontrados[i],
                                                   intervalos_scar[i])

# percorremos cada compasso analisando as notas
comp = []
for compasso in compassos.getElementsByClass(m.stream.Measure):
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
    comp.append(notas)

compassos_incidencias=[]

for o in onde:
    compassos_incidencias.append([])
    ii=0
    compasso=0
    for i in o: # para cada incidencia do motivo
        n_notas=0
        while ii<i: #achando a nota
           c=[x[0] for x in groupby(comp[compasso])]
           ii+=len(c)
           if compasso > 0:
               try:
                   if c[0] ==comp[compasso-1][-1]:
                       ii-=1
               except:
                   pass
           compasso+=1
        compassos_incidencias[-1].append(compasso)

            
            








