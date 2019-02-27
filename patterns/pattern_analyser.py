import os
import random
import sys

'''
- O padrao é atualizado ao longo do tempo? se sim, no 
padrao vem o tema (saudaçao, etc) da pergunta?

- Podemos usar o nome, posteriormente, nas frases do dialogo

'''

### DATA ###

# USERS
users_dic = {   1: 'Gil',
                2: 'Diana',
                3: 'Luis',
                4: 'Raul',
                5: 'Kiko' 
            }

#DOMAINS
domain_dic = {  1: 'BD',
                2: 'BIO',
                3: 'FIS',
                4: 'INF',
                5: 'ENF'
            }

#SUB-DOMAINS
subdomain_dic = {   'BD': ['a','b','c'],
                    'BIO': ['d','e','f'],
                    'FIS': ['g','h','i'],
                    'INF': ['j','k','l'],
                    'ENF': ['m','n','o']
                }

# SKILLS
skill_dic = {
    range(0,21) : 'Terrible',
    range(20,41) : 'Bad',
    range(40, 61) : 'Average',
    range(60, 81) :'Good',
    range(80, 100) : 'Excellent'
    }

# PERFORMANCE
perf_dic = {
    range(0,21) : 'Terrible',
    range(20,41) : 'Bad',
    range(40,61) : 'Average',
    range(60, 81) :'Good',
    range(80, 100) : 'Excellent'
    }

# LANGUAGES
language_dic = {    1: 'PT',
                    2: 'EN',
                    3: 'ES',
                    4: 'DE',
                    5: 'FR',
                    6: 'RU'
                }

# QUESTION TYPES
typeQ_dic = {   1: 'greetingsI',
                2: 'greetingsA',
                3: 'domain',
                4: 'subdomain',
                5: 'doubt',
                6: 'bye',
                7: 'timeout'
                }


### PATTERN ANALYSER ###

class Pat_Analyser:

    __user= ""
    __domain = ""
    __subdomain = ""
    __skill = ""
    __performance = ""
    __language = ""
    __typeQ = ""

    '''
    def __init__(self, user, domain, subdomain, skill, performance, language, typeQ):
        self.__user= user
        self.__domain_= domain
        self.__subdomain = subdomain
        self.__skill = skill
        self.__performance = performance
        self.__language = language
         __typeQ = typeQ
    '''

    def __init__(self):
        self.__user= ""
        self.__domain_= ""
        self.__subdomain = ""
        self.__skill = ""
        self.__performance = ""
        self.__language = ""
        self.__typeQ = ""

    # pat_parser : converts the recieved pattern into the respective fields (user,domain,subdomain,etc), and sets those parameters into class Pattern Analyser.
    def pat_parser(self, p):
        
        self.__user = users_dic[p[0]]
    
        self.__domain = domain_dic[p[1]]

        self.__subdomain = subdomain_dic[self.__domain][p[2]]

        for key in skill_dic:
            if p[3] in key:
                self.__skill = skill_dic[key]

        for key in perf_dic:
            if p[4] in key:
                self.__performance = perf_dic[key]

        self.__language = language_dic[p[5]]

        self.__typeQ = typeQ_dic[p[6]]

    # Get the pattern's user
    def get_user(self):
        return self.__user

    # Displays fields into a string (separated by ','). The string is used to declare a fact, which represents the pattern, in the Rules Engine.
    def pat_string(self):
        return '{},{},{},{},{},{},{}'.format(self.__domain,self.__subdomain,self.__skill,self.__performance,self.__language,self.__typeQ,self.__user)


######### MAIN
'''
# pattern
patt = [4,3,2,85,57,3,1]
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
