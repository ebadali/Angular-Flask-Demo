
''' Responder suit: Generate Response for apis'''

from flask import jsonify
def getResponce(status,message, sessionvalue):
	response = {}
	if status == "error":
		response = {'status':'error','error':message}
	else:
		response = {'status':'success','sessionkey':sessionvalue, 'message':message}
	return jsonify(response);	

def getFailResponse(reason):
	response = {'status':'failure','error':reason}
	return jsonify(response);	


def getSuccessResponse(sessionvalue, data=None):
	response = {'status':'success','sessionkey':sessionvalue, 'users':data}
	return jsonify(response);