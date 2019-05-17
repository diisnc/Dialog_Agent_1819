from rules_engine import *
from auxiliary import *


###### Dialog Agent ######

class Dialog_Agent:

    __pattern = []
    __dialog = ""
    __userID = ""
    __username = ""

    def __init__(self, patt):
        self.__dialog = ""
        self.__userID = patt[0]
        self.__username = "Joe" # TODO : get username with user ID
        # if typeQ patt[13] is empty
        if not patt[13] :
            patt[13] = self.getGreetings(patt)
        self.__pattern = patt

        
    def getGreetings(self,patt):
        # New User
        if patt[8] == '0': # if skill is 0, then it's the FIRST TIME
            typeQ = "greetingsI"
            # New user history entry
            print(" ########## New user history entry ########## ")
            userH = {
                    "userID" : self.__userID,
                    "beginChatTime" : [datetime.now()],
                    "endChatTime" : [] 
                    }

            col_userHist.insert_one(userH) 

        # User exists
        else:
            print(" ########## User history exists ########## ")
            typeQ = "greetingsA"

            # begin chattime
            col_userHist.update_one({'userID': self.__userID}, {'$push': {'beginChatTime': datetime.now()}})
            
            # user history
            userH = col_userHist.find_one({"userID": self.__userID})

            # checking last chatted time
            lastChatTime = userH["endChatTime"][-1]
            # typeQ = greetingsT if last ChatTime (diff) between 5 minutes and 1 hour (60 minutes) later,
            # or 1 (7 days = 7 * 24 * 60 min = 10.080) week later
            diff = (datetime.now() - lastChatTime).total_seconds()
            diff = diff / 60 # seconds to minutes
            if (diff>=5 and diff <= 60):
                typeQ = "greetingsTSoon"
            elif(diff >= 10080):
                typeQ = "greetingsTLate"

        return typeQ

    def run(self):
        ### MAKE DECISION - by converting pattern into a fact and filtering it with rules previously declared in the program ###
        # Init rules engine
        # print('Initializing engine rules')
        # watch('RULES', 'FACTS')   
        aux = RulesEngine(self.__userID,self.__username)   
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
        
    def getUserID(self):
        return self.__userID

    def getUsername(self):
        return self.__username



#################################### MAIN ####################################

'''
Patterns for testing
'''

patt1 = ["1", "1", "", "", "", "", "4", "123456", "0", "0", "0", "0", "0", ""]
patt2 = ["1", "1", "1", "1", "1", "3", "4", "123456", "4", "4", "3", "4", "3", "doubt"]
patt3 = ["1", "1", "1", "1", "1", "3", "4", "123456", "4", "4", "3", "4", "3", "bye"]
patt4 = ["1", "1", "1", "1", "1", "3", "4", "123456", "4", "4", "3", "4", "3", ""]
patt5 = ["1", "1", "1", "1", "1", "3", "4", "123456", "4", "4", "3", "4", "3", "domain"]
patt6 = ["1", "1", "1", "1", "1", "3", "4", "123456", "4", "4", "3", "4", "3", "subdomain"]
patt7 = ["1", "1", "1", "1", "0", "3", "4", "123456", "4", "3", "3", "4", "3", "answer"]
patt8 = ["1", "1", "1", "1", "1", "3", "4", "123456", "4", "4", "3", "4", "3", "answer"]
patt9 = ["1", "1", "1", "1", "1", "3", "4", "123456", "4", "4", "3", "4", "3", "farewell"]

# pattern
#patt = pattern_reader("pattern_example.json")

patt = [patt1,patt2,patt3,patt4,patt5,patt6,patt7,patt8,patt9]
i = 0
# dialog agent
for p in patt:
    i += 1
    agent = Dialog_Agent(p)
    agent.run()
    dialog = agent.getDialog()
    if dialog:
        print("#### Patt "+ str(i) + " ####")
        print("Phrase = " + str(dialog["Phrase"]))
        print("Answer = " + str(dialog["Answer"]))
    else:
        print("No dialog found")
