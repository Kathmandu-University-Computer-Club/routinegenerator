from google.appengine.ext import db

class ClassCourse(db.Model):
	faculty = db.StringProperty(required = True) # ce cs Reference to Faculty (key)
	year = db.IntegerProperty(default = 1) #year 1-4
	semester = db.IntegerProperty(default = 1) #year 1,2
	course = db.StringProperty(str) # [{"COMP101":teacherid}, {...: ...}...] reference to course(key) and teacher(id)
	# ['comp 101','comp 102'] reference to Course (key)
	
