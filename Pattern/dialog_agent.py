import random
from pattern_analyser import * 
from rules_engine import *


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
        p = Pattern(username = str_pat[0], language = str_pat[1] , typeQ = str_pat[2] , domain = str_pat[3] ,subdomain = str_pat[4] , question = str_pat[5] , answer = str_pat[6] , 
                    question_lvl = str_pat[7] , student_lvl = str_pat[8] , state = str_pat[9] , skill_domain = str_pat[10] , performance_domain = str_pat[11] ,
                    skill_subdomain = str_pat[12] , performance_subdomain = str_pat[13], time = str_pat[14])
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

# pattern
patt = ['John001', 'PT', 8, 'BD', 'Modelos ER', 'Gostas de pêras? Sim. Não.', 0, 2, 'B', 'processoX', 103, 53, 63, 15, 20]

# dialog agent
agent = Dialog_Agent(patt)
agent.run()
dialog = agent.getDialog()
if dialog:
    print(dialog)
else:
    print("No dialog found")
