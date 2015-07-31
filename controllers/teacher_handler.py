from controllers.base_handler import *
from google.appengine.ext import db
from models.Teacher import Teacher
from models.Department import Department


class TeacherHandler(BaseHandler):
	def get(self):
		teachers = db.GqlQuery("Select * from Teacher")
		departments = db.GqlQuery("Select * from Department")
		# class_courses = db.GqlQuery("Select * from ClassCourse")

		r = []
		for teacher in teachers:
			r.append({
				'id': teacher.key().id(),
				'teacher_name': teacher.teacher_name,
				'department_id': teacher.department,
				'department_name': Department.get_by_id(teacher.department).department_name,
				'teaching_time': teacher.teaching_time
			})
		self.render("teacher.html",{'teachers':r, 'departments': departments, 
			# 'class_courses': class_courses
		})

	def post(self):
		teacher_name = self.request.get('teacher_name')
		department = int(self.request.get('department'))
		teaching_time = self.request.get('teaching_time')

		# sun = self.request.get('sun').replace(' ', '').split(',')
		# mon = self.request.get('mon')
		# tue = self.request.get('tue')
		# wed = self.request.get('wed')
		# thu = self.request.get('thu')
		# fri = self.request.get('fri')
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
