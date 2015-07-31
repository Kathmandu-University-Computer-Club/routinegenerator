from controllers.base_handler import *
from models.Course import Course
from google.appengine.ext import db

class CourseHandler(BaseHandler):
	def get(self):
		courses = db.GqlQuery("SELECT * FROM Course")
		self.render("course.html",{'courses':courses, 'layoutTitle': 'Course'})

	def post(self):
		course_id = self.request.get('course_id')
		course_name = self.request.get('course_name')
		class_per_week = int(self.request.get('class_per_week'))
		class_distribution_1 = int(self.request.get('class_distribution_1') or 0)
		class_distribution_2 = int(self.request.get('class_distribution_2') or 0)
		class_distribution_3 = int(self.request.get('class_distribution_3') or 0)
		class_distribution_4 = int(self.request.get('class_distribution_4') or 0)
		class_distribution = {
			"1": class_distribution_1,
			"2": class_distribution_2,
			"3": class_distribution_3,
			"4": class_distribution_4
		}

		course = Course(
			key_name = course_id,
			course_name = course_name,
			class_per_week = class_per_week,
			class_distribution = str(class_distribution)
		)
		course.put()
		self.response.write("success")
