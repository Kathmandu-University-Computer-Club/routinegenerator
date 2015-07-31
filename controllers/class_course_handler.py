from controllers.base_handler import *
from models.ClassCourse import ClassCourse
#from models.Course import Course
from google.appengine.ext import db

class ClassCourseHandler(BaseHandler):
	def get(self):
		classcourse = db.GqlQuery("SELECT * FROM ClassCourse")
		courses = db.GqlQuery("SELECT * FROM Course")
		faculties = db.GqlQuery("SELECT * FROM Faculty")
		teachers = db.GqlQuery("SELECT * FROM Teacher")
		self.render("classcourse.html", {
			'classcourse':classcourse,
			'courses': courses,
			'faculties': faculties,
			'teachers': teachers
		})

	def post(self):
		faculty= self.request.get('faculty')
		year = int(self.request.get('year'))
		semester = int(self.request.get('semester'))
		# course = self.request.get('course').replace(', ', ',').split(',')
		courses = str(self.request.get('courses').replace(" ", "").split(","))
		# self.response.write("ok")
		# return
		classcourse = ClassCourse(
			faculty = faculty,
			year = year,
			semester = semester,
			course = courses
			)
		classcourse.put()
		self.response.write("Sucessfully")
