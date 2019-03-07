'''
- Correr mongod
- Correr este file
- Seguem-se algumas queries de consulta a usar no engine:

    funções úteis:  - db.collection.findOne(query, projection)
                    - (...)

'''

import pymongo
# pprint library is used to make the output look more pretty
from pprint import pprint

# Connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["lei"]
mycol = mydb["dialogs"]

x = mycol.find_one()

y = mycol.find_one(
    { },
    { "greetingsI": 1 }
)

pprint(x) 
pprint(y)
