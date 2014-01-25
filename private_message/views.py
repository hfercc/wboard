import common, forms, models, __init__
from common import exceptions, utils
from models import PrivateMessage
from common.ajax_response import STATUS_SUCCESS
from django.http import HttpResponseRedirect, Http404

@common.login_required
@common.ajax_by_method('pm/list.html')
def private_message_list(request):
	kind = request.GET.get('kind', '')
	objects = PrivateMessage.objects.filter_message(request.user, kind)
	if not objects:
		raise Http404	
	objects = utils.paginate_to_dict(objects, request)
	objects.update({'kind': kind})
	return objects

@common.login_required
@common.ajax_by_method('pm/detail.html')
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
	return {}
	
@common.login_required
@common.csrf_protect
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
	else:
		pass   #expected to be completed
	return {}