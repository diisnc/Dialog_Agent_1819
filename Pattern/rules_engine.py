import re
from pyknow import *
from pattern_analyser import *
from random import choice
from datetime import datetime
# pprint library is used to make the output look more pretty
import pymongo
from pprint import pprint
# nltk package
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer

# Connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["lei"]
col_dialog = mydb["dialogs"]
col_synonyms = mydb["synonyms"]

# col_dialog.find_one({},{"greetingsI"}) = retorna objeto JSON, get("greetingsI") = retorna array (que é o valor da key "greetingsI")
# greetingsI
list_greetingsI = col_dialog.find_one({}, {"greetingsI"}).get("greetingsI")
# greetingsA
list_greetingsA = col_dialog.find_one({}, {"greetingsA"}).get("greetingsA")


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
def rep(mystring):
    if "_name_" in mystring: 
        mystring = mystring.replace("_name_",p_analys.get_username())
    if "_day_" in mystring: #admitimos que está sempre no inicio da frase. Depois complicamos isto
        now = datetime.now()
        if(now.hour < 6 or now.hour > 20):
            mystring = mystring.replace("_day_","Boa noite")
        elif(now.hour < 12):
            mystring = mystring.replace("_day_","Bom dia")
        else:
            mystring = mystring.replace("_day_","Boa tarde")

    return mystring

# Pattern Fact
class Pattern(Fact):  
    '''
    Pattern(language , typeQ , domain ,subdomain , question , answer , question_lvl , student_lvl , state , 
            skill_domain , performance_domain , skill_subdomain , performance_subdomain, time)
    '''
    pass


### Rules Engine ###
class RulesEngine(KnowledgeEngine):
    
    '''
    ## Declare initial facts
    @DefFacts()
    def dialog_maker(self):
        yield Pattern(domain='Futebol',subdomain='Cenas',skill='Good',performance='Average',time="Good",language='EN')
        yield Question(typeQ = 'greetingsI')
    '''

    ## Declare rules
    @Rule(Pattern(typeQ='greetingsI'))
    def greetingsI (self):
        # seleciona um elemento random da lista
        random_elem = random.choice(list_greetingsI)
        # seleciona a frase e respetivas respostas do elemento
        phrase = random_elem["Phrase"]
        answers = random_elem["Answer"]
        print(rep(synonyms(phrase)))
        print(answers)

    @Rule(Pattern(typeQ='greetingsA'))
    def greetingsA (self):
        # seleciona um elemento random da lista
        random_elem = random.choice(list_greetingsA)
         # seleciona a frase e respetivas respostas do elemento
        phrase = random_elem["Phrase"]
        answers = random_elem["Answer"]
        print(rep(synonyms(phrase)))
        print(answers)

    @Rule(OR(   
            Pattern(skill_domain = L('Terrible') | L('Bad')),
            Pattern(performance_domain = L('Terrible') | L('Bad'))
            ))
    def teste2 (self):
        print('Teste 2')

    @Rule(AND(   
            Pattern(skill_subdomain = L('Terrible') | L('Bad')),
            Pattern(performance_domain = L('Terrible') | L('Bad')),
            Pattern(performance_subdomain = L('Terrible') | L('Bad'))
            ))
    def teste3 (self):
        print('Teste 3')



### PATTERN PARSER ###

# pattern
patt = ['John001', 'PT', 2, 'BD', 'Modelos ER', 'Gostas de pêras? Sim. Não.', 0, 3, 'B', 'processoX', 103, 53, 63, 15, 20]
# pattern analyser
p_analys = Pat_Analyser()
# pattern conversion
p_analys.pat_parser(patt)
# array w/ pattern fields (domain,subdomain,skill,performance,language,user,typeQ)
str_pat = p_analys.pat_string().split(",")
# print array above
print(str_pat)

### MAKE DECISION - by converting pattern into a fact and filtering it with rules previously declared in the program ###
# Init rules engine
print('Initializing engine rules')
watch('RULES', 'FACTS')   
aux = RulesEngine()   
aux.reset() 

# example of declaring fact
#aux.declare(Question(typeQ = 'greetingsI'))

# declare facts with pattern recieved
p = Pattern(username = str_pat[0], language = str_pat[1] , typeQ = str_pat[2] , domain = str_pat[3] ,subdomain = str_pat[4] , question = str_pat[5] , answer = str_pat[6] , 
            question_lvl = str_pat[7] , student_lvl = str_pat[8] , state = str_pat[9] , skill_domain = str_pat[10] , performance_domain = str_pat[11] ,
            skill_subdomain = str_pat[12] , performance_subdomain = str_pat[13], time = str_pat[14])
aux.declare(p)

# run engine
aux.run()
aux.facts

