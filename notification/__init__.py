import models
from models import Notification
from django.contrib.auth.models import User
from common import utils
from itertools import chain

notification_classes = {'comment': models.CommentNotification,
												'status' : models.StatusNotification,
										#		'pm'     : models.PrivateMessageNotification
											 }	

get_class = lambda s: notification_classes[s]
				
def send_notification(receiver, kind, **kw_args):
	cls = notification_classes[kind]
	if kind == 'comment':
		n = cls(receiver = receiver, comment = kw_args['comment'])
	elif kind == 'status':
		n = cls(receiver = receiver, status = kw_args['status'], category = kw_args['category'])
	# elif kind == 'pm':
		# n = cls(receiver = receiver, private_message = kw_args['private_message'])
	n.save()
	return n
	
def send_notification_to_admin(kind, **kw_args):
	admin = User.objects.get(username = "xstd")
	return send_notification(admin, kind, **kw_args)