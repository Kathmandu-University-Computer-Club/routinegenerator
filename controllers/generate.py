from controllers.base_handler import *
from google.appengine.ext import db
from models.Teacher import Teacher
from models.Department import Department
from models.Course import Course

import random
import json
import copy

def findTiming(day, duration):
	# [1,2,4,5,6]    3
	if not day:
		return []
	r = []
	for i in range(0, len(day)):
		d = duration
		k = 0
		for j in range(i, len(day)):
			if day[i] + k == day[j]:
				# days are continuous 
				d -= 1
				if d == 0:
					r.append([day[i], day[j]])
			k += 1
	return r

def findTeachingTime(subject, available_teaching_time, total_classes, class_duration, routine, possibilities):
	for day in routine:
		if day in available_teaching_time:
			pt = findTiming(available_teaching_time[day], class_duration)
			if len(pt):
				possibilities[day][class_duration] = pt
	return False

def overlaps(a, b):
	if a[1] < b[0] or a[0] > b[1]:
		return False
	return True


def get_random_day_for_duration(possibilities, duration, routine):
	# remove overlapping classes from possibilities

	for day in routine:
		for class_ in routine[day]:
			for class_duration in possibilities[day]:
				toremove = []
				for x in possibilities[day][class_duration]:
					if overlaps(x, class_['timing']):
						print x, class_['timing']
						toremove.append(x)
				for x in toremove:
					possibilities[day][class_duration].remove(x)
	keys = [key for key in possibilities if possibilities[key] != {} and duration in possibilities[key]]
	r = keys[random.randint(0, len(keys) - 1)]
	return r, random.choice(possibilities[r][duration])

class GenerateAjaxHandler(BaseHandler):
	def get(self):
		teachers = db.GqlQuery("Select * from Teacher")
		teachers_timing = {}
		for teacher in teachers:
			teachers_timing[teacher.key().id()] = eval(teacher.teaching_time)

		print teachers_timing
		classCourses = db.GqlQuery("Select * from ClassCourse")
		
		classes = {}
		for classCourse in classCourses:
			classes[classCourse.key().id()] = {
				'routine': {
					'sunday': [],
					'monday': [],
					'tuesday': [],
					'wednesday': [],
					'thursday': [],
					'friday': []
				},
				'class_distribution': {

				},
				'details': {
					'faculty': classCourse.faculty,
					'year': classCourse.year,
					'semester': classCourse.semester
				}
			}

			eCourse = eval(classCourse.course)
			for course in eCourse:
				# l = Teacher.get_by_id(eCourse[course])
				l = {
					'distribution': eval(Course.get_by_key_name(course).class_distribution),
					'teacher': eCourse[course],
					'teaching_time': eval(Teacher.get_by_id(eCourse[course]).teaching_time),
					'possibilities': {
						'sunday': {},
						'monday': {},
						'tuesday': {},
						'wednesday': {},
						'thursday': {},
						'friday': {}
					},

				}
				# print l
				classes[classCourse.key().id()]['class_distribution'][course] = l


		for class_ in classes:
			class_distribution = classes[class_]['class_distribution']
			routine = classes[class_]['routine']
			for subject in class_distribution:
				distribution = class_distribution[subject]['distribution']
				for i in range(4, 0, -1):
					if distribution[str(i)] != 0:
						# print "found " + str(i) + " " + str(distribution[str(i)]) + subject
						findTeachingTime(subject = subject,
							available_teaching_time = class_distribution[subject]['teaching_time'],
							routine = routine,
							class_duration = i,
							total_classes = distribution[str(i)],
							possibilities = class_distribution[subject]['possibilities']
						)

		total_tries = 0
		original_classes = copy.deepcopy(classes)
		inner_fail = True
		while total_tries < 50 and inner_fail == True:
			inner_fail = False
			total_tries += 1
			classes = copy.deepcopy(original_classes)
			# classes = 
			for class_ in classes:
				class_distribution = classes[class_]['class_distribution']
				routine = classes[class_]['routine']
				for subject in class_distribution:
					distribution = class_distribution[subject]['distribution']
					for i in range(4, 0, -1):
						tries = 0
						while distribution[str(i)] != 0:
							if tries > 10:
								print "giving up"
								inner_fail = True
								break

							try:
								randomday, randomtime = get_random_day_for_duration(class_distribution[subject]['possibilities'], i, routine)
							except:
								tries += 1
								continue	
							t = Teacher.get_by_id(class_distribution[subject]['teacher'])
							routine[randomday].append({
								'subject': subject,
								'teacher': {
									'id': t.key().id(),
									'name': t.teacher_name,
								},
								'timing': copy.deepcopy(randomtime)
								})
							class_distribution[subject]['possibilities'][randomday] = {}
							# print "--"
							print routine

							distribution[str(i)] -= 1 #reduce total classes
		self.response.headers['Content-Type'] = 'application/json'
		# self.write(json.dumps(original_classes,sort_keys=True, indent=4))
		self.write(json.dumps(classes,sort_keys=True, indent=4))
		# self.write(classes)

class GenerateHandler(BaseHandler):
	def get(self):
		self.render("generate.html")
