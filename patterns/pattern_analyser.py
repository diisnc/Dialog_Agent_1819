import os
import random
import sys

'''

- Podemos usar o nome, posteriormente, nas frases do dialogo

'''

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

    __user= ""
    __language = ""
    __typeQ = ""
    __domain = ""
    __subdomain = ""
    __question = ""
    __answer = ""
    __skill_domain = ""
    __performance_domain = ""
    __skill_subdomain = ""
    __performance_subdomain = ""
    __time = ""



    def __init__(self):
        self.__user= ""
        self.__language = ""
        self.__typeQ = ""
        self.__domain = ""
        self.__subdomain = ""
        self.__question = ""
        self.__answer = ""
        self.__skill_domain = ""
        self.__performance_domain = ""
        self.__skill_subdomain = ""
        self.__performance_subdomain = ""
        self.__time = ""

    # pat_parser : converts the recieved pattern into the respective fields (user,domain,subdomain,etc), and sets those parameters into class Pattern Analyser.
    def pat_parser(self, p):
        
        self.__user = p[0]
        self.__language = p[1]
        self.__typeQ = p[2]
        self.__domain = p[3]
        self.__subdomain = p[4]
        self.__question = p[5]
        self.__answer = p[6]

        for key in skill_dic:
            if p[7] in key:
                self.__skill_domain = skill_dic[key]
                break

        for key in perf_dic:
            if p[8] in key:
                self.__performance_domain = perf_dic[key]
                break

        for key in skill_dic:
            if p[9] in key:
                self.__skill_subdomain = skill_dic[key]
                break

        for key in perf_dic:
            if p[10] in key:
                self.__performance_subdomain = perf_dic[key]
                break

        for key in time_dic:
            if p[11] in key:
                self.__time = time_dic[key]
                break

    # Get the pattern's user
    def get_user(self):
        return self.__user

    # Displays fields into a string (separated by ','). The string is used to declare a fact, which represents the pattern, in the Rules Engine.
    def pat_string(self):
        return f'{self.__user},{self.__language},{self.__typeQ},{self.__domain},{self.__subdomain},{self.__question},{self.__answer},{self.__skill_domain}, {self.__performance_domain},{self.__skill_subdomain},{self.__performance_subdomain},{self.__time}'




######### MAIN
'''
# pattern
patt = ['John','PT',3,'BD','Modelos ER','Qual é coisa qual é ela?',1,33,43,53,63,20]
# class
p_analys = Pat_Analyser()
# pattern conversion
p_analys.pat_parser(patt)
# print user
print(p_analys.get_user())
# print pattern string
print(p_analys.pat_string())
# print array of fields
print(p_analys.pat_string().split(","))
'''
