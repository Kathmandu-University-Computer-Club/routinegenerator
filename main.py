#!/usr/bin/env python

from controllers.base_handler import *
from controllers.main_handler import MainHandler
from controllers.course_handler import CourseHandler
from controllers.class_course_handler import ClassCourseHandler
from controllers.faculty_handler import FacultyHandler
from controllers.department_handler import DepartmentHandler
from controllers.teacher_handler import TeacherHandler
from controllers.generate import GenerateHandler, GenerateAjaxHandler
import webapp2


			
app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/course',CourseHandler),
	('/classcourse',ClassCourseHandler),
	('/faculty',FacultyHandler),
	('/department',DepartmentHandler),
	('/teacher', TeacherHandler),
	('/generate', GenerateHandler),
	('/generateAjax', GenerateAjaxHandler),

], debug=True)
