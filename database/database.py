import sys
import pymongo
import random
from datetime import datetime
# pprint library is used to make the output look more pretty
from pprint import pprint

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer

# Connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["lei"]
col_generic = mydb["generic_dialog"]
col_BD = mydb["BD_dialog"]
col_synonyms = mydb["synonyms"]

###### Dialogs ######
# Generic
generic_dialog = col_generic.find_one()
# BD domain
bd_dialog = col_BD.find_one()

# ["greetingsI"] = returns phrases grouped by type (which is the value of key "greetingsI")
# greetingsI
list_greetingsI = generic_dialog["greetingsI"]
# greetingsA
list_greetingsA = generic_dialog["greetingsA"]
# doubt
list_doubt = generic_dialog["doubt"]
# farewell_bye
#list_farewell_bye = generic_dialog["farewell"]["bye"]
# farewell_badP
#list_farewell_badP = generic_dialog["farewell"]["badP"]
# farewell_goodP
#list_farewell_goodP = generic_dialog["farewell"]["goodP"]
# farewell_avgP
#list_farewell_avgP = generic_dialog["farewell"]["avgP"]
# domain
list_domain = generic_dialog["domain"]
# subdomain
list_subdomain = bd_dialog["subdomain"]
# time_out
list_time = bd_dialog["time"]["timeout"]
# too_soon
list_time = bd_dialog["time"]["toosoon"]
# answer_right_easy
list_answer_right_easy = bd_dialog["answer"]["right"]["easy"]
# answer_right_hard
list_answer_right_hard = bd_dialog["answer"]["right"]["hard"]
# answer_wrong_easy
list_answer_wrong_easy = bd_dialog["answer"]["wrong"]["easy"]
# answer_wrong_hard
list_answer_wrong_hard = bd_dialog["answer"]["wrong"]["hard"]


# Function that replaces a word with synonym
def synonyms(sentence):
    words = word_tokenize(sentence)

    for i in range(0,len(words)):
        l_w = words[i].lower()
        synonyms = col_synonyms.find_one({}, {l_w}).get(l_w)
        if synonyms:
            new_word = random.choices(synonyms)[0]
            if words[i].istitle() or words[i] == '_day_' :
                words[i] = new_word.capitalize()
            else:
                words[i] = new_word
    
    output = TreebankWordDetokenizer().detokenize(words)
    return output

# Funtion that replaces _name_ and _day_ by username and day
def rep(mystring):
    if "_name_" in mystring: 
        mystring = mystring.replace("_name_","John")
    if "_day_" in mystring: #admitimos que está sempre no inicio da frase. Depois complicamos isto
        now = datetime.now()
        if(now.hour < 6 or now.hour > 20):
            mystring = mystring.replace("_day_","Boa noite")
        elif(now.hour < 12):
            mystring = mystring.replace("_day_","Bom dia")
        else:
            mystring = mystring.replace("_day_","Boa tarde")

    return mystring



# Choose dialog element having into account the type and counter of the phrase
def choose_dialog(list_typeQ, typeP):
        chosen_dialogs = []
        list_typeP = []
        
        # If type == "All" then choose random type
        if typeP == "All":
            typeP = random.choice(list(list_typeQ.keys()))

        list_typeP = list_typeQ[typeP]

        min_counter = list_typeP[0]["Counter"]

        # Getting smallest counter
        for elem in list_typeP:
            if elem["Counter"] < min_counter:
                min_counter = elem["Counter"]

        # Always chooses the phrases with the smallest counter
        for elem in list_typeP:
            if elem["Counter"] == min_counter:
                chosen_dialogs.append(elem)

        # Choose random element from list with elements with smallest counter
        chosen_elem = random.choice(chosen_dialogs)

        # Increment counter in list
        chosen_elem["Counter"]+=1

        return chosen_elem

print(choose_dialog(list_answer_wrong_easy,"All"))