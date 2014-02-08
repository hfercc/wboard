import common
from common import exceptions, utils
from django.http import Http404
from common.ajax_response import STATUS_SUCCESS
from  __init__ import get_class

@common.login_required
@common.ajax_by_method('notification/list.html')
def notifications_list(request):
	kind = request.GET.get('kind','') or request.POST.get('kind','')
	if not kind:
		raise Http404
	if kind == 'all':
		objects = []
		for i in ['status', 'comment', 'pm']:
			objects+=get_class(i).objects.notifications(request.user)
	else:
		notification_class = get_class(kind)
		objects = notification_class.objects.notifications(request.user)
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