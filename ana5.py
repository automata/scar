# coding: utf-8

import music21 as m, numpy as n
from itertools import groupby
import matplotlib.pyplot as plt

# parametros
MAX_TOLERANCIA = 4

corpus = open('corpus_beethoven.txt')
linhas = corpus.readlines()
hums = [l.split('/')[-1].replace('\n', '') for l in linhas]

# para cada sonata
for hum in hums:
    print 'Sonata %s de Beethoven'
    print '-' * 80
    
    # importamos a sonata
    opus = m.converter.parse('corpus_beethoven/%s' % (hum))

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
    
    # quais compassos? começa contar por 0...
    compassos = voz.measures(1, 1000)
        
    # percorremos cada compasso analisando as notas
    comps = []
    for compasso in compassos.getElementsByClass(m.stream.Measure):
        print compasso.timeSignature
        
