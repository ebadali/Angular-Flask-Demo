import dblayer
from werkzeug import check_password_hash, generate_password_hash

'''
These Methods perform db specific validations and DbWrapper
Not to confuse with parameterized validation.
'''
def signUpValidation(username, email, password):

	error = None
	if dblayer.getuserwithemail(email):
		# User Already exist
		error = "Email Address already exists"
	elif dblayer.getuserwithusername(username):
		# User Already exist
		error = "User Name is taken"

	if error:
		return "failed", None, error

	user = dblayer.createuser(username,email,generate_password_hash(password))
	if user is not None:
		return "success", str(user), None

	return "failed", None, "Internal DB Error"		

def signInValidation(email, password):

	error = None
	user = dblayer.getuserwithemail(email)	    
	if user is None:
	    error = 'Email Address Not found'
	elif not check_password_hash(user['password'],
	                             password):
	    error = 'Invalid password'
	else:
	    return "success", str(user['_id']), error

	return "failed", None, error

