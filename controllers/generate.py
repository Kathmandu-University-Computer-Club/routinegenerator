from controllers.base_handler import *
from google.appengine.ext import db
from models.Teacher import Teacher
from models.Department import Department
from models.Course import Course

import random
import json
import copy

def findTiming(day, duration):
	# [1,2,4,5,6] 3
	

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
					# r['timing'].append([day[i], day[j]])
					r.append([day[i], day[j]])
			k += 1
	return r

	# if not day:
	# 	return []
	# r = {"duration": duration,
	# 	"timing": []
	# }
	# r = []
	# for i in range(0, len(day)):
	# 	d = duration
	# 	k = 0
	# 	for j in range(i, len(day)):
	# 		if i + k == j:
	# 			# days are continuous 
	# 			d -= 1
	# 			if d == 0:
	# 				# r['timing'].append([day[i], day[j]])
	# 				r.append([day[i], day[j]])
	# 		k += 1
	# return r

def findTeachingTime(subject, available_teaching_time, total_classes, class_duration, routine, possibilities):
	# print subject, available_teaching_time, total_classes, class_duration, routine
	# viable_days = []
	for day in routine:
		# day_has_subject = False
		# for r in routine[day]:
		# 	if r[0] == subject:
		# 		day_has_subject = True
		# 		break;

		# if day_has_subject == False:
			# no subject in that day..
			# so find if teacher has available time in that class.
		

		if day in available_teaching_time:
			pt = findTiming(available_teaching_time[day], class_duration)
			
			if len(pt):
				# if day not in viable_days:
					# viable_days.append(day)
				possibilities[day][class_duration] = pt
		# randomday = viable_days[random.randint(0, len(viable_days) - 1)]
		# print randomday
	# print viable_days
			# print day, findTiming(available_teaching_time[day], class_duration)
	




	return False









def overlaps(a, b):
	if a[1] < b[0] or a[0] > b[1]:
		return False
	return True


def get_random_day_for_duration(possibilities, duration, routine):
	# remove overlapping classes from possibilities

	for day in routine:

		for class_ in routine[day]:
			# if day in possibilities
				for class_duration in possibilities[day]:
					toremove = []
					for x in possibilities[day][class_duration]:
						if overlaps(x, class_['timing']):
							print x, class_['timing']
							toremove.append(x)
					for x in toremove:
						possibilities[day][class_duration].remove(x)
			# print day, class_

	# for k_day in possibilities:
	# 	x = possibilities[k_day] # "1": [[1, 1 ], [3, 3 ], [4, 4 ] ], "2" :[..]
	# 	for y in x:
	# 			z = x[y] #[[1, 1 ], [3, 3 ], [4, 4 ] ]
	# 		# for day in routine:
	# 			# for class_ in routine[day]:
	# 			print k_day, z, routine[k_day]
	# 			# for class_ in routine[k_day]:
	# 			# 	v = class_['timing']
	# 			# 	for u in z:
	# 			# 		if not (u[1] < v[0] or u[0] > v[1]): 
	# 			# 			# z.remove(class_['timing'])
	# 			# 			# print u, v, k_day
	# 			# 			z.remove(u)

	# 						# pass

	# 				# if class_['timing'] in z:
	# 					# z.remove(class_['timing'])

	keys = [key for key in possibilities if possibilities[key] != {} and duration in possibilities[key]]

  # print keys
	# print possibilities
	# return "sunday"
	r = keys[random.randint(0, len(keys) - 1)]
	# now delete from possibilities of class and from teacher's avaliable timing
	# rtime = 
	# print possibilities[r]
	# print "__"
	# print possibilities[r][duration]

	return r, random.choice(possibilities[r][duration])

class GenerateHandler(BaseHandler):
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
		while total_tries < 5 and inner_fail == True:
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
							# print class_distribution[subject]['possibilities']
							# print randomday, i, subject, randomtime
							# delete class_distribution[subject]['possibilities'][randomday]
							# class_distribution[subject]['possibilities'].pop(randomday, None)
							# print class_distribution[subject]['possibilities']
							routine[randomday].append({
								'subject': subject,
								'teacher': class_distribution[subject]['teacher'],
								'timing': copy.deepcopy(randomtime)
								})
							class_distribution[subject]['possibilities'][randomday] = {}
							# print "--"
							print routine




							# for day in routine:
							# 	for class_ in routine[day]:
							# 		print day, class_


							distribution[str(i)] -= 1 #reduce total classes
							# print distribution[str[i]]

		self.response.headers['Content-Type'] = 'application/json'
		# self.write(json.dumps(original_classes,sort_keys=True, indent=4))
		self.write(json.dumps(classes,sort_keys=True, indent=4))