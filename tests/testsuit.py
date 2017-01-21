import sys
# Add the ptdraft folder path to the sys.path list
sys.path.append('../')

import unittest
import dblayer
import dbvalidationlayer



def fun(x):
    return x + 1

''' Test specific to db operations '''

class DBTest(unittest.TestCase):

	def setUp(self):
		print "Setting up"
		self.email = "testuser@email.com"
		self.password = "hashedpass"
		self.username = "testuser1"
		self.userid = dblayer.createuser(self.username,self.email,self.password)
		# print(self.userid)

	def tearDown(self):
		print "Tearing down"

	'''SignUp test: asserts if user already exists with email, username combination'''
	def test_signup(self):				
		self.assertTrue(dbvalidationlayer.signUpValidation(self.username,"ebadaliesadaaa@gmail.com", "somepass")==('failed', None, 'User Name is taken'))
		self.assertTrue(dbvalidationlayer.signUpValidation(self.username,self.email, "somepass")==('failed', None, 'Email Address already exists'))

	'''Login test: tries with invalid email pass then with correct email password
	but with non hashed password'''
	def test_signin(self):				
		self.assertTrue(dbvalidationlayer.signInValidation("eaa@gmail.com", self.password)==('failed', None, 'Email Address Not found'))
		self.assertFalse(dbvalidationlayer.signInValidation(self.email, self.password)==('success', self.userid, None))


''' Tests specific to util functions.'''
class UtilTest(unittest.TestCase):

	def setUp(self):
		print "Setting up Util"


	def tearDown(self):
		print "Tearing down up Util"

	def password_hash_test(self):
		print "password hash test"
		from werkzeug import check_password_hash, generate_password_hash
		hashed = (generate_password_hash("ebad"))
		self.assertTrue(check_password_hash(hashed,"ebad"))

	# TODO: Add Rest of the tests here.



if __name__ == '__main__':
    unittest.main()
