import os
import sys

### DATA ###

# SKILLS
skill_dic = {
    1 : 'Terrible',
    2 : 'Bad',
    3 : 'Average',
    4 :'Good',
    5 : 'Excellent'
    }

# PERFORMANCE
perf_dic = {
    1 : 'Terrible',
    2 : 'Bad',
    3 : 'Average',
    4 :'Good',
    5 : 'Excellent'
    }

# QUESTION TYPES
typeQ_dic = {   1: 'greetingsI',
                2: 'greetingsA',
                3: 'doubt',
                4: 'bye',
                5: 'farewell',
                6: 'domain',
                7: 'subdomain',
                8: 'time',
                9: 'answer'
                }

# TIME
# Aqui a ordem não corresponde ao 1 - pior , 5 - melhor
time_dic = {    1 : 'Soon', 
                2 : 'Good',
                3 : 'Good',
                4 : 'Bad',
                5 :'Terrible'
                }


### PATTERN ANALYSER ###

class Patt_Analyser:

    __username= ""
    __language = ""
    __typeQ = ""
    __domain = ""
    __subdomain = ""
    __question = ""
    __answer = ""
    __question_lvl = ""
    __student_lvl = ""
    __state = ""
    __skill_domain = ""
    __performance_domain = ""
    __skill_subdomain = ""
    __performance_subdomain = ""
    __time = ""



    def __init__(self):
        self.__username= ""
        self.__language = ""
        self.__typeQ = ""
        self.__domain = ""
        self.__subdomain = ""
        self.__question = ""
        self.__answer = ""
        self.__question_lvl = ""
        self.__student_lvl = ""
        self.__state = ""
        self.__skill_domain = ""
        self.__performance_domain = ""
        self.__skill_subdomain = ""
        self.__performance_subdomain = ""
        self.__time = ""

    # patt_parser : converts the recieved pattern into the respective fields (user,domain,subdomain,etc), and sets those parameters into class Pattern Analyser.
    def patt_parser(self, p):
        
        self.__username = p[0]
        self.__language = p[1]
        self.__typeQ = typeQ_dic[p[2]]
        self.__domain = p[3]
        self.__subdomain = p[4]
        self.__question = p[5]
        self.__answer = p[6]
        self.__question_lvl = p[7]
        self.__student_lvl = p[8]
        self.__state = p[9]

        # skill_domain
        for key in skill_dic:
            if p[10] in key:
                self.__skill_domain = skill_dic[key]
                break

        # performance_domain
        for key in perf_dic:
            if p[11] in key:
                self.__performance_domain = perf_dic[key]
                break

        # skill_subdomain
        for key in skill_dic:
            if p[12] in key:
                self.__skill_subdomain = skill_dic[key]
                break

        # performance_subdomain
        for key in perf_dic:
            if p[13] in key:
                self.__performance_subdomain = perf_dic[key]
                break

        for key in time_dic:
            if p[14] in key:
                self.__time = time_dic[key]
                break

    # Get the pattern's user
    def getUsername(self):
        return self.__username

    # Displays fields into a string (separated by ','). The string is used to declare a fact, which represents the pattern, in the Rules Engine.
    def patt_string(self):
        return f'{self.__username},{self.__language},{self.__typeQ},{self.__domain},{self.__subdomain},{self.__question},{self.__answer},{self.__question_lvl},{self.__student_lvl},{self.__state},{self.__skill_domain},{self.__performance_domain},{self.__skill_subdomain},{self.__performance_subdomain},{self.__time}'
