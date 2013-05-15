# coding: utf-8

import music21 as m, numpy as n
from itertools import groupby
import matplotlib.pyplot as plt
import pickle as pk

# parametros
MAX_TOLERANCIA = 4
ARQ_SCARLATTI = 'motscar_199.txt'

# lemos os motivos do arquivo de conf
intervalos_scar = []
ids_scar = []
for line in open(ARQ_SCARLATTI):
    if line.strip():
        partes = line.split(']')
        mot = partes[0].replace('[', '')
        ide = partes[1].replace('\n', '')
        intervalos_scar.append([int(x) for x in mot.split(',')])
        ids_scar.append(ide)

# corpus que iremos considerar
compositores = ['beethoven', 'mozart']

cos = []
qtd_notas_ambos = []
sonatas_ambos = []

# analisamos cada compositor
for compositor in compositores:
    corpus = open('corpus_%s.txt' % compositor)
    linhas = corpus.readlines()
    enco_todos = []
    qtd_notas = 0
    hums = [l.split('/')[-1].replace('\n', '') for l in linhas]
    sonatas = []
    
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

        # contamos as notas de cada compasso dessa sonata e soma ao todo
        qtd_notas += sum([len(comp) for comp in comps])

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
        enco = []
        for i in xrange(len(C)):
            j = 0
            for inci in C[i]:
                enco.append([intervalos_scar[i], j+1, len(inci)])
                if len(inci) != 0:
                    if j != 0:
                        print '\n\nPara motivo %s %s e tolerância +-%s, encontradas %s incidências.\n\n' % (intervalos_scar[i], ids_scar[i], j, len(inci))
                    else:
                        print '\n\nPara motivo %s %s ESTRITO, encontradas %s incidências.\n\n' % (intervalos_scar[i], ids_scar[i], len(inci))
                    print 'C.ini\tN ini\tC.fim\tN.fim\tM.encontrado'
                    print '-' * 80
                    for incii in inci:
                        print '%s\t%s\t%s\t%s\t%s' % (incii[0]+1, incii[1]+1, incii[2]+1, incii[3]+1, incii[4])
                j += 1
            #print '\n'
            #print '*' * 80
        print '\n'
        # para motivo x, quantidade de incidencias em enco
        #print enco
        enco_todos.append(enco)
        sonatas.append([hum,
                        sum([x[2] for x in enco if x[2] > 0 and x[1] == 1]),
                        sum([x[2] for x in enco if x[2] > 0 and x[1] == 2]),
                        sum([x[2] for x in enco if x[2] > 0 and x[1] == 3]),
                        sum([x[2] for x in enco if x[2] > 0 and x[1] == 4])])

    # para gerar gráfico de tolerâncias
    co = []
    for j in xrange(MAX_TOLERANCIA):
        bar = []
        for i in xrange(len(intervalos_scar)):
            l = MAX_TOLERANCIA
            foo = sum([[y[2] for y in x[i*l:i*l+l]][j] for x in enco_todos])
            bar.append(foo)
        co.append(bar)
    cos.append(co)

    qtd_notas_ambos.append(qtd_notas)

    sonatas_ambos.append(sonatas)

# depois fazer razão com qtd_notas_ambos[0] (beethoven) e qtd_notas_ambos[1]
# (mozart)
#print qtd_notas_ambos

fator = float(qtd_notas_ambos[0]) / qtd_notas_ambos[1]

# guardando dados
f = open('d1.pkl', 'wb')
pk.dump((qtd_notas_ambos, fator, cos, intervalos_scar, ids_scar,
         sonatas_ambos), f)
f.close()

# print qtd_notas_ambos[0], qtd_notas_ambos[1], fator

# fig = plt.figure(num=None, figsize=(15, 10))
# plot = fig.add_subplot(111)
# # beethoven
# cores = 'cbgr'
# for i in xrange(MAX_TOLERANCIA):
#     plot.plot(range(len(intervalos_scar)), [x/fator for x in cos[0][i]], color=cores[i], marker='o')
# # mozart
# for i in xrange(MAX_TOLERANCIA):
#     plot.plot(range(len(intervalos_scar)), [x/fator for x in cos[1][i]], color=cores[i], marker='+', alpha=.6)

# plot.legend(('Beethoven estrito', 'Beethoven $\pm1$', 'Beethoven $\pm2$', 'Beethoven $\pm3$',
#              'Mozart estrito', 'Mozart $\pm1$', 'Mozart $\pm2$', 'Mozart $\pm3$'), shadow=True)
# plot.set_xticks(range(len(intervalos_scar)))
# plot.set_xticklabels(ids_scar)
# plot.set_xlim((0,len(intervalos_scar)-1))
# fig.autofmt_xdate()
# plot.set_title('Incidencias em sonatas de Beethoven e Mozart considerando tolerancias')
# plot.set_xlabel('motivos')
# plot.set_ylabel('incidencias (em todas as sonatas do corpus)')
# fig.savefig('tolerancias_ambos.png')

# #### gráfico beethoven

# fig = plt.figure(num=None, figsize=(15, 10))
# plot = fig.add_subplot(211)
# # beethoven
# cores = 'kbgr'
# for i in xrange(MAX_TOLERANCIA):
#     plot.plot(range(len(intervalos_scar)), cos[0][i], color=cores[i], marker='o')
# plot.legend(('Estrito', 'Tolerancia $\pm1$', 'Tolerancia $\pm2$', 'Tolerancia $\pm3$'), shadow=True)
# plot.set_xticks(range(len(intervalos_scar)))
# plot.set_xticklabels(ids_scar)
# plot.set_xlim((0,len(intervalos_scar)-1))
# fig.autofmt_xdate()
# plot.set_title('Incidencias em sonatas de Beethoven considerando tolerancias')
# plot.set_xlabel('motivos')
# plot.set_ylabel('incidencias (em todas as sonatas)')

# plot = fig.add_subplot(212)
# # mozart
# for i in xrange(MAX_TOLERANCIA):
#     plot.plot(range(len(intervalos_scar)), cos[1][i], color=cores[i], marker='o')

# plot.legend(('Estrito', 'Tolerancia $\pm1$', 'Tolerancia $\pm2$', 'Tolerancia $\pm3$'), shadow=True)
# plot.set_xticks(range(len(intervalos_scar)))
# plot.set_xticklabels(ids_scar)
# plot.set_xlim((0,len(intervalos_scar)-1))
# fig.autofmt_xdate()
# plot.set_title('Incidencias em sonatas de Mozart considerando tolerancias')
# plot.set_xlabel('motivos')
# plot.set_ylabel('incidencias (em todas as sonatas)')
# fig.savefig('tolerancias_separados.png')

