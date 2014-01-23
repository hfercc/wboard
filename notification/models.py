from django.db import models
from django.contrib.auth.models import User
from private_message.models import PrivateMessage
from webboard.models import Status, Comment

class NotificationManager(models.Manager):

	def unread_notifications(self, user):
		return self.filter(receiver = user.id, has_read = False)
		
	def notifications(self, user):
		return self.filter(receiver = user.id)

class Notification(models.Model):   #abstract class of notification
	
	created_time = models.DateTimeField(auto_now_add = True)
	receiver     = models.ForeignKey(User)
	has_read     = models.BooleanField(default = False)
	
	def __unicode__(self):
		return unicode('%s\'s notification.' % self.receiver.get_profile().nick_name)
		
	def url(self):                    #abstract
		pass
		
	def mark_read(self, flag):        #abstract
		self.has_read = flag
		self.save()
		
	def message(self):                #abstract
		pass
		
	class Meta:
		abstract = True
		
class PrivateMessageNotification(Notification):

	private_message = models.ForeignKey(PrivateMessage)
	
	
class StatusNotification(Notification):
	
	status   = models.ForeignKey(Status)
	category = models.CharField(max_length = 10, choices = [
						('POSTED','posted'),
						('REJECTED', 'rejected'),
						('VERIFIED', 'verified')
	])
	
class CommentNotification(Notification):
	
	comment = models.ForeignKey(Comment)