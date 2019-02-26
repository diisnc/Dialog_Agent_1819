<<<<<<< HEAD
import re

from pyknow import *

#nao e preciso user
class Pattern(Fact):  

    '''
    Pattern(domain, subdomain, skill, performance, language)
    '''
    pass

# admite-se que se recebe o tema da pergunta no padrao
class Question(Fact):

    '''
    Question(theme)
    '''
    pass

class RulesEngine(KnowledgeEngine):
    @DefFacts()
    def dialog_maker(self):
        yield Pattern(domain='Futebol',subdomain='Cenas',skill='Good',performance='Average',language='EN')
        #yield Question(theme = 'greetingsI')

    @Rule(Question(theme='greetingsI'))
    def teste (self):
        print('Saudaçao inicial')


# MAIN
watch('RULES', 'FACTS')   
aux = RulesEngine()   
aux.reset() 
aux.declare(Question(theme = 'greetingsI'))
aux.run()
aux.facts
