# coding: utf-8

import music21 as m

corpus = open('corpus.txt')
linhas = corpus.readlines()

hums = [l.split('/')[-1].replace('\n', '') for l in linhas]

for hum in hums:
    print 'Convertendo arquivo %s para MIDI' % hum
    # importamos o humdrum
    opus = m.converter.parse('corpus/%s' % hum)

    # acha a voz mais aguda, se é o id spine_1 ou spine_2
    ids_vozes = [voz.id for voz in opus.parts]
    if 'spine_1' in ids_vozes:
        voz_aguda = 'spine_1'
    else:
        voz_aguda = 'spine_2'

    # qual voz queremos? apenas a mais aguda
    voz = opus.getElementById(voz_aguda)

    # converte para notas midi
    mf = m.midi.translate.streamToMidiFile(voz)
    # escreve o arquivo midi
    mf.open('midi/%s.mid' % hum.split('.')[0], 'wb')
    mf.write()
    mf.close()
