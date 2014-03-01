import common
from common import exceptions, utils
from django.http import Http404
from common.ajax_response import STATUS_SUCCESS
from  __init__ import get_class
from django.views.decorators.cache import cache_page

@common.login_required
#@cache_page(20)
@common.ajax_by_method('notification/list.html')
def notifications_list(request):
	kind = request.GET.get('kind','') or request.POST.get('kind','')
	if kind == 'all':
		args = {}
	elif kind == 'unread':
		args = {'has_read': False}
	else:
		raise Http404
	print args
	objects = []
	for i in ('status', 'comment'):
		q = get_class(i).objects.notifications(request.user).filter(**args)
		if kind == 'all':
			utils.mark_read(q)
			common.kv.ChannelKV(request.user).send_unread()
		objects += q
	notifications = utils.paginate_to_dict(
			objects,
			request
	)
	return notifications
	
@common.login_required
@common.method('POST')
@common.ajax_request
def delete(request, notification_id):
	kind = request.GET.get('kind','') or request.POST.get('kind','')
	if not kind:
		raise Http404	
	notification = utils.get_object_by_id(get_class(kind), notification_id)
	utils.verify_user(request, notification.receiver)
	notification.delete()
	return {}
	
@common.login_required
@common.ajax_by_method('notification/detail.html')
def detail(request, notification_id):
	kind = request.GET.get('kind','') or request.POST.get('kind','')
	if not kind:
		raise Http404
	notification = utils.get_object_by_id(get_class(kind), notification_id, method = request.method)
	notification.mark_read()
	utils.verify_user(request, notification.receiver)
	return {'notification': notification}