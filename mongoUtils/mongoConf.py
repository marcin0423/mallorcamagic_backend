import pymongo
from utils.Logger import log

# we can use separate db uri for dev and prod db here
# unable to connect to the test cluster
client = pymongo.MongoClient(
    'mongodb://mallorca:V!2ZNV^98fm2ZPdD@178.62.216.217:27017,207.154.254.241:27018,207.154.254.241:27019/mallorcadb'
)

# 'mongodb+srv://root:Mallorca%40Magic@cluster0.ltrd4xr.mongodb.net/test')
db = client.get_database()
