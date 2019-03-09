import re
from pyknow import *
from pattern_analyser import *
from random import choice


# Pattern Fact
# no need for user
class Pattern(Fact):  

    '''
    Pattern(id_user, language, typeQ, domain, subdomain, question, answer, skill_domain, performance_domain, skill_subdomain, performance_subdomain, time)
    Pattern(domain, subdomain, skill, performance, time, language)
    '''
    pass

# Question Fact
# admite-se que se recebe o tema da pergunta no padrao
class Question(Fact):
    '''
    Question(typeQ)
    '''
    pass

### Rules Engine ###
class RulesEngine(KnowledgeEngine):
    
    ## Declare initial facts
    @DefFacts()
    def dialog_maker(self):
        yield Pattern(domain='Futebol',subdomain='Cenas',skill='Good',performance='Average',time="Good",language='EN')
        #yield Question(typeQ = 'greetingsI')

    ## Declare rules
    @Rule(Question(typeQ='greetingsI'))
    def teste1 (self):
        print('Saudaçao inicial')

    @Rule(OR(   
            Pattern(skill = L('Terrible') | L('Bad')),
            Pattern(performance = L('Terrible') | L('Bad'))
            ))
    def teste2 (self):
        print('Secção Duvidas')

    @Rule(AND(   
            Pattern(skill = L('Terrible') | L('Bad')),
            Pattern(performance = L('Terrible') | L('Bad')),
            Pattern(performance = L('Terrible') | L('Bad'))
            ))
    def teste3 (self):
        print('Secção Duvidas 2')



### PATTERN PARSER ###

# pattern
patt = ['John','PT',3,'BD','Modelos ER','Qual é coisa qual é ela?',1,33,43,53,63,20]
# pattern analyser
p_analys = Pat_Analyser()
# pattern conversion
p_analys.pat_parser(patt)
# print user
print(p_analys.get_user())
# array w/ pattern fields (domain,subdomain,skill,performance,language,user,typeQ)
str_pat = p_analys.pat_string().split(",")
# print array above
print(str_pat)

### MAKE DECISION - by converting pattern into a fact and filtering it with rules previously declared in the program ###
# Init rules engine
watch('RULES', 'FACTS')   
aux = RulesEngine()   
aux.reset() 

# example of declaring fact
aux.declare(Question(typeQ = 'greetingsI'))

# declare facts with pattern recieved
p = Pattern(domain= str_pat[0], subdomain= str_pat[1], skill= str_pat[2], performance= str_pat[3], language= str_pat[4], time=str_pat[6])
q = Question(typeQ = str_pat[5])

aux.declare(p)
aux.declare(q)

# run engine
aux.run()
aux.facts

