from google.appengine.ext import db

class Faculty(db.Model):
	#CE, CS
	#key_name set as CE, CS...
	faculty_name = db.StringProperty(required = True) #Computer Engineering
	department = db.IntegerProperty(required = True) #reference to department (id)



