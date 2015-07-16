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
		class_distribution = self.request.get('class_distribution')

		course = Course(
			key_name = course_id,
			course_name = course_name,
			class_per_week = class_per_week,
			class_distribution = class_distribution
			)
		course.put()
		self.response.write("success")
