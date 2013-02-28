# encode: utf-8

import os

corpus = open('corpus.txt')
linhas = corpus.readlines()

opus = [l.split('/')[-1].replace('\n', '') for l in linhas]

for op in opus:
    os.system("wget 'http://kern.ccarh.org/data?l=beethoven/sonatas&file=%s' -O corpus/%s" % (op, op))
