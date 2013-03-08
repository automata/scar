* Arquivos e diretórios

corpus/           Arquivos Kern e partituras em PDF que estamos usando 
                  (sonatas de Beethoven)

corpus.txt        Lista os arquivos que estão no corpus/

ana2.py           Lê uma sonata em corpus/ e procura por intervalos
                  usados por Scarlatti

downloadsonatas.py Faz download de todas as 32 sonatas de Beethoven do
                    KernScores


== Descrição do algoritmo em ana2 ==

O programa carrega uma sonata, no momento estamos usando arquivos .krn.
Então, há a escolha de uma voz da sonata, e a obtenção de todas as notas,
somente as alturas, em sequência. Por último, são removidas todas as notas
repetidas.

Depois disso, o programa percorre a voz, começando em cada nota, para procurar
os temas/traços/motivos de interesse, levando em consideração somente a direção do movimento.
Depois de percorridas as vozes, e registradas as incidências,
as linhas são novamente percorridas para obtenção dos compassos das incidências.


== Descrição do algoritmo em ana3 ==

Igual a ana2, mas são percorridas todas as vozes de todas as sonatas.
