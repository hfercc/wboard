import common
from common.utils import get_object_by_id, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Permission
from django.contrib import auth
from common.ajax_response import STATUS_SUCCESS
import models

@common.permission_required("delete_modify")
def add_friend(request):
    l = User.objects.all()
    for user in l:
        friends_list = user.profile.friends.all()
        for friend in l.exclude(username=user.username):
            if not friend in friends_list:
                user.profile.friends.add(friend)
    return HttpResponse("OK")

@common.permission_required("delete_modify")
def add(request):
	if request.method == 'GET':
		return render_to_response("accounts/add.html")
	data = request.POST["data"]
	tmp = "qwertyuiopasdfghjklzxcvbnm1234567890"
	psw = {}
	import random
	for user in data.split("\n"):
		a = user.split()
		username = a[1]
		try:
			u = User.objects.get(username = username)
		except:
			u = None
		nick_name = a[0]
		p = a[2] if len(a)>2 else ""
		l = range(random.randint(6,10))
		code = ""
		for i in l:
			code+=tmp[random.choice(l)]
		if not u:
			u = User.objects.create_user(username, '', password = code)
		else:
			u.set_password(code)
		permissions = []
		if "d" in p:
			permissions += ['verify', 'delete_modify']
		if "p" in p:
			permissions += ['post']
		u.save()
		for i in permissions:
			u.user_permissions.add(Permission.objects.get(codename=i))
		#u.user_permissions.add([Permission.objects.get(codename=i) for i in permissions])
		u.profile.nick_name = nick_name
		u.profile.save()
		u.save()
		psw[nick_name] = code
	html = '<br/>'.join([':'.join((i,j)) for i,j in psw.iteritems()])
	return HttpResponse(html)

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
		
#@common.ajax_request
def logout(request):
	auth.logout(request)
	return common.utils.HttpResponseRedirect("/")

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