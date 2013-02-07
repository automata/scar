# coding: utf-8

import music21 as m

# intervalos (em semitons) das frases de interesse nas opus de beethoven:
# K12:     -5 +9 -2 -2 -5 | +2 -2 -2 -3 | +0 -1 -2 -4 | +0 -2 -2
# K135:    +2 +2 -2 -2 +2 +2 -2 -2
# K6:      +4 +3 +5 +7 -3 -4
# K13 C22: +1 +4 -7

# importando corpus:
# http://mit.edu/music21/doc/html/referenceCorpus.html#referencecorpus
# http://mit.edu/music21/doc/html/referenceCorpus.html#ludwig-van-beethoven

# opus132: String Quartet No.15
# opus133: Große Fuge, Op.133
# opus18 no1: String Quartet No.1, Op.18 No.1
# opus18 no2: String Quartet No.2, Op.18 No.2
# opus18 no4: String Quartet No.2, Op.18 No.4
# opus18 no5: String Quartet No.2, Op.18 No.5
# opus59 no1: String Quartet No.7, Op.59 No.1
# opus59 no2: String Quartet No.8, Op.59 No.2
# opus59 no3: String Quartet No.9, Op.59 No.3
# opus74: String Quartet No.10, Op.74

# caminhos para todas as opus do beethoven:
paths = m.corpus.getComposer('beethoven')

# queremos a opus132
opus = m.corpus.parse(paths[0])
# ou m.corpus.parse('opus132')

# opus é um Score. um Score possui Parts. Parts possui Instrument, Measures.
# Measures possuem TimeSignature, Clef, KeySignature, Note, Silence

# vamos ver quais Parts existem no Score
print [voz.id for voz in opus.parts]
# [u'Violin I', u'Violin II', u'Viola', u'Violoncello']

# queremos apenas o primeiro violino
voz = opus.getElementById('Violin I')
# ou... voz = opus.parts[0]

# vamos percorrer todos os 10 primeiros compassos dessa voz
for compasso in voz.measures(1, 10):
    
    
