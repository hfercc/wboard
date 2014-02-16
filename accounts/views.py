import common
from common.utils import get_object_by_id
from django.contrib.auth.models import User
from django.contrib import auth
from common.ajax_response import STATUS_SUCCESS

#@common.method('POST')
#@common.ajax_request
@common.ajax_by_method('registration/login.html')
def login(request):
	if request.method == 'GET':
		return {}
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username = username, password = password)

	if user:
		auth.login(request, user)
		response = {'user':user}
		return response
	else:
		raise common.AuthenticatedFailed
		
@common.ajax_request
def logout(request):
	auth.logout(request)
	return {}

@common.login_required
@common.ajax_by_method('accounts/info.html')
def info(request, user_id):
	user = get_object_by_id(User, user_id, method = request.method)
	return {'object': user}
	
@common.method('POST')
@common.login_required
@common.ajax_request
def make_friends(request):
	action = request.POST.get("action",'') or request.GET.get("action", '')
	friend = get_object_by_id(User, request.POST.get('id', ''))
	if action == 'add':
		request.user.profile.friends.add(friend)
	elif action == 'remove':
		if friend in request.user.profile.friends.all():
			request.user.profile.friends.remove(friend)
		else:
			return {}
	return {}
	
@common.method('POST')
@common.login_required
@common.ajax_request
def friends(request):
	return {'objects': request.user.profile.friends.all()}