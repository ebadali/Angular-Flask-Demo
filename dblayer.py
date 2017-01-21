# insert user into document.
from pymongo import MongoClient
from bson.objectid import ObjectId


''' Creates Connection with the Mongo server.
	handles db calls made from wrappers.
'''

mongo = MongoClient('localhost', 27017)

dedb = mongo.girtdb

deusers = dedb.users

def createuser(username, email,hashedpassword):
	# 
	user = {
    	'username': username,
    	'email': email,
    	'password': hashedpassword
	}
	result = dedb.users.insert(user)

	print(result)
	return result

def getuser(userid):
	
	result = deusers.find_one({"_id": ObjectId(userid)})
	# if result == None: might retur None
	return result
	

def getusers():
	result = []
	cursor = deusers.find()
	for document in cursor:
		result.append({'Username': document["username"], "Email" : document["email"]})
	return result

def getuserwithusername(username):
	return deusers.find_one({"username": username})
	
def getuserwithemail(email):
	return deusers.find_one({"email": email})

def getuserwithemailpassword(email,password):

	return deusers.find_one({"email": email, 'password':password})



# getusers()
# print(createuser("asd","asdasd","asdads"))