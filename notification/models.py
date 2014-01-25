from django.db import models
from django.contrib.auth.models import User
from common import jsonobj
from private_message.models import PrivateMessage
from webboard.models import Status, Comment

class NotificationManager(models.Manager):

	def unread_notifications(self, user):
		return self.filter(receiver = user.id, has_read = False)
		
	def notifications(self, user):
		return self.filter(receiver = user.id)

class Notification(jsonobj.JsonObjectModel):   #abstract class of notification
	
	created_time = models.DateTimeField(auto_now_add = True)
	receiver     = models.ForeignKey(User)
	has_read     = models.BooleanField(default = False)
	
	json_extra   = ['kind']
	
	def __unicode__(self):
		return unicode('%s\'s notification.' % self.receiver.profile.nick_name)
		
	def url(self):                    #abstract
		pass
		
	def mark_read(self, flag):        #abstract
		self.has_read = flag
		self.save()
		
	def message(self):                #abstract
		pass
		
	def kind(self):                   #abstract
		pass
	
	class Meta:
		abstract = True
		
class PrivateMessageNotification(Notification):

	private_message = models.OneToOneField(PrivateMessage, related_name = 'notification')
	
	def kind(self):
		return 'pm'
	
class StatusNotification(Notification):
	
	status   = models.ForeignKey(Status, related_name = 'notifications')
	category = models.CharField(max_length = 10, choices = [
						('POSTED',   'posted'),
						('REJECTED', 'rejected'),
						('VERIFIED', 'verified'),
						('DELETED',  'deleted'),
	])
	
	def kind(self):
		return 'status'
	
class CommentNotification(Notification):
	
	comment = models.OneToOneField(Comment, related_name = 'notification')
	
	def kind(self):
		return 'comment'