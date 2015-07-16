from controllers.base_handler import *
from models.Faculty import Faculty
from google.appengine.ext import db

class FacultyHandler(BaseHandler):
	def get(self):
		faculties = db.GqlQuery("SELECT * FROM Faculty")
		departments = db.GqlQuery("SELECT * FROM Department")
		# for faculty  in faculties:
		# 	# found = False
		# 	for department in departments:
		# 		if faculty.department == department.key().id():
		# 			# found = True
		# 			# faculty.department = department.department_name
		# 			# faculty['department'] = department.department_name
		# 			break
		self.render("faculty.html",{'faculties':faculties, 'departments':departments})

	def post(self):
		faculty_id= self.request.get('faculty_id')
		faculty_name= self.request.get('faculty_name')
		department = int(self.request.get('department'))

		faculty = Faculty(
			key_name = faculty_id,
			faculty_name = faculty_name,
			department = department
			)

		faculty.put()
		self.response.write("Sucessfully")
