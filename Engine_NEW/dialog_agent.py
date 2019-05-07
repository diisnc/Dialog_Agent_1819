import random
from datetime import datetime
from rules_engine import *
import json

#JSON pattern reader
def pattern_reader(file):
    input_file = open (file)
    json_array = json.load(input_file)
    # [1, 1, 1, 1, 1, 3, 4, 123443, 4, 4, 3, 4, 3, 'greetingsI',"last ChatTime"]
    patt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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
    patt[14] = json_array['lastChatTime']

    return patt

###### Dialog Agent ######

class Dialog_Agent:

    __pattern = []
    __dialog = ""
    __username = ""
    __lastChatTime = ""

    def __init__(self, patt):
        self.__dialog = ""
        self.__username = patt[0]
        self.__lastChatTime = patt[14]
        self.__pattern = patt # self.getTypeQ(patt)
        

    def getTypeQ(self,patt):
        if patt[8] == 0:
            typeQ = "greetingsI"
        else:
            typeQ = "greetingsA"

        
        diff = (datetime.now() - datetime.strptime(self.__lastChatTime,'%Y-%m-%d %H:%M:%S.%f')).total_seconds()
        diff = diff / 60 # seconds to minutes
        # typeQ = greetingsT if last ChatTime (diff) between 5 minutes and 1 hour (60 minutes) later, or 1 (7 days = 7 * 24 * 60 min = 10.080) week later
        if (diff>=5 and diff <= 60):
            typeQ = "greetingsTSoon"
        elif(diff >= 10080):
            typeQ = "greetingsTLate"

        patt[13]=typeQ

        return patt

    def run(self):
        ### MAKE DECISION - by converting pattern into a fact and filtering it with rules previously declared in the program ###
        # Init rules engine
        print('Initializing engine rules')
        #watch('RULES', 'FACTS')   
        aux = RulesEngine(self.__username)   
        aux.reset() 


        # declare facts with pattern recieved
        p = Pattern(username = self.__pattern[0], language = self.__pattern[1], domain = self.__pattern[2] ,subdomain = self.__pattern[3],
                    answer = self.__pattern[4], question_lvl = self.__pattern[5], student_lvl = self.__pattern[6], state = self.__pattern[7],
                    skill_domain = self.__pattern[8], performance_domain = self.__pattern[9], skill_subdomain = self.__pattern[10], 
                    performance_subdomain = self.__pattern[11], time = self.__pattern[12], typeQ = self.__pattern[13])
        aux.declare(p)


        # run engine
        aux.run()
        aux.facts
        self.__dialog = aux.getResult()
        

    def getDialog(self):
        return self.__dialog
        
    def getUsername(self):
        return self.__username



#################################### MAIN ####################################

### PATTERN PARSER ###

'''
Patterns for testing
'''

patt1 = ["1", "1", "1", "1", "1", "3", "4", "123456", "0", "0", "0", "0", "0", "greetingsI", "2019-04-10 22:49:29.786997"]
patt2 = ["1", "1", "1", "1", "1", "3", "4", "123456", "4", "4", "3", "4", "3", "doubt", "2019-04-10 22:49:29.786997"]
patt3 = ["1", "1", "1", "1", "1", "3", "4", "123456", "4", "4", "3", "4", "3", "domain", "2019-04-10 22:49:29.786997"]
patt4 = ["1", "1", "1", "1", "1", "3", "4", "123456", "4", "4", "3", "4", "3", "subdomain", "2019-04-10 22:49:29.786997"]
patt5 = ["1", "1", "1", "1", "0", "3", "4", "123456", "4", "3", "3", "4", "3", "answer", "2019-04-10 22:49:29.786997"]
patt6 = ["1", "1", "1", "1", "1", "3", "4", "123456", "4", "4", "3", "4", "3", "answer", "2019-04-10 22:49:29.786997"]
patt7 = ["1", "1", "1", "1", "1", "3", "4", "123456", "4", "4", "3", "4", "3", "farewell", "2019-04-10 22:49:29.786997"]

# pattern
#patt = pattern_reader("pattern_example.json")

patt = [patt1,patt2,patt3,patt4,patt5,patt6,patt7]

# dialog agent
for i in patt:
    agent = Dialog_Agent(i)
    agent.run()
    dialog = agent.getDialog()
    if dialog:
        pprint(dialog["Phrase"])
    else:
        print("No dialog found")
