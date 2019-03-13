import os
import random
import sys


### DATA ###


# SKILLS
skill_dic = {
    range(121,151) : 'Terrible',
    range(91,121) : 'Bad',
    range(61, 91) : 'Average',
    range(31, 61) :'Good',
    range(0, 31) : 'Excellent'
    }

# PERFORMANCE
perf_dic = {
    range(0,21) : 'Terrible',
    range(20,41) : 'Bad',
    range(40,61) : 'Average',
    range(60, 81) :'Good',
    range(80, 100) : 'Excellent'
    }

# QUESTION TYPES
typeQ_dic = {   1: 'greetingsI',
                2: 'greetingsA',
                3: 'domain',
                4: 'subdomain',
                5: 'doubt',
                6: 'farewell',
                7: 'time',
                8: 'answer'
                }

# TIME
time_dic = {    range(0,6) : 'Soon',
                range(6,31) : 'Good',
                range(31,61) : 'Bad',
                range(61, 91) :'Terrible'
                }


### PATTERN ANALYSER ###

class Pat_Analyser:

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

    # pat_parser : converts the recieved pattern into the respective fields (user,domain,subdomain,etc), and sets those parameters into class Pattern Analyser.
    def pat_parser(self, p):
        
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
    def get_user(self):
        return self.__username

    # Displays fields into a string (separated by ','). The string is used to declare a fact, which represents the pattern, in the Rules Engine.
    def pat_string(self):
        return f'{self.__username},{self.__language},{self.__typeQ},{self.__domain},{self.__subdomain},{self.__question},{self.__answer},{self.__question_lvl},{self.__student_lvl},{self.__state},{self.__skill_domain},{self.__performance_domain},{self.__skill_subdomain},{self.__performance_subdomain},{self.__time}'




######### MAIN
'''
# pattern
patt = ['John001', 'PT', 1, 'BD', 'Modelos ER', 'Gostas de pêras? Sim. Não.', 0, 3, 'B', 'processoX', 53, 53, 63, 75, 20]
# class
p_analys = Pat_Analyser()
# pattern conversion
p_analys.pat_parser(patt)
# print username
print(p_analys.get_user())
# print pattern string
print(p_analys.pat_string())
# print array of fields
print(p_analys.pat_string().split(","))
'''
