from flask import Flask, send_file
from flask import request,jsonify
from flask import session

from flask_cors import CORS
import responder
from hashlib import md5
from datetime import datetime
import dblayer
import dbvalidationlayer

app = Flask(__name__)
CORS(app)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route("/")
def index():
    return send_file("templates/index.html")


@app.route('/signin',methods=['POST'])
def signin():
	content = request.json
	
	# If user is already logged in, just return session key.
	# Not depending on the Browsers cookies.

	sessionValue = content.get('sessionkey') 
	if sessionValue in session:
		# User never logout, might have lost the cookie,
		# send hime the new one.
		return responder.getSuccessResponse(sessionValue)		    	


	email = content.get('email')
	password = content.get('password')	

	error = "credentials required"
	if email and password:
		status, userId, error = dbvalidationlayer.signInValidation(email,password)
		if status == "success":
		    session['sessionkey'] = userId
		    return responder.getSuccessResponse(userId)

	return responder.getFailResponse(error)

@app.route('/signup',methods=['POST'])
def signup():
	content = request.json
	username=content.get('username')
	email=content.get('email')
	password=content.get('password')
	

	#TODO: Perform Sanity Check
	# using validation layer.
	error = "Invalid Credentials"
	if username and email and password:	
		status, userId, error = dbvalidationlayer.signUpValidation(username,email,password)
		if status == "success":
			session['sessionkey'] = userId
			return responder.getSuccessResponse(userId)

	return responder.getFailResponse(error)	

@app.route('/signout',methods=['POST'])
def signout():
	content = request.json
	clientSession = content.get('sessionkey') 
	if clientSession and "sessionkey" in session and clientSession == session["sessionkey"]:	
		# remove Session
		session.pop('sessionkey', None)
		return responder.getSuccessResponse(clientSession)

	return responder.getFailResponse("Session Doesn't exist")	

'''
Returns Dummy Data, Perform no Validation whatsoever
'''
@app.route('/getviewtable',methods=['GET'])
def getviewtable():
	data = [
            { 'Route': '4d', 'Description': 'Glendon St' , 'AM': '9.00', 'PM':'10.15'},
            { 'Route': '5a', 'Description': 'Rialto to Blackrock' , 'AM': '12.00', 'PM':'10.15'},
            { 'Route': '1b', 'Description': 'From Merrion Sq. to Lucan (Dodsboro)' , 'AM': '7.00', 'PM':'3.30'},
            { 'Route': '2d', 'Description': 'From Merrion Sq. Towards Adamstown Rail Station' , 'AM': '9.00', 'PM':'1.15'},
            { 'Route': '3a', 'Description': 'From UCD Belfield To Lucan' , 'AM': '11.00', 'PM':'9.15'},                        
            { 'Route': '4c', 'Description': 'Swords to Portrane' , 'AM': '8.15', 'PM':'10.15'},

    ];
	return jsonify(data)	

'''
Returns Dummy Data, Perform no Validation whatsoever
'''
@app.route('/getdummydata',methods=['GET'])
def getdummydata():
	data = [
			{ 'Route': '4d', 'Description': 'Glendon St'},
            { 'Route': '2a', 'Description': 'Rialto to Blackrock'},
            { 'Route': '4b', 'Description': 'From Merrion Sq. to Lucan (Dodsboro)'},
            { 'Route': '1a', 'Description': 'From Merrion Sq. Towards Adamstown Rail Station' },
            { 'Route': '3c', 'Description': 'From UCD Belfield To Lucan' },                        
            { 'Route': '3c', 'Description': 'Swords to Portrane' },  
    ];
	return jsonify(data)	

''' Fetch all users from db. alive session is required '''
@app.route('/getallusers',methods=['POST'])
def getallusers():


	content = request.json
	clientSession = content.get('sessionkey')
	if "sessionkey" in session and clientSession == session["sessionkey"]:

		data = dblayer.getusers()
		return responder.getSuccessResponse(clientSession, data)
	return responder.getFailResponse("Login Require")	


	
if __name__ == "__main__":
    app.run(host='0.0.0.0')