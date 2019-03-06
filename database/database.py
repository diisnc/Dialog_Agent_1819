'''
Requisitos para isto funcionar: Mongod e pymongo instalado
'''
import json
import pymongo  # pip install pymongo
from bson import json_util 
from pymongo import MongoClient # Comes with pymongo

conn = pymongo.Connection('mongodb://user:user123@localhost27017.mongolab.com:33499/enron')
client = MongoClient('localhost', 27017)
db = client.lei
collection.find_one({},{"goodPerformance": 1}) 



