# coding: utf-8

import os

corpus = open('corpus_mozart.txt')
linhas = corpus.readlines()

opus = [l.split('/')[-1].replace('\n', '') for l in linhas]

for op in opus:
    print 'Baixando arquivo %s' % op
    os.system("wget 'http://kern.ccarh.org/data?l=mozart/sonatas&file=%s' -O corpus_mozart/%s" % (op, op))
