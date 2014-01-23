from common import render_to, login_required
from common.utils import get_object_by_id
from django.contrib.auth.models import User
from common.ajax_response import STATUS_SUCCESS

@login_required
@render_to('accounts/info.html')
def info(request, user_id):
	user = get_object_by_id(User, user_id, True)
	return {'data':{'user': user}}
	
@method('POST')
@login_required
@ajax_request
def make_friend(request):
	friend = get_object_by_id(User, request.POST.get('id', '')
	request.user.get_profile().friends.add(friend)
	return STATUS_SUCCESS