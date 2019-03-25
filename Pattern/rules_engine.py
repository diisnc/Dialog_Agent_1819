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
col_generic = mydb["generic_dialog"]
col_BD = mydb["BD_dialog"]
col_synonyms = mydb["synonyms"]

############################## Dialogs ######################################
# Generic
generic_dialog = col_generic.find_one()
# BD domain
bd_dialog = col_BD.find_one()
#############################################################################

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

        # TODO: Fazer increment do counter no MONGODB??

        return chosen_elem


# Pattern Fact
class Pattern(Fact):  
    '''
    Pattern(language , typeQ , domain ,subdomain , question , answer , question_lvl , student_lvl , state , 
            skill_domain , performance_domain , skill_subdomain , performance_subdomain, time)
    '''
    pass

# Rule execution Fact, to manage rules execution: only one rule executes at a time
class Rule_exe(Fact):  
    '''
    Rule_exe(executed = False)
    '''
    pass


### Rules Engine ###
class RulesEngine(KnowledgeEngine):
    
    
    ## Declare initial facts
    @DefFacts()
    def dialog_maker(self):
        yield Rule_exe(executed = False)
    
    
    ## Declare rules
    # Greeting for the first time
    @Rule(Pattern(typeQ='greetingsI'))
    def greetingsI (self):
        # selects an element from the list, having into account its type
        dialog = choose_dialog(list_greetingsI,"All")
        # selects the phrase and respective answers from the element dialog
        phrase = dialog["Phrase"]
        answers = dialog["Answer"]
        print(rep(synonyms(phrase)))
        print(answers)

    # Greeting again
    @Rule(Pattern(typeQ='greetingsA'))
    def greetingsA (self):
        dialog = choose_dialog(list_greetingsA,"All")
        phrase = dialog["Phrase"]
        answers = dialog["Answer"]
        print(rep(synonyms(phrase)))
        print(answers)

    # Wrong answer, easy question
    @Rule(Pattern(answer = '0', question_lvl = L('1') | L('2') | L('3')), Rule_exe(executed = False))
    def wrong_easy (self):
        dialog = choose_dialog(list_answer_wrong_easy,"All")
        phrase = dialog["Phrase"]
        print(rep(synonyms(phrase)))
        self.modify(self.facts[1], executed= True)

    # Wrong answer, hard question
    @Rule(Pattern(answer = '0', question_lvl = L('4') | L('5')), Rule_exe(executed = False))
    def wrong_hard (self):
        dialog = choose_dialog(list_answer_wrong_hard,"All")
        phrase = dialog["Phrase"]
        print(rep(synonyms(phrase)))
        self.modify(self.facts[1], executed= True)

    # Right answer, easy question
    @Rule(Pattern(answer = '1', question_lvl = L('1') | L('2') | L('3')), Rule_exe(executed = False))
    def right_easy (self):
        dialog = choose_dialog(list_answer_right_easy,"All")
        phrase = dialog["Phrase"]
        print(rep(synonyms(phrase)))
        self.modify(self.facts[1], executed= True)

    # Right answer, hard question
    @Rule(Pattern(answer = '1', question_lvl = L('4') | L('5')), Rule_exe(executed = False))
    def right_hard (self):
        dialog = choose_dialog(list_answer_right_hard,"All")
        phrase = dialog["Phrase"]
        print(rep(synonyms(phrase)))
        self.modify(self.facts[1], executed= True)

    # Wrong answer, easy question, good student
    @Rule(Pattern(answer = '0', question_lvl = L('1') | L('2') | L('3'), student_lvl = L('A') | L('B')), Rule_exe(executed = False), salience=1)
    def wrong_easy_goodSt (self):
        dialog = choose_dialog(list_answer_wrong_easy,"Mock")
        phrase = dialog["Phrase"]
        print(rep(synonyms(phrase)))
        self.modify(self.facts[1], executed= True)
    
    '''
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
    
    @Rule(Pattern(language='PT'), Rule_exe(executed = False), salience=1)
    def teste4 (self):
        print('Teste 4')
        self.modify(self.facts[1], executed= True)

    @Rule(Pattern(language='PT', domain='BD'), Rule_exe(executed = False), salience=0)
    def teste5 (self):
        print('Teste 5')
        self.modify(self.facts[1], executed= True)
        '''



### PATTERN PARSER ###

# pattern
patt = ['John001', 'PT', 3, 'BD', 'Modelos ER', 'Gostas de pêras? Sim. Não.', 0, 2, 'B', 'processoX', 103, 53, 63, 15, 20]
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

# declare facts with pattern recieved
p = Pattern(username = str_pat[0], language = str_pat[1] , typeQ = str_pat[2] , domain = str_pat[3] ,subdomain = str_pat[4] , question = str_pat[5] , answer = str_pat[6] , 
            question_lvl = str_pat[7] , student_lvl = str_pat[8] , state = str_pat[9] , skill_domain = str_pat[10] , performance_domain = str_pat[11] ,
            skill_subdomain = str_pat[12] , performance_subdomain = str_pat[13], time = str_pat[14])
aux.declare(p)

# run engine
aux.run()
aux.facts

