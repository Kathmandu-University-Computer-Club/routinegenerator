from controllers.base_handler import *
from google.appengine.ext import db
from models.Teacher import Teacher

class TeacherHandler(BaseHandler):
	def get(self):
		teacher = db.GqlQuery("Select * from Teacher")
		departments = db.GqlQuery("Select * from Department")
		# class_courses = db.GqlQuery("Select * from ClassCourse")
		self.render("teacher.html",{'teacher':teacher, 'departments': departments, 
			# 'class_courses': class_courses
		})

	def post(self):
		teacher_name = self.request.get('teacher_name')
		department = int(self.request.get('department'))
		teaching_time = self.request.get('teaching_time')
		# class_courses = self.request.get('class_courses')

		teacher = Teacher(
			teacher_name = teacher_name,
			department = department,
			teaching_time = teaching_time,
			# class_courses = class_courses
			)

		teacher.put()
		self.response.write("Sucessfully")



	# 	teacher_name = db.StringProperty(required = True) 
	# department = db.ReferenceProperty(required = True)
	# teaching_time = db.StringProperty(default = "{}")
	# class_courses = db.StringProperty(int)
