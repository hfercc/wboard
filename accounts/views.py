import common
from common.utils import get_object_by_id
from django.contrib.auth.models import User
from common.ajax_response import STATUS_SUCCESS

@common.login_required
@common.render_to('accounts/info.html')
def info(request, user_id):
	user = get_object_by_id(User, user_id, True)
	return {'data':{'user': user}}
	
@common.method('POST')
@common.login_required
@common.ajax_request
def make_friends(request):
	friend = get_object_by_id(User, request.POST.get('id', ''))
	request.user.get_profile().friends.add(friend)
	return STATUS_SUCCESS