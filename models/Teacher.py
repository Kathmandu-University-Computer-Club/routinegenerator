from google.appengine.ext import db

class Teacher(db.Model):
	teacher_name = db.StringProperty(required = True)
	department = db.IntegerProperty(required = True) #reference to Department (id)
	teaching_time = db.StringProperty(default = "{}") #{'sunday': [1,2,3,5,6], 'tuesday':[7]"}
	# class_courses = db.StringProperty(default='[]') #list of tuple of classcourse and course. both reference
	# [(classcourseid, COMP101), (...,...)]
	#[ce,1,comp101, ce,1,comp102]

	#teacher le padhaune courses haru
	#store as an ID ->
