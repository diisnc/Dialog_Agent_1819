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
list_time_out = bd_dialog["time"]["timeout"]
# too_soon
list_time_soon = bd_dialog["time"]["toosoon"]
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
def choose_dialog(list_typeQ, typesP):
        chosen_dialogs = []
        list_typeP = []
        
        # If type == "All" then choose random type
        if typesP[0] == "All":
            type = random.choice(list(list_typeQ.keys()))
        else:
            type = random.choice(typesP)


        list_typeP = list_typeQ[type]

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
    Pattern(typeQ, domain, subdomain, answer, question_lvl, student_lvl,
            skill_domain, performance_domain, skill_subdomain, 
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
        self.modify(self.facts[1], executed= True)
        # selects an element from the list, having into account its type
        dialog = choose_dialog(list_greetingsI,["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Greeting again
    @Rule(Pattern(typeQ = 'greetingsA'), Rule_exe(executed = False))
    def greetingsA_geral (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_greetingsA,["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Greeting again, student_lvl = 1 ou student_lvl = 2  [OUTPUT: funny]
    @Rule(Pattern(typeQ = 'greetingsA', student_lvl = L('1') | L('2')), Rule_exe(executed = False), salience=1)
    def greetingsA_BadSt (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_greetingsA,["Funny"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Greeting again, student_lvl = A ou student_lvl = B  [OUTPUT: mock]
    @Rule(Pattern(typeQ = 'greetingsA', student_lvl = L('5') | L('4')), Rule_exe(executed = False), salience=1)
    def greetingsA_goodSt (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_greetingsA,["Mock"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Doubt 
    @Rule(Pattern(typeQ = 'doubt'), Rule_exe(executed = False))
    def doubt (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_doubt,["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Farewell bye
    @Rule(Pattern(typeQ = 'bye'), Rule_exe(executed = False))
    def bye (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_farewell_bye,["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Farewell badP
    @Rule(Pattern(typeQ = 'farewell', student_lvl = L('2') | L('1')), Rule_exe(executed = False), salience = 1)
    def f_badP (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_farewell_badP,["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog

     # Farewell avgP
    @Rule(Pattern(typeQ = 'farewell', student_lvl = '3'), Rule_exe(executed = False), salience = 1)
    def f_avgP (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_farewell_avgP,["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog

   
    # Farewell goodP
    @Rule(Pattern(typeQ = 'farewell', student_lvl = L('5') | L('4')), Rule_exe(executed = False), salience = 1)
    def f_goodP (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_farewell_goodP,["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Domain
    @Rule(Pattern(typeQ = 'domain'), Rule_exe(executed = False))
    def domain (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_domain,["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Subdomain
    @Rule(Pattern(typeQ = 'subdomain'), Rule_exe(executed = False))
    def subdomain (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_subdomain,["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # time = bad | terrible -> timeout
    # time = bad -> Normal | Funny
    # time = terrible -> Serious | Mock
    # skill_subdomain = Bad | Terrible -> BadP
    # skill_subdomain = Avg -> AvgP
    # skill_subdomain = Good | Excellent -> GoodP



    # 1: SOON, 2: GOOD, 3: GOOD, 4: BAD, 5: TERRIBLE
    # Time - timeout
    @Rule(Pattern(typeQ = 'time', time=L('Bad') | L('Terrible')), Rule_exe(executed = False))
    def timeout (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_time_out,["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Time - timeout - terrible time - BadP
    @Rule(Pattern(typeQ = 'time', time='Terrible', skill_subdomain=L('Bad') | L('Terrible')), Rule_exe(executed = False), salience = 1)
    def timeout_terrible_badP (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_time_out['badP'],["Serious","Mock"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog

    # Time - timeout - bad time - BadP
    @Rule(Pattern(typeQ = 'time', time='Bad', skill_subdomain=L('Bad') | L('Terrible')), Rule_exe(executed = False), salience = 1)
    def timeout_bad_badP (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_time_out['badP'],["Normal","Funny"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog

    # Time - timeout - terrible time - AvgP
    @Rule(Pattern(typeQ = 'time', time='Terrible', skill_subdomain='Average'), Rule_exe(executed = False), salience = 1)
    def timeout_terrible_avgP (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_time_out['avgP'],["Serious","Mock"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog

    # Time - timeout - bad time - AvgP
    @Rule(Pattern(typeQ = 'time', time='Bad', skill_subdomain='Average'), Rule_exe(executed = False), salience = 1)
    def timeout_bad_avgP (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_time_out['avgP'],["Normal","Funny"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog

    # Time - timeout - GoodP
    @Rule(Pattern(typeQ = 'time', time=L('Bad') | L('Terrible'), skill_subdomain=L('Good') | L('Excellent')), Rule_exe(executed = False), salience = 1)
    def timeout_goodP (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_time_out['goodP'],["Incentive"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    
    # time = soon -> toosoon
    # skill_subdomain = Bad | Terrible -> BadP
    # skill_subdomain = Avg -> AvgP
    # skill_subdomain = Good | Excellent -> GoodP

    # Time - too soon
    @Rule(Pattern(typeQ = 'time', time=L('Soon')), Rule_exe(executed = False))
    def toosoon (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_time_soon,["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Time - too soon - terrible - badP
    @Rule(Pattern(typeQ = 'time', time=L('Soon'), skill_subdomain='Terrible'), Rule_exe(executed = False), salience = 1)
    def toosoon_terrible (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_time_soon['badP'],["Serious","Mock"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog

    # Time - too soon - bad - badP
    @Rule(Pattern(typeQ = 'time', time=L('Soon'), skill_subdomain='Bad'), Rule_exe(executed = False), salience = 1)
    def toosoon_bad (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_time_soon['badP'],["Normal","Funny"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Time - too soon - goodP
    @Rule(Pattern(typeQ = 'time', time=L('Soon'), skill_subdomain="Average"), Rule_exe(executed = False), salience = 1)
    def toosoon_avg (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_time_soon['avgP'],["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog
    
    # Time - too soon - goodP
    @Rule(Pattern(typeQ = 'time', time=L('Soon'), skill_subdomain=L('Good') | L('Excellent')), Rule_exe(executed = False), salience = 1)
    def toosoon_good (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_time_soon['goodP'],["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog



    # wrong answer, easy question:
    #   - student level = A, B -> Mock, Serious
    #   - student level = C -> Incentive
    #   - student level = D, E -> Normal, Funny

    # wrong answer, hard question:
    #   - student level = A, B -> Normal, Funny
    #   - student level = C -> Incentive
    #   - student level = D, E -> Serious, Mock

    # right answer, easy question:
    #   - student level = A, B -> Mock, Normal
    #   - student level = C -> Funny, Serious
    #   - student level = D, E -> Incentive

    # right answer, hard question:
    #   - student level = A, B -> Serious, Funny
    #   - student level = C -> Incentive, Serious, Mock
    #   - student level = D, E -> Incentive, Normal


    # Answer - Wrong answer, easy question
    @Rule(Pattern(typeQ = 'answer', answer = '0', question_lvl = L('1') | L('2') | L('3')), Rule_exe(executed = False))
    def wrong_easy (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_answer_wrong_easy, ["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog
        

    # Answer - Wrong answer, hard question
    @Rule(Pattern(typeQ = 'answer',  answer = '0', question_lvl = L('4') | L('5')), Rule_exe(executed = False))
    def wrong_hard (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_answer_wrong_hard,["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Answer - Right answer, easy question
    @Rule(Pattern(typeQ = 'answer',  answer = '1', question_lvl = L('1') | L('2') | L('3')), Rule_exe(executed = False))
    def right_easy (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_answer_right_easy,["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Answer - Right answer, hard question
    @Rule(Pattern(typeQ = 'answer',  answer = '1', question_lvl = L('4') | L('5')), Rule_exe(executed = False))
    def right_hard (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_answer_right_hard,["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Answer - Wrong answer, easy question, good student
    @Rule(Pattern(typeQ = 'answer',  answer = '0', question_lvl = L('1') | L('2') | L('3'), student_lvl = L('5') | L('4')), Rule_exe(executed = False), salience=1)
    def wrong_easy_goodSt (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_answer_wrong_easy,["Mock","Serious"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog

    # Answer - Wrong answer, easy question, avg student
    @Rule(Pattern(typeQ = 'answer',  answer = '0', question_lvl = L('1') | L('2') | L('3'), student_lvl = '3'), Rule_exe(executed = False), salience=1)
    def wrong_easy_avgSt (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_answer_wrong_easy,["Incentive"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog

    # Answer - Wrong answer, easy question, bad student
    @Rule(Pattern(typeQ = 'answer',  answer = '0', question_lvl = L('1') | L('2') | L('3'), student_lvl = L('2') | L('1')), Rule_exe(executed = False), salience=1)
    def wrong_easy_badSt (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_answer_wrong_easy,["Normal","Funny"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog

    # Answer - Wrong answer, hard question, good student
    @Rule(Pattern(typeQ = 'answer',  answer = '0', question_lvl = L('4') | L('5'), student_lvl = L('5') | L('4')), Rule_exe(executed = False), salience=1)
    def wrong_hard_goodSt (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_answer_wrong_hard,["Normal","Funny"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog

    # Answer - Wrong answer, hard question, avg student
    @Rule(Pattern(typeQ = 'answer',  answer = '0', question_lvl = L('4') | L('5'), student_lvl = '3'), Rule_exe(executed = False), salience=1)
    def wrong_hard_avgSt (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_answer_wrong_hard,["Incentive"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog

    # Answer - Wrong answer, hard question, bad student
    @Rule(Pattern(typeQ = 'answer',  answer = '0', question_lvl = L('4') | L('5'), student_lvl = L('2') | L('1')), Rule_exe(executed = False), salience=1)
    def wrong_hard_badSt (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_answer_wrong_hard,["Serious","Mock"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog

    # Answer - right answer, easy question, good student
    @Rule(Pattern(typeQ = 'answer',  answer = '1', question_lvl = L('1') | L('2') | L('3'), student_lvl = L('5') | L('4')), Rule_exe(executed = False), salience=1)
    def right_easy_goodSt (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_answer_right_easy,["Mock","Normal"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog

    # Answer - right answer, easy question, avg student
    @Rule(Pattern(typeQ = 'answer',  answer = '1', question_lvl = L('1') | L('2') | L('3'), student_lvl = '3'), Rule_exe(executed = False), salience=1)
    def right_easy_avgSt (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_answer_right_easy,["Funny","Serious"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog

    # Answer - right answer, easy question, bad student
    @Rule(Pattern(typeQ = 'answer',  answer = '1', question_lvl = L('1') | L('2') | L('3'), student_lvl = L('2') | L('1')), Rule_exe(executed = False), salience=1)
    def right_easy_badSt (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_answer_right_easy,["Incentive"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Answer - right answer, hard question, bad student
    @Rule(Pattern(typeQ = 'answer',  answer = '1', question_lvl = L('4') | L('5'), student_lvl = L('5') | L('4')), Rule_exe(executed = False), salience=1)
    def right_hard_goodSt (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_answer_right_hard,["Serious","Funny"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog
    
    # Answer - right answer, hard question, avg student
    @Rule(Pattern(typeQ = 'answer',  answer = '1', question_lvl = L('4') | L('5'), student_lvl = '3'), Rule_exe(executed = False), salience=1)
    def right_hard_avgSt (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_answer_right_hard,["Incentive","Serious","Mock"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Answer - right answer, hard question, bad student
    @Rule(Pattern(typeQ = 'answer',  answer = '1', question_lvl = L('4') | L('5'), student_lvl = L('2') | L('1')), Rule_exe(executed = False), salience=1)
    def right_hard_badSt (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_answer_right_hard,["Incentive","Normal"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    def getResult(self):
        return self.__result


    def getUsername(self):
       return self.__username