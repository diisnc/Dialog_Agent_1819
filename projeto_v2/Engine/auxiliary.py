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


############## MAIN TEST ##############

def getPhrases(dialog, identifier):

    # list with json objets of dialog phrases, to return to user history (userHist)
    phrasesList = []

    # TYPES of dialog [Funny,Mock,Serious,Normal,Incentive]
    types = list(dialog.keys())
    
    for type in types:
        # Phrases IDs of each type [1,2,3,4,5,...]
        phrases = dialog[type] 
        for p in phrases:

            id = identifier+"|"+type+"|"+ str(p["ID"])
          
            phrase = { id : 0 } # counter inicial = 0

            phrasesList.append(phrase)

    return phrasesList


def getAllPhrases():

    phrases = []

    # greetingsI
    phrases += getPhrases(list_greetingsI,"greetingsI")
    # greetingsA
    phrases += getPhrases(list_greetingsA,"greetingsA")
    # greetingsA_Soon
    phrases += getPhrases(list_greetingsTSoon,"greetingsT|soon")
    # greetingsA_Late
    phrases += getPhrases(list_greetingsTLate,"greetingsT|late")
    # doubt
    phrases += getPhrases(list_doubt,"doubt")
    # farewell_bye
    phrases += getPhrases(list_farewell_bye,"farewell|bye")
    # farewell_badP
    phrases += getPhrases(list_farewell_badP,"farewell|badP")
    # farewell_goodP
    phrases += getPhrases(list_farewell_goodP,"farewell|goodP")
    # farewell_avgP
    phrases += getPhrases(list_farewell_avgP,"farewell|avgP")
    # domain
    phrases += getPhrases(list_domain,"domain")
    # subdomain
    phrases += getPhrases(list_subdomain,"subdomain")
    # time_out_badP
    phrases += getPhrases(list_time_out['badP'],"time|timeout|badP")
    # time_out_avgP
    phrases += getPhrases(list_time_out['avgP'],"time|timeout|avgP")
    # time_out_goodP
    phrases += getPhrases(list_time_out['goodP'],"time|timeout|goodP")
    # time_soon_badP
    phrases += getPhrases(list_time_soon['badP'],"time|timesoon|badP")
    # time_soon_avgP
    phrases += getPhrases(list_time_soon['avgP'],"time|timesoon|avgP")
    # time_soon_goodP
    phrases += getPhrases(list_time_soon['goodP'],"time|timesoon|goodP")
    # answer_right_easy
    phrases += getPhrases(list_answer_right_easy,"answer|right|easy")
    # answer_right_hard
    phrases += getPhrases(list_answer_right_hard,"answer|right|hard")
    # answer_wrong_easy
    phrases += getPhrases(list_answer_wrong_easy,"answer|wrong|easy")
    # answer_wrong_hard
    phrases += getPhrases(list_answer_wrong_hard,"answer|wrong|hard")

    return phrases
