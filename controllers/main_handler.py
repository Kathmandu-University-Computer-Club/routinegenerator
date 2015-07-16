from controllers.base_handler import *

class MainHandler(BaseHandler):
	def get(self):
		# self.response.write('Hello')
		self.render("index.html", {'layoutTitle': 'Home'})
