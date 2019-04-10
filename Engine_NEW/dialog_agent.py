import random
from pattern_analyser import * 
from rules_engine import *
import json

#JSON pattern reader
def pattern_reader(file):
    input_file = open (file)
    json_array = json.load(input_file)
    
    patt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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

    return(patt)

###### Dialog Agent ######

class Dialog_Agent:

    __pattern = []
    __dialog = ""
    __username = ""

    def __init__(self, patt):
        self.__pattern = patt
        self.__dialog = ""
        self.__username = ""

    def run(self):
        # pattern analyser
        p_analys = Patt_Analyser()
        # pattern conversion
        p_analys.patt_parser(self.__pattern)
        # username
        self.__username = p_analys.getUsername()
        # array w/ pattern fields (domain,subdomain,skill,performance,language,user,typeQ)
        str_pat = p_analys.patt_string().split(",")
        # print array above
        # print(str_pat)


        ### MAKE DECISION - by converting pattern into a fact and filtering it with rules previously declared in the program ###
        # Init rules engine
        print('Initializing engine rules')
        watch('RULES', 'FACTS')   
        aux = RulesEngine(self.__username)   
        aux.reset() 

        # declare facts with pattern recieved
        p = Pattern(username = str_pat[0], language = str_pat[1] , typeQ = str_pat[2] , domain = str_pat[3] ,subdomain = str_pat[4] ,
                    question = str_pat[5] , answer = str_pat[6] , question_lvl = str_pat[7] , student_lvl = str_pat[8] , state = str_pat[9] ,
                    skill_domain = str_pat[10] , performance_domain = str_pat[11] ,skill_subdomain = str_pat[12] , 
                    performance_subdomain = str_pat[13], time = str_pat[14])
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
patt = [1, 1, 1, 1, 1, 3, 4, 123443, 4, 4, 3, 4, 3]

# dialog agent
agent = Dialog_Agent(patt)
agent.run()
dialog = agent.getDialog()
if dialog:
    pprint(dialog)
else:
    print("No dialog found")
