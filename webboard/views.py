import common, forms
from common import exceptions, utils
from common.ajax_response import STATUS_SUCCESS
from models import Status, Comment
from django.http import HttpResponseRedirect
from notification import send_notification, send_notification_to_admin

@common.login_required
@common.render_to('/webboard/status/list.html')
def status_list(request):
	return {
			'statuses': utils.paginate_by_request(
					Status.objects.verified_statuses, 
					request
			)
	}		
	
@common.login_required
@common.render_to('/webboard/status/detail.html')
def detail(request, status_id):
	status = utils.get_object_by_id(Status, status_id, True)
	return {'status': status}
	
def _add_or_modify(request, status_id = ''):
	
	@common.render_to('/webboard/status/add.html')
	def get():
		if status_id:
			status = utils.get_object_by_id(Status, status_id, True)
			return {'status': status}
		else:
			return {}
		
	@common.ajax_request
	def post():
		if status_id:
			status = utils.get_object_by_id(Status, status_id)
			status.save()
		else:
			form = forms.StatusForm(request.POST)
			if form.is_valid():
				data = form.cleaned_data
				status = Status(author    = request.user,
												title     = data.title,
												body_text = data.body_text
										)
				status.save()
				send_notification_to_admin('status', status = status, category = 'POSTED')
			else:
				raise exceptions.DataFieldMissed
				
		return STATUS_SUCCESS
		
	if request.method == 'POST':
		return post()
	elif request.method == 'GET':
		return get()
		
@common.login_required
@common.permission_required('status.post')
def add(request):
	return _add_or_modify(request)
	
@common.login_required
@common.permission_required('status.delete_modify')
def modify(request, status_id):
	return _add_or_modify(request, status_id)

@common.login_required
@common.permission_required('status.delete_modify')
def delete_get(request, status_id):
	send_notification(status.author, 
										'status',
										status = status,
										category = 'DELETED'
										)
	utils.get_object_by_id(request, status_id, True).delete()
	return HttpResponseRedirect('/status/list/')
	
@common.login_required
@common.permission_required('status.delete_modify')
@common.ajax_request
def delete_post(request, status_id):
	send_notification(status.author, 
										'status',
										status = status,
										category = 'DELETED'
										)
	utils.get_object_by_id(Status, status_id).delete()
	return STATUS_SUCCESS
	
@common.login_required
@common.permission_required('status.verify')
@common.ajax_request
def verify(request, status_id):
	status = utils.get_object_by_id(Status, status_id)
	action = request.GET.get('action', '')
	if action == 'verify':
		send_notification(status.author, 
											'status',
											status = status,
											category = 'VERIFIED'
											)
		status.verify()
	elif action == 'reject':
		send_notification(status.author,
											'status',
											status = status,
											category = 'REJECTED'
											)
		status.reject()
	return STATUS_SUCCESS
	
#=======================Comment Part========================

@utils.method('POST')
@common.login_required
@common.ajax_request
def add_comment(request):
	form = forms.CommentForm(request.POST)
	if form.is_valid():
		data = form.cleaned_data
		comment = Comment(status = form.status,
											body_text = data.body_text,
											author = request.user
											)
		comment.save()
		send_notification(form.status.author,
											'comment',
											comment = comment
											)
	else:
		raise exceptions.DataFieldMissed
	return STATUS_SUCCESS
	
@utils.method('POST')
@common.login_required
@common.ajax_request
def delete_comment(request, comment_id):
	comment = utils.get_object_by_id(Comment, comment_id)
	utils.verify_user(request, comment.author)
	comment.delete()
	return STATUS_SUCCESS