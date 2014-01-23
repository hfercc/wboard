import common, forms, models, __init__
from common import exceptions, utils
from models import PrivateMessage
from common.ajax_response import STATUS_SUCCESS
from django.http import HttpResponseRedirect, Http404

@common.login_required
@common.render_to('pm/list.html')
def private_message_list(request):
	kind = request.GET.get('kind', '')
	if kind == 'sent':
		objects = request.user.private_message_sent
	elif kind == 'received':
		objects = request.user.private_message_received
	elif kind == 'all':
		objects = request.user.private_message_sent + request.user.private_message_received
	else:
		raise Http404
	return {'private_messages': utils.paginate_by_request(objects, request),
					'kind': kind
					}

@common.login_required
@common.render_to('pm/detail.html')
def detail(request, pm_id):
	private_message = utils.get_object_by_id(PrivateMessage, pm_id)
	utils.verify_user(request, (private_message.sender, private_message.receiver))
	return {'private_message': private_message}
	
@common.login_required
def delete_get(request, pm_id):
	private_message = utils.get_object_by_id(PrivateMessage, pm_id, True)
	utils.verify_user(request, private_message.sender)
	private_message.delete()
	return HttpResponseRedirect('/pm/list/')
	
@common.login_required
@common.ajax_request
def delete_post(request, pm_id):
	private_message = utils.get_object_by_id(PrivateMessage, pm_id)
	utils.verify_user(request, private_message.sender)
	private_message.delete()
	return STATUS_SUCCESS
	
@common.login_required
@common.render_to('pm/write.html')
def write_get(request):
	return {}

@common.login_required
@common.ajax_request
def write_post(request):
	form = PrivateMessageForm(request.POST)
	if form.is_valid():
		for user in form.users_received:
			__init__.send_private_message_and_notify(
					request.user,
					user,
					form.cleaned_data.body_text,
					form.attachments
			)
	return STATUS_SUCCESS