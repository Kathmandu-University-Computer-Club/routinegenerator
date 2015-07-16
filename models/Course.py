from google.appengine.ext import db

class Course(db.Model):
	#key_name set when new course is created example COMP 101
	# course_Id
	course_name = db.StringProperty(required = True)
	class_per_week = db.IntegerProperty(default = 5)
	class_distribution = db.StringProperty(default = "{1:5}")


