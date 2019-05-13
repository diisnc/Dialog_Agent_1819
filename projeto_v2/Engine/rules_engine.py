# PyKnow Rules Engine
from pyknow import *
from pprint import pprint
# Collector Module
from collector import *
from auxiliary import *

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
    __userID = ""
    __result = {}

    
    def __init__(self,userID,username):
        self.__username = username
        self.__userID = userID
        self.__result = {   "Phrase" : "",
                            "Answer" : ""}
        super().__init__()


    ## Declare initial facts
    @DefFacts()
    def dialog_maker(self):
        yield Rule_exe(executed = False)
    
    
    ## Declare rules
    # Greeting for the first time
    @Rule(Pattern(typeQ = 'greetingsI'), Rule_exe(executed = False))
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


    # Greeting again, lastLogin = from 5 minutes to 1 hour later
    @Rule(Pattern(typeQ = 'greetingsTSoon'), Rule_exe(executed = False))
    def greetingsTSoon (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_greetingsTSoon,["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog

    # Greeting again, lastLogin = from one week later 
    @Rule(Pattern(typeQ = 'greetingsTLate'), Rule_exe(executed = False))
    def greetingsTLate (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_greetingsTLate,["All"])
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
        #last login
        userH = col_userHist.find_one({"userID": self.__userID})
        col_userHist.update_one({'userID': self.__userID}, {'$push': {'endChatTime': datetime.now()}})

    # Farewell badP
    @Rule(Pattern(typeQ = 'farewell', student_lvl = L('2') | L('1')), Rule_exe(executed = False), salience = 1)
    def f_badP (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_farewell_badP,["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog
        #last login
        col_userHist.update_one({'userID': self.__userID}, {'$push': {'endChatTime': datetime.now()}})

     # Farewell avgP
    @Rule(Pattern(typeQ = 'farewell', student_lvl = '3'), Rule_exe(executed = False), salience = 1)
    def f_avgP (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_farewell_avgP,["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog
        #last login
        col_userHist.update_one({'userID': self.__userID}, {'$push': {'endChatTime': datetime.now()}})

   
    # Farewell goodP
    @Rule(Pattern(typeQ = 'farewell', student_lvl = L('5') | L('4')), Rule_exe(executed = False), salience = 1)
    def f_goodP (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_farewell_goodP,["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog
        #last login
        col_userHist.update_one({'userID': self.__userID}, {'$push': {'endChatTime': datetime.now()}})


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

    # Time - timeout
    @Rule(Pattern(typeQ = 'time', time = L('4') | L('5')), Rule_exe(executed = False))
    def timeout (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_time_out,["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog

    
    # Time - timeout - terrible time - BadP
    @Rule(Pattern(typeQ = 'time', time = '5', skill_subdomain=L('2') | L('1')), Rule_exe(executed = False), salience = 1)
    def timeout_terrible_badP (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_time_out['badP'],["Serious","Mock"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog

    
    # Time - timeout - bad time - BadP
    @Rule(Pattern(typeQ = 'time', time = '4', skill_subdomain=L('2') | L('1')), Rule_exe(executed = False), salience = 1)
    def timeout_bad_badP (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_time_out['badP'],["Normal","Funny"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Time - timeout - terrible time - AvgP
    @Rule(Pattern(typeQ = 'time', time = '5', skill_subdomain='3'), Rule_exe(executed = False), salience = 1)
    def timeout_terrible_avgP (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_time_out['avgP'],["Serious","Mock"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog

    
    # Time - timeout - bad time - AvgP
    @Rule(Pattern(typeQ = 'time', time = '4', skill_subdomain='3'), Rule_exe(executed = False), salience = 1)
    def timeout_bad_avgP (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_time_out['avgP'],["Normal","Funny"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Time - timeout - GoodP
    @Rule(Pattern(typeQ = 'time', time = L('4') | L('5'), skill_subdomain=L('4') | L('5')), Rule_exe(executed = False), salience = 1)
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
    @Rule(Pattern(typeQ = 'time', time = '1'), Rule_exe(executed = False))
    def toosoon (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_time_soon,["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Time - too soon - terrible - badP
    @Rule(Pattern(typeQ = 'time', time = '1', skill_subdomain='1'), Rule_exe(executed = False), salience = 1)
    def toosoon_terrible (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_time_soon['badP'],["Serious","Mock"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog

    
    # Time - too soon - bad - badP
    @Rule(Pattern(typeQ = 'time', time = '1', skill_subdomain='2'), Rule_exe(executed = False), salience = 1)
    def toosoon_bad (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_time_soon['badP'],["Normal","Funny"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog


    # Time - too soon - goodP
    @Rule(Pattern(typeQ = 'time', time = '1', skill_subdomain="3"), Rule_exe(executed = False), salience = 1)
    def toosoon_avg (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_time_soon['avgP'],["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog
    

    # Time - too soon - goodP
    @Rule(Pattern(typeQ = 'time', time = '1', skill_subdomain=L('4') | L('5')), Rule_exe(executed = False), salience = 1)
    def toosoon_good (self):
        self.modify(self.facts[1], executed= True)
        dialog = choose_dialog(list_time_soon['goodP'],["All"])
        dialog["Phrase"] = rep(synonyms(dialog["Phrase"]),self.__username)
        self.__result = dialog



    # wrong answer, easy question:
    #   - student level = A(1), B(2) -> Mock, Serious
    #   - student level = C(3) -> Incentive
    #   - student level = D(4), E(5) -> Normal, Funny

    # wrong answer, hard question:
    #   - student level = A(1), B(2) -> Normal, Funny
    #   - student level = C(3) -> Incentive
    #   - student level = D(4), E(5) -> Serious, Mock

    # right answer, easy question:
    #   - student level = A(1), B(2) -> Mock, Normal
    #   - student level = C(3) -> Funny, Serious
    #   - student level = D(4), E(5) -> Incentive

    # right answer, hard question:
    #   - student level = A(1), B(2) -> Serious, Funny
    #   - student level = C(3) -> Incentive, Serious, Mock
    #   - student level = D(4), E(5) -> Incentive, Normal


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

    def getUserID(self):
       return self.__userID

    def getUsername(self):
       return self.__username