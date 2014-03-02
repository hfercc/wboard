from exceptions import Redirect, AjaxError
from django.http import HttpResponse
import json

class AjaxMiddleware(object):
	
	def process_exception(self, request, exception):
		if isinstance(exception, AjaxError):
			return HttpResponse(json.dumps(exception.error))