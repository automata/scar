# coding: utf-8

import os

corpus = open('corpus_scarlatti.txt')
linhas = corpus.readlines()

opus = [l.split('/')[-1].replace('\n', '') for l in linhas]

for op in opus:
    print 'Baixando arquivo %s' % op
    os.system("wget 'http://kern.ccarh.org/data?l=scarlatti/sonatas&file=%s' -O corpus_scarlatti/%s" % (op, op))
