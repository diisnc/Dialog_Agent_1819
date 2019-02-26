import os
import random
import sys
'''
- O padrao é atualizado ao longo do tempo? se sim, no 
padrao vem o tema (saudaçao, etc) da pergunta?

- Podemos usar o nome, posteriormente, nas frases do dialogo

'''


users_dic = {   1: 'Gil',
                2: 'Diana',
                3: 'Luis',
                4: 'Raul',
                5: 'Kiko' 
            }

domain_dic = {  1: 'BD',
                2: 'BIO',
                3: 'FIS',
                4: 'INF',
                5: 'ENF'
            }

subdomain_dic = {   'BD': ['a','b','c'],
                    'BIO': ['d','e','f'],
                    'FIS': ['g','h','i'],
                    'INF': ['j','k','l'],
                    'ENF': ['m','n','o']
                }

skill_dic = {
    range(0,21) : 'Terrible',
    range(20,41) : 'Bad',
    range(40, 61) : 'Average',
    range(60, 81) :'Good',
    range(80, 100) : 'Excellent'
    }

perf_dic = {
    range(0,21) : 'Terrible',
    range(20,41) : 'Bad',
    range(40,61) : 'Average',
    range(60, 81) :'Good',
    range(80, 100) : 'Excellent'
    }

language_dic = {    1: 'PT',
                    2: 'EN',
                    3: 'ES',
                    4: 'DE',
                    5: 'FR',
                    6: 'RU'
                }

typeQ_dic = {   1: 'greetingsI',
                2: 'greetingsA',
                3: 'domain',
                4: 'subdomain',
                5: 'doubt',
                6: 'bye',
                7: 'timeout'
                }



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

    def pat_parser(self, p):
        
        for x in range(0, 7):
            if x == 0:
                self.__user = users_dic[p[x]]
            
            elif x == 1:
               self.__domain = domain_dic[p[x]]
            
            elif x == 2:
                self.__subdomain = subdomain_dic[self.__domain][p[x]]
            
            elif x == 3:
                for key in skill_dic:
                    if p[x] in key:
                       self.__skill = skill_dic[key]
            
            elif x == 4:
                for key in perf_dic:
                    if p[x] in key:
                       self.__performance = perf_dic[key]
            
            elif x == 5:
                self.__language = language_dic[p[x]]
            
            elif x == 6:
                self.__typeQ = typeQ_dic[p[x]]

    def get_user(self):
        return self.__user

    def string_pat(self):
        return '{},{},{},{},{},{},{}'.format(self.__domain,self.__subdomain,self.__skill,self.__performance,self.__language,self.__typeQ,self.__user)

######### MAIN
'''
patt = [4,3,2,85,57,3,1]

p_analys = Pat_Analyser()

p_analys.pat_parser(patt)

print(p_analys.get_user())

print(p_analys.string_pat())

print(p_analys.string_pat().split(","))
'''
