import random
import json
import re
from datetime import datetime
# PyKnow Rules Engine
from pyknow import *
from pprint import pprint
# nltk package
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
# Collector Module
from collector import *
# Generator Module
from generator import *

################################### Auxiliary Functions ###################################

#JSON pattern reader
def pattern_reader(file):
    input_file = open (file)
    json_array = json.load(input_file)
    # [1, 1, 1, 1, 1, 3, 4, 123443, 4, 4, 3, 4, 3, 'greetingsI']
    patt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    patt[0] = json_array['username']
    patt[1] = json_array['language']
    patt[2] = json_array['domain']
    patt[3] = json_array['subdomain']
    patt[4] = json_array['answer']
    patt[5] = json_array['question_lvl']
    patt[6] = json_array['student_lvl']
    patt[7] = json_array['state']
    patt[8] = json_array['skill_domain']
    patt[9] = json_array['performance_domain']
    patt[10] = json_array['skill_subdomain']
    patt[11] = json_array['performance_subdomain']
    patt[12] = json_array['time']
    patt[13] = json_array['typeQ']

    return patt

# Function that replaces a word with synonym
def synonyms(sentence):
    words = word_tokenize(sentence)

    for i in range(0,len(words)):
        l_w = words[i].lower()
        synonyms = col_synonyms.find_one({}, {l_w}).get(l_w)
        if synonyms:
            new_word = random.choices(synonyms)[0]
            if words[i].istitle() or words[i] == '_day_':
                words[i] = new_word.capitalize()
            else:
                words[i] = new_word
    
    output = TreebankWordDetokenizer().detokenize(words)
    return output

# Funtion that replaces _name_ and _day_ by username and day
def rep(mystring, username):
    if "_name_" in mystring: 
        mystring = mystring.replace("_name_", username)
    if "_day_" in mystring:
        now = datetime.now()
        if(now.hour < 6 or now.hour > 20):
            mystring = mystring.replace("_day_","Boa noite")
        elif(now.hour < 12):
            mystring = mystring.replace("_day_","Bom dia")
        else:
            mystring = mystring.replace("_day_","Boa tarde")

    return mystring


# Choose dialog element having into account the type and counter of the phrase
def choose_dialog(list_typeQ, types, username, tag, subtag):

        dataset = []

        # CHOOSE TYPE: If type == "All" then choose randomly
        if types[0] == "All":
            types = list(list_typeQ.keys()) 

        if not tag :
            for t in types:
                dataset += list_typeQ[t]
        # GREETINGS & DOUBT
        # Phrases
        elif tag == "Phrases":
            for t in types:
                dataset += list_typeQ[t][tag]
        # Answers
        elif tag: 
            for t in types:
                dataset += list_typeQ[t][tag][subtag]

        # Result
        randomResult =  generate(dataset)
        randomResult =  rep(synonyms(randomResult), username)
        
        return randomResult
