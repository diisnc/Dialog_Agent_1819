import re
from collections import Counter, defaultdict
import random
import sys

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer

from collector import *


# GLOBAL VARIABLES
N = 3
i = 0
occurrences = defaultdict(Counter)

# Build words dictionary
def build(dataset):

    for line in dataset:
        line = line + ' __END'
        words = re.split(r'\s+', line)
        occurrences['__BEGIN'][tuple(words[0:N-1])] += 1
        seq = [tuple(words[i:i+N]) for i in range(0,len(words) -N + 1)]
        for t in seq:
            occurrences[t[0:-1]][t[-1]] += 1

# Generate sentences
def gen():
    sentence = list(random.choices(list(occurrences['__BEGIN']), occurrences['__BEGIN'].values())[0])
    while sentence[-1] != '__END':
        state = (sentence[-2], sentence[-1])
        sentence.append(random.choices(list(occurrences[state]), occurrences[state].values())[0])
    return ' '.join(sentence[:-1])


# Start generator
def generate(dataset):

    sentences = []

    # Build gnerator
    build(dataset)

    # Generates 50 sentences
    for i in range(0,50):
        sentence = gen()+'\n'
        
        if isinstance(sentence, str) and sentence != '':
            sentences.append(sentence)

    # Chooses one random sentence
    result = random.choice(sentences)

    occurrences.clear()

    return result


