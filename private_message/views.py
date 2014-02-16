import common, forms, models, __init__
from common import exceptions, utils
from models import PrivateMessage
from common.ajax_response import STATUS_SUCCESS
from django.http import HttpResponseRedirect, Http404

@common.login_required
@common.ajax_by_method('pm/list.html')
def private_message_list(request):
	kind = request.GET.get('kind', 'all') or request.POST.get('kind', 'all')
	objects = PrivateMessage.objects.filter_messages(request.user, kind)
	user_id = request.GET.get('user_id', '') or request.POST.get('user_id', '')
	if user_id:
		objects = objects.filter(sender = user_id) + objects.filter(receiver = user_id)
	if not objects and request.method == 'GET':
		raise Http404	
	objects = utils.paginate_to_dict(objects, request)
	objects.update({'kind': kind})
	return objects

@common.login_required
@common.ajax_by_method('pm/detail.html')
def detail(request, pm_id):
	private_message = utils.get_object_by_id(PrivateMessage, pm_id, method = request.method)
	utils.verify_user(request, (private_message.sender, private_message.receiver))
	return {'private_message': private_message}
	
@common.method('POST')
@common.login_required
@common.ajax_request
def delete(request, pm_id):
	private_message = utils.get_object_by_id(PrivateMessage, pm_id)
	utils.verify_user(request, private_message.sender)
	private_message.delete()
	return {}
	
@common.login_required
#@common.csrf_protect
@common.render_to('pm/write.html')
def write_get(request):
	return {}

@common.login_required
@common.ajax_request
def write_post(request):
	form = forms.PrivateMessageForm(request.POST)
	if form.is_valid():
		for user in form.users_received:
			__init__.send_private_message_and_notify(
					request.user,
					user,
					form.cleaned_data['body_text'],
					form.attachments
			)
	else:
		raise exceptions.DataFieldMissed
	return {}