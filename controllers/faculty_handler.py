from controllers.base_handler import *
from google.appengine.ext import db
from models.Faculty import Faculty
from models.Department import Department

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
		f = []
		for faculty in faculties:
			f.append({
				'id': faculty.key().name(),
				'faculty_name': faculty.faculty_name,
				'department_id': faculty.department,
				'department_name': Department.get_by_id(faculty.department).department_name
			})
		self.render("faculty.html",{'faculties':f, 'departments':departments})
		# self.render("faculty.html",{'faculties':faculties, 'departments':departments})

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
