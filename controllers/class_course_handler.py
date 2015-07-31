from controllers.base_handler import *
from models.ClassCourse import ClassCourse
#from models.Course import Course
from google.appengine.ext import db

class ClassCourseHandler(BaseHandler):
	def get(self):
		classcourses = db.GqlQuery("SELECT * FROM ClassCourse")
		courses = db.GqlQuery("SELECT * FROM Course")
		faculties = db.GqlQuery("SELECT * FROM Faculty")
		teachers = db.GqlQuery("SELECT * FROM Teacher")

		# r = []
		# for classcourse in classcourses:
		# 	r.append({
		# 		'id': classcourse.key().id,
		# 		'faculty_id':classcourse.faculty,
		# 		'year': classcourse.year,
		# 		'semester': classcourse.semester,
		# 	})
		self.render("classcourse.html", {
			'classcourses':classcourses,
			'courses': courses,
			'faculties': faculties,
			'teachers': teachers
		})

	def post(self):
		faculty= self.request.get('faculty')
		year = int(self.request.get('year'))
		semester = int(self.request.get('semester'))
		# course = self.request.get('course').replace(', ', ',').split(',')
		cnt = 1
		r = {}
		while self.request.get('course_' + str(cnt)) != "":
			r[self.request.get('course_' + str(cnt))] = int(self.request.get('teacher_' + str(cnt)))
			cnt += 1
		# courses = str(self.request.get('courses').replace(" ", "").split(","))
		courses = r
		# self.response.write("ok")
		# return
		classcourse = ClassCourse(
			faculty = faculty,
			year = year,
			semester = semester,
			course = str(courses)
			)
		classcourse.put()
		self.response.write("Sucessfully")
