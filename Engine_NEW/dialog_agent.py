import random
from rules_engine import *
import json

#JSON pattern reader
def pattern_reader(file):
    input_file = open (file)
    json_array = json.load(input_file)
    # [1, 1, 1, 1, 1, 3, 4, 123443, 4, 4, 3, 4, 3, 'greetingsI']
    patt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    patt[0] = int(json_array['username'])
    patt[1] = int(json_array['language'])
    patt[2] = int(json_array['domain'])
    patt[3] = int(json_array['subdomain'])
    patt[4] = int(json_array['answer'])
    patt[5] = int(json_array['question_lvl'])
    patt[6] = int(json_array['student_lvl'])
    patt[7] = int(json_array['state'])
    patt[8] = int(json_array['skill_domain'])
    patt[9] = int(json_array['performance_domain'])
    patt[10] = int(json_array['skill_domain'])
    patt[11] = int(json_array['performance_subdomain'])
    patt[12] = int(json_array['time'])
    patt[13] = json_array['typeQ']

    return patt

###### Dialog Agent ######

class Dialog_Agent:

    __pattern = []
    __dialog = ""
    __username = ""

    def __init__(self, patt):
        self.__pattern = self.getTypeQ(patt)
        self.__dialog = ""
        self.__username = ""

    def getTypeQ(self,patt):
        if patt[8] == 0:
            typeQ = "greetingsI"
        else:
            typeQ = "greetingsA"

        patt[13]=typeQ
        return patt

    def run(self):
        ### MAKE DECISION - by converting pattern into a fact and filtering it with rules previously declared in the program ###
        # Init rules engine
        print('Initializing engine rules')
        watch('RULES', 'FACTS')   
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

patt = [1, 1, 1, 1, 1, 3, 4, 123443, 0, 0, 0, 0, 0]
patt = [1, 1, 1, 1, 1, 3, 4, 123443, 2, 2, 2, 2, 1]
patt = [1, 1, 1, 1, 1, 3, 4, 123443, 2, 2, 2, 2, 4]
patt = ['John001', 'PT', 2, 'BD', 'Modelos ER', 'Gostas de pêras? Sim. Não.', 0, 2, 'C', 'processoX', 103, 53, 63, 15, 20]
patt = ['John001', 'PT', 8, 'BD', 'Modelos ER', 'Gostas de pêras? Sim. Não.', 0, 5, 'B', 'processoX', 103, 53, 63, 15, 20]
patt = ['John001', 'PT', 8, 'BD', 'Modelos ER', 'Gostas de pêras? Sim. Não.', 0, 1, 'D', 'processoX', 103, 53, 63, 15, 20]
patt = ['John001', 'PT', 8, 'BD', 'Modelos ER', 'Gostas de pêras? Sim. Não.', 1, 5, 'B', 'processoX', 103, 53, 63, 15, 20]
patt = ['John001', 'PT', 8, 'BD', 'Modelos ER', 'Gostas de pêras? Sim. Não.', 1, 1, 'D', 'processoX', 103, 53, 63, 15, 20]


patt = ['John001', 'PT', 2, 'BD', 'Modelos ER', 'Gostas de pêras? Sim. Não.', 0, 2, 'C', 'processoX', 103, 53, 63, 15, 20]

'''
# pattern
patt = pattern_reader("pattern_example.json")

# dialog agent
agent = Dialog_Agent(patt)
agent.run()
dialog = agent.getDialog()
if dialog:
    pprint(dialog)
else:
    print("No dialog found")
