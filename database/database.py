'''
- Correr mongod
- Correr este file
- Seguem-se algumas queries de consulta a usar no engine:

    funções úteis:  - db.collection.findOne(query, projection)
                    - (...)

'''
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
mycol = mydb["synonyms"]

col_dialog = mydb["dialogs"]
col_synonyms = mydb["synonyms"]

# mycol.find_one({},{"greetingsI"}) = retorna objeto JSON, get("greetingsI") = retorna array (que é o valor da key "greetingsI")
#list = mycol.find_one({},{"greetingsI"}).get("greetingsI")

# seleciona um elemento random da lista
#random_elem = random.choice(list)

# seleciona a frase do elemento
#phrase = random_elem["Phrase"]

#print(phrase)


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

# col_dialog.find_one({},{"greetingsI"}) = retorna objeto JSON, get("greetingsI") = retorna array (que é o valor da key "greetingsI")
list_greetingsI = col_dialog.find_one({}, {"greetingsI"}).get("greetingsI")
# seleciona um elemento random da lista
random_elem = random.choice(list_greetingsI)
# seleciona a frase do elemento
phrase = random_elem["Phrase"]

print(rep(synonyms("_day_")))