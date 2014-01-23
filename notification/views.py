from common import exceptions,
	render_to, method, ajax_request, login_required, utils, ajax_response
from  __init__ import get_class

@login_required
@render_to('notification/list.html')
def notifications_list(request, kind):
	notification_class = get_class(kind)
	notifications = utils.paginate_by_request(
			notification_class.objects.notifications(request.user), 
			request
	)
	return {'objects': notifications}
	
@login_required
@method('POST')
@ajax_request
def delete(request, kind, notification_id):
	notification = utils.get_object_by_id(get_class(kind), notification_id)
	utils.verify_user(request, notification.receiver)
	notification.delete()
	return ajax_response.STATUS_SUCCESS
	
@login_required
@render_to('notification/detail.html')
def detail(request, kind, notification_id):
	notification = utils.get_object_by_id(get_class(kind), notification_id)
	notification.mark_read()
	utils.verify_user(request, notification.receiver)
	return {'notification': notification}