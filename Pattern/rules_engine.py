import re
from pyknow import *
from pattern_analyser import *
from random import choice

'''

- Podemos usar o nome, posteriormente, nas frases do dialogo

'''

# Pattern Fact
# no need for user
class Pattern(Fact):  

    '''
    Pattern(username, language, typeQ, domain, subdomain, question, answer, question_lvl, student_lvl, state, skill_domain, performance_domain, skill_subdomain, performance_subdomain, time)
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
            Pattern(skill_domain = L('Terrible') | L('Bad')),
            Pattern(performance_domain = L('Terrible') | L('Bad'))
            ))
    def teste2 (self):
        print('Teste 2')

    @Rule(AND(   
            Pattern(skill_subdomain = L('Terrible') | L('Bad')),
            Pattern(performance_domain = L('Terrible') | L('Bad')),
            Pattern(performance_subdomain = L('Terrible') | L('Bad'))
            ))
    def teste3 (self):
        print('Teste 3')



### PATTERN PARSER ###

# pattern
patt = ['John001', 'PT', 1, 'BD', 'Modelos ER', 'Gostas de pêras? Sim. Não.', 0, 3, 'B', 'processoX', 103, 53, 63, 15, 20]
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
p = Pattern(language= str_pat[1], domain= str_pat[3], subdomain= str_pat[4], skill_domain= str_pat[10], performance_subdomain= str_pat[13], time=str_pat[14])
q = Question(typeQ = str_pat[2])

aux.declare(p)
aux.declare(q)

# run engine
aux.run()
aux.facts

