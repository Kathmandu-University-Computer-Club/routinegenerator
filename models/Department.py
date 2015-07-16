from google.appengine.ext import db

class Department(db.Model):
	department_name = db.StringProperty(required = True)
	# class_per_week = db.IntegerProperty(default = 5)
    # class_Distribution = db.StringProperty(default = "{1:5}")


