import random
from datetime import datetime
from rules_engine import *
from dialog_agent import *
import json

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


def getGreetingsI(self):
    return list_greetingsI

def getGreetingsA(self):
    return list_greetingsA

def getDoubt(self):
    return list_doubt

def getFarewellBye(self):
    return list_farewell_bye

def getFarewellBadP(self):
    return list_farewell_badP

def getFarewellGoodP(self):
    return list_farewell_goodP

def getFarewellAvgP(self):
    return list_farewell_avgP

def getDomain(self):
    return list_domain

def getSubdomain(self):
    return list_subdomain

def getTimeout(self):
    return list_time_out

def getTimesoon(self):
    return list_time_soon

def getAnswerRightEasy(self):
    return list_answer_right_easy

def getAnswerRightHard(self):
    return list_answer_right_hard

def getAnswerWrongEasy(self):
    return list_answer_wrong_easy

def getAnswerWrongHard(self):
    return list_answer_wrong_hard