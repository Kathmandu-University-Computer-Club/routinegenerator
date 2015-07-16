from controllers.base_handler import *
from models.Department import Department
from google.appengine.ext import db

class DepartmentHandler(BaseHandler):
	def get(self):
		departments = db.GqlQuery("SELECT * from Department")
		self.render("department.html",{'departments':departments})
	def post(self):
		department_name = self.request.get('department_name')


		department = Department(
			department_name = department_name
		)

		department.put()
		self.response.write("success")
