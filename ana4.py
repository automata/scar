# coding: utf-8

import music21 as m, numpy as n
from itertools import groupby

# parametros
MAX_TOLERANCIA = 3
ARQ_SCARLATTI = 'motscar.txt'

# teste
#intervalos_scar = [[1,1], [1,2]]
#comps = [[], [60,62,64], [], [60,62,66, 60, 61], [60], [], [60,62], [60,60,62]]

# lemos os motivos do arquivo de conf
f = open(ARQ_SCARLATTI, 'r')
ln = f.readlines()
intervalos_scar = [[int(x) for x in l[1:-2].split(',')] for l in ln]

# corpus que iremos considerar
compositores = ['beethoven', 'mozart']

# analisamos cada compositor
for compositor in compositores:
    corpus = open('corpus_%s.txt' % compositor)
    linhas = corpus.readlines()
    
    hums = [l.split('/')[-1].replace('\n', '') for l in linhas]

    print '!' * 80
    print '!!!!! ANALISANDO %s !!!!!' % compositor
    print '!' * 80

    # e cada sonata de cada compositor
    for hum in hums:
        print 'Sonata %s de %s' % (hum, compositor)
        print '-' * 80

        # importamos a sonata
        opus = m.converter.parse('corpus_%s/%s' % (compositor, hum))

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
            notas = []
            # percorremos cada nota do compasso
            for nota in compasso.notes:
                # consideramos apenas notas
                if type(nota) == m.note.Note:
                    # guardamos o valor MIDI da nota
                    notas.append(nota.midi)
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

                    if comps[i][-1] != comps[i+1][j]:
                        break
                    j += 1

        # cria lista de intervalos considerando compassos
        inters = []
        ultimo = None
        for i in xrange(len(comps)):
            if len(comps[i]) == 0:
                inters.append([])
            else:
                if ultimo == None:
                    l = []
                    for j in xrange(len(comps[i])-1):
                        l.append(comps[i][j+1] - comps[i][j])
                        ultimo = comps[i][j+1]
                    inters.append(l)
                else:
                    l = [comps[i][0] - ultimo]
                    for j in xrange(len(comps[i])-1):
                        l.append(comps[i][j+1] - comps[i][j])
                        ultimo = comps[i][j+1]
                    if len(comps[i]) == 1:
                        ultimo = comps[i][0]
                    inters.append(l)

        # percorremos lista de intervalos e coletamos as incidências
        # para cada motivo intervalar de scarlatti
        C = []
        ci = 0
        for inter_scar in intervalos_scar:
            C_inter = []
            for tol in range(MAX_TOLERANCIA):
                C_tol = []
                for i in xrange(len(inters)):
                    inter = inters[i]
                    for j in xrange(len(inter)):
                        trecho = inter[j:j+len(inter_scar)]
                        c = None
                        if len(trecho) < len(inter_scar): # preciso de notas
                            completado = trecho[:]
                            k = 1
                            falta = None
                            # procuro notas nos proximos k compassos,
                            # ateh me fartar
                            while ((len(inter_scar) - len(completado)) > 0) and ((i+k) < len(inters)):
                                falta = len(inter_scar) - len(completado)
                                if (i+k) < len(inters):
                                    if len(inters[i+k]):
                                        completado.extend(inters[i+k][:falta])
                                    k += 1
                            if len(completado) == len(inter_scar):
                                c = [i, j, i+k-1, falta-1, completado, [completado[x]-inter_scar[x] for x in xrange(len(inter_scar))]]
                        else: # nao preciso procurar mais notas, jah estah ok
                            c = [i, j, i, j+len(inter_scar)-1, trecho, [trecho[x]-inter_scar[x] for x in xrange(len(inter_scar))]]
                        if c != None:
                            inci = [c[4][x]-tol <= inter_scar[x] <= c[4][x]+tol for x in xrange(len(inter_scar))]
                            if sum(inci) == len(inter_scar):
                                C_tol.append(c)
                C_inter.append(C_tol)
            C.append(C_inter)

        # sobre C...
        #
        # cada elemento em C possui uma lista com as tolerâncias
        # cada uma dessas listas contém uma lista de incidências
        # cada incidência tem o seguinte formato:
        #
        #   [compasso ini,
        #    nota ini,
        #    compasso fim,
        #    nota fim,
        #    motivo encontrado,
        #    motivo encontrado - motivo alvo]
        
        # gerando resultado/saida
        for i in xrange(len(C)):
            j = 0
            for inci in C[i]:
                print '\n\nPara motivo %s e tolerância +-%s, encontradas %s incidências.\n\n' % (intervalos_scar[i], j+1, len(inci))
                if inci != []:
                    print 'C.ini\tN ini\tC.fim\tN.fim\tM.encontrado'
                    print '-' * 80
                    for incii in inci:
                        print '%s\t%s\t%s\t%s\t%s' % (incii[0]+1, incii[1]+1, incii[2]+1, incii[3]+1, incii[4])
                j += 1
            print '\n'
            print '*' * 80
