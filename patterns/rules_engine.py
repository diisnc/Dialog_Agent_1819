import re
from pyknow import *
from pattern_analyser import *
from random import choice


# no need for user
class Pattern(Fact):  

    '''
    Pattern(domain, subdomain, skill, performance, language)
    '''
    pass

# admite-se que se recebe o tema da pergunta no padrao
class Question(Fact):
    '''
    Question(typeQ)
    '''
    pass

class RulesEngine(KnowledgeEngine):
    @DefFacts()
    def dialog_maker(self):
        yield Pattern(domain='Futebol',subdomain='Cenas',skill='Good',performance='Average',language='EN')
        #yield Question(typeQ = 'greetingsI')

    @Rule(Question(typeQ='greetingsI'))
    def teste1 (self):
        print('Saudaçao inicial')

    @Rule(OR(   
            Pattern(skill = L('Terrible') | L('Bad')),
            Pattern(performance = L('Terrible') | L('Bad'))
            ))
    def teste2 (self):
        print('Secção Duvidas')

# PATTERN PARSER

# pattern
patt = [4,3,2,15,57,3,1]

# pattern analyser
p_analys = Pat_Analyser()

p_analys.pat_parser(patt)

# print user
print(p_analys.get_user())

# array w/ pattern fields (domain,subdomain,skill,performance,language,user,typeQ)
str_pat = p_analys.string_pat().split(",")
# print it
print(str_pat)


# MAIN
watch('RULES', 'FACTS')   
aux = RulesEngine()   
aux.reset() 

# example of declaring fact
aux.declare(Question(typeQ = 'greetingsI'))

# declare facts with pattern recieved
p = Pattern(domain= str_pat[0], subdomain= str_pat[1], skill= str_pat[2], performance= str_pat[3], language= str_pat[4])
q = Question(typeQ = str_pat[5])

aux.declare(p)
aux.declare(q)

# run engine
aux.run()
aux.facts

