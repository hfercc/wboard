from decorators import render_to, method, ajax_request
from exceptions import MethodError
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect