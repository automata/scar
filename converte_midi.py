# coding: utf-8

import music21 as m

arqs = ['corpus.txt', 'corpus_mozart.txt', 'corpus_scarlatti.txt']

for arq in arqs:
    corpus = open(arq)
    linhas = corpus.readlines()
    
    hums = [l.split('/')[-1].replace('\n', '') for l in linhas]

    print 'Corpus: %s' % arq
    
    for hum in hums:
        print 'Convertendo arquivo %s para MIDI' % hum
        # importamos o humdrum
        if 'mozart' in arq:
            opus = m.converter.parse('corpus_mozart/%s' % hum)
        elif 'scarlatti' in arq:
            opus = m.converter.parse('corpus_scarlatti/%s' % hum)
        else:
            opus = m.converter.parse('corpus/%s' % hum)
        
        # acha a voz mais aguda, se é o id spine_1 ou spine_2
        ids_vozes = [voz.id for voz in opus.parts]
        print ids_vozes
        if 'spine_1' in ids_vozes:
            voz_aguda = 'spine_1'
        else:
            voz_aguda = 'spine_2'

        # qual voz queremos? apenas a mais aguda
        voz = opus.getElementById(voz_aguda)
        
        # converte para notas midi
        mf = m.midi.translate.streamToMidiFile(voz)
        # escreve o arquivo midi
        if 'mozart' in arq:
            mf.open('midi_mozart/%s.mid' % hum.split('.')[0], 'wb')
        elif 'scarlatti' in arq:
            mf.open('midi_scarlatti/%s.mid' % hum.split('.')[0], 'wb')
        else:
            mf.open('midi/%s.mid' % hum.split('.')[0], 'wb')
        mf.write()
        mf.close()
