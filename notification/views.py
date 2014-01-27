import common
from common import exceptions, utils
from common.ajax_response import STATUS_SUCCESS
from  __init__ import get_class

@common.login_required
@common.ajax_by_method('notification/list.html')
def notifications_list(request, kind):
	notification_class = get_class(kind)
	notifications = utils.paginate_to_dict(
			notification_class.objects.notifications(request.user), 
			request
	)
	return notifications
	
@common.login_required
@common.method('POST')
@common.ajax_request
def delete(request, kind, notification_id):
	notification = utils.get_object_by_id(get_class(kind), notification_id)
	utils.verify_user(request, notification.receiver)
	notification.delete()
	return {}
	
@common.login_required
@common.ajax_by_method('notification/detail.html')
def detail(request, kind, notification_id):
	notification = utils.get_object_by_id(get_class(kind), notification_id, method = request.method)
	notification.mark_read()
	utils.verify_user(request, notification.receiver)
	return {'notification': notification}