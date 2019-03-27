import random
from datetime import datetime
# PyKnow Rules Engine
from pyknow import *
# pprint library is used to make the output look more pretty
import pymongo
from pprint import pprint
# nltk package
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer

# Connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["lei"]
col_generic = mydb["dialog"]
col_BD = mydb["domain_BD"]
col_synonyms = mydb["synonyms"]

############################## Dialogs MongoDB ######################################
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
list_farewell_bye = generic_dialog["farewell"]["bye"]
# farewell_badP
list_farewell_badP = generic_dialog["farewell"]["badP"]
# farewell_goodP
list_farewell_goodP = generic_dialog["farewell"]["goodP"]
# farewell_avgP
list_farewell_avgP = generic_dialog["farewell"]["avgP"]
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


################################### Auxiliar Functions ###################################
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


############## Pattern Fact ##############
class Pattern(Fact):  
    '''
    Pattern(language, typeQ, domain, subdomain, question, answer, question_lvl, 
            student_lvl, state, skill_domain, performance_domain, skill_subdomain, 
            performance_subdomain, time)
    '''
    pass

############## Rule execution Fact, to manage rules execution: only one rule executes at a time 
class Rule_exe(Fact):  
    '''
    Rule_exe(executed = False)
    '''
    pass


############## Rules Engine ##############
class RulesEngine(KnowledgeEngine):

    __username = ""
    __result = ""

    
    def __init__(self,username):
        __username = username
        __result = ""
        super().__init__()


    ## Declare initial facts
    @DefFacts()
    def dialog_maker(self):
        yield Rule_exe(executed = False)
    
    
    ## Declare rules
    # Greeting for the first time
    @Rule(Pattern(typeQ = 'greetingsI'))
    def greetingsI (self):
        # selects an element from the list, having into account its type
        dialog = choose_dialog(list_greetingsI,"All")
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Greeting again
    @Rule(Pattern(typeQ = 'greetingsA'), Rule_exe(executed = False))
    def greetingsA (self):
        dialog = choose_dialog(list_greetingsA,"All")
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # [TEST] Greeting again, student_lvl = E ou student_lvl = D  [OUTPUT: funny]
    @Rule(Pattern(typeQ = 'greetingsA', student_lvl = L('E') | L('D'), Rule_exe(executed = False), salience=1))
    def greetingsA (self):
        dialog = choose_dialog(list_greetingsA,"Funny")
        phrase = dialog["Phrase"]
        answers = dialog["Answer"]
        print(rep(synonyms(phrase)))
        print(answers)


    # [TEST] Greeting again, student_lvl = A ou student_lvl = B  [OUTPUT: mock]
    @Rule(Pattern(typeQ = 'greetingsA', student_lvl = L('A') | L('B'), Rule_exe(executed = False), salience=1))
    def greetingsA (self):
        dialog = choose_dialog(list_greetingsA,"Mock")
        phrase = dialog["Phrase"]
        answers = dialog["Answer"]
        print(rep(synonyms(phrase)))
        print(answers)


    # Wrong answer, easy question
    @Rule(Pattern(typeQ = 'answer', answer = '0', question_lvl = L('1') | L('2') | L('3')), Rule_exe(executed = False))
    def wrong_easy (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_answer_wrong_easy,"All")
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog
        

    # Wrong answer, hard question
    @Rule(Pattern(typeQ = 'answer', answer = '0', question_lvl = L('4') | L('5')), Rule_exe(executed = False))
    def wrong_hard (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_answer_wrong_hard,"All")
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Right answer, easy question
    @Rule(Pattern(typeQ = 'answer', answer = '1', question_lvl = L('1') | L('2') | L('3')), Rule_exe(executed = False))
    def right_easy (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_answer_right_easy,"All")
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Right answer, hard question
    @Rule(Pattern(typeQ = 'answer', answer = '1', question_lvl = L('4') | L('5')), Rule_exe(executed = False))
    def right_hard (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_answer_right_hard,"All")
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Wrong answer, easy question, good student
    @Rule(Pattern(typeQ = 'answer', answer = '0', question_lvl = L('1') | L('2') | L('3'), student_lvl = L('A') | L('B')), Rule_exe(executed = False), salience=1)
    def wrong_easy_goodSt (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_answer_wrong_easy,"Mock")
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog
    

    def getResult(self):
        return self.__result


    def getUsername(self):
       return self.__username

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
    
    @Rule(Pattern(language='PT'), Rule_exe(executed = False), salience=0)
    def teste4 (self):
        print('Teste 4')
        self.modify(self.facts[1], executed= True)

    @Rule(Pattern(language='PT', domain='BD'), Rule_exe(executed = False), salience=1)
    def teste5 (self):
        print('Teste 5')
        self.modify(self.facts[1], executed= True)
    '''