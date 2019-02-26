import re

from pyknow import *

class Pattern(Fact):  

    '''
    Pattern(user, domain, subdomain, skill, performance, language)
    '''
    pass

class Question(Fact):

    '''
    Question(tema)
    '''
    pass

class RulesEngine(KnowledgeEngine):
    @DefFacts()
    def dialog_maker(self):
        yield Pattern(user='Raul',domain='Futebol',subdomain='Cenas',skill='Good',performance='Average',language='EN')
    
    @Rule(Pattern(user=))