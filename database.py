
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri = "mongodb+srv://marabk03:SR2BvU9KQrPD9Pju@discordbot.eihn4ge.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
collection = client.item_prices




collection = client.item_prices
skyblock_prices_database = collection["item"]
welcome_channel = collection["welcome"]
election_channel = collection["election"]
penis_size = collection["penis"]
logging_channel = collection["logging"]
married_log = collection["married"]
messages_log = collection["messages"]
hypixel_api = collection["hypixelapi"]

item_prices = {}
for document in skyblock_prices_database.find():
    for item_name, item_data in document.items():
        if item_name != "_id": 
            price = item_data["buy"]
            item_prices[item_name] = price







