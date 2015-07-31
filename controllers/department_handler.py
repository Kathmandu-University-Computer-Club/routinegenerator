from controllers.base_handler import *
from models.Department import Department
from google.appengine.ext import db

class DepartmentHandler(BaseHandler):
	def get(self):
		departments = db.GqlQuery("SELECT * from Department ORDER BY department_name")
		self.render("department.html",{'departments':departments})
	def post(self):
		department_name = self.request.get('department_name')
		department_id = int(self.request.get('department_id') or 0)

		if department_id:
			department = Department.get_by_id(department_id)
			department.department_name = department_name
			department.put()
		else:
			department = Department(
				id = department_id,
				department_name = department_name
			)
			department.put()
		self.redirectto('/department')
