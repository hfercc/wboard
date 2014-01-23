import re

from django.conf import settings
from django.views.static import serve
from django.shortcuts import redirect

from exceptions import Redirect, AjaxError
from django.http import HttpResponse
import json

class AjaxMiddleware(object):
	
	def process_exception(self, request, exception):
		if isinstance(exception, AjaxError) and request.method == 'POST':
			return HttpResponse(json.dumps(exception.error))

class StaticServe(object):
    """
    Django middleware for serving static files instead of using urls.py
    """
    regex = re.compile(r'^%s(?P<path>.*)$' % settings.MEDIA_URL)

    def process_request(self, request):
        if settings.DEBUG:
            match = self.regex.search(request.path)
            if match:
                return serve(request, match.group(1), settings.MEDIA_ROOT)


class RedirectMiddleware(object):
    """
    You must add this middleware to MIDDLEWARE_CLASSES list,
    to make work Redirect exception. All arguments passed to
    Redirect will be passed to django built in redirect function.
    """
    def process_exception(self, request, exception):
        if not isinstance(exception, Redirect):
            return
        return redirect(*exception.args, **exception.kwargs)
