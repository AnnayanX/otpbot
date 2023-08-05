from pymongo import MongoClient

_client = MongoClient("mongodb+srv://otp261456:jPOZuA9Ol36Qk6OZ@cluster0.gq9kzea.mongodb.net/?retryWrites=true&w=majority")

UsersCol = _client['OtpBot']["Users"]
OthersCol = _client['OtpBot']['Others']
Transactions = _client['OtpBot']['Transactions']
Orders = _client['OtpBot']['Orders']


def add_service(user_id, service, s="1"):
    user = UsersCol.find_one({"_id": user_id})
    if service in user[f"fav{s}"]:
        return "This service already exists in your Favourite Services List."
    else:
        services = user[f"fav{s}"]
        services.append(service)
        UsersCol.update_one({"_id": user_id}, {"$set": {f"fav{s}": services}})
        return "✅ Successfully added to your Favourite Services List."


def rm_service(user_id, service, s="1"):
    user = UsersCol.find_one({"_id": user_id})
    if service in user[f"fav{s}"]:
        services = user[f"fav{s}"]
        services.remove(service)
        UsersCol.update_one({"_id": user_id}, {"$set": {f"fav{s}": services}})
        return "✅ Successfully removed from your Favourite Services List."
    else:
        return "❌ This service does not exists in your Favourite Services List."
