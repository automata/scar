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

# caminhos para todas as opus do beethoven:
paths = m.corpus.getComposer('beethoven')

# queremos a opus132
opus = m.corpus.parse(paths[0])
# ou m.corpus.parse('opus132')




