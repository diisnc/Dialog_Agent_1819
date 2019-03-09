from pprint import pprint
import fileinput
import re
from collections import Counter, defaultdict
import random
import sys

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer

import json


# GLOBAL VARIABLES
N = 3
i = 0
ocorrencias = defaultdict(Counter)

# FUNCTIONS
def loadDict():
    with open('synonyms.json', 'r', encoding='utf-8') as f:
        syn_dict = json.load(f)
    return syn_dict


def build():
    for line in fileinput.input(openhook=fileinput.hook_encoded("utf-8")):
        line = line + ' __END'
        words = re.split(r'\s+', line)
        ocorrencias['__BEGIN'][tuple(words[0:N-1])] += 1
        seq = [tuple(words[i:i+N]) for i in range(0,len(words) -N + 1)]
        for t in seq:
            ocorrencias[t[0:-1]][t[-1]] += 1


def generate():
    sentence = list(random.choices(list(ocorrencias['__BEGIN']), ocorrencias['__BEGIN'].values())[0])
    while sentence[-1] != '__END':
        state = (sentence[-2], sentence[-1])
        sentence.append(random.choices(list(ocorrencias[state]), ocorrencias[state].values())[0])
    return ' '.join(sentence[:-1])


def synonyms(sentence):
    words = word_tokenize(sentence)

    for i in range(0,len(words)):
        l_w = words[i].lower()
        if l_w in syn_dict:
            new_word = random.choices(syn_dict[l_w])[0]
            if words[i].istitle():
                words[i] = new_word.capitalize()
            else:
                words[i] = new_word
    
    output = TreebankWordDetokenizer().detokenize(words)
    return output
            


print('A carregar dicionario de sinonimos...')
syn_dict = loadDict()

'''
w = 'saudações'
if w in syn_dict:
    print(random.choices(syn_dict[w]))
'''
print('A construir gerador...')
build()

print('A gerar frases...')

f = open(sys.argv[1], "a", encoding="utf-8")

for i in range(0,10):
    sentence = synonyms(generate())
    f.write(sentence + '\n')

print('Concluido!')

