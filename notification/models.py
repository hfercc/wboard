from django.db import models
from django.contrib.auth.models import User
from private_message.models import PrivateMessage
from webboard.models import Status, Comment

class Notification(models.Model):   #abstract class of notification
	
	created_time = models.DateTimeField()
	receiver     = models.ForeignKey(User)
	has_read     = models.BooleanField()
	
	def __unicode__(self):
		return unicode('%s\'s notification.' % self.receiver.first_name)
		
	def url(self):                    #abstract
		pass
		
	def mark_read(self, flag):        #abstract
		pass
		
	def message(self):                #abstract
		pass
		
	class Meta:
		abstract = True
		
class PrivateMessageNotification(Notification):

	private_message = models.ForeignKey(PrivateMessage)
	
	
class StatusNotification(Notification):

	#notification kind constants
	REJECTED = 1
	VERIFIED = 2
	POSTED   = 3
	
	status = models.ForeignKey(Status)
	kind   = models.IntegerField()
	
class CommentNotification(Notification):
	
	comment = models.ForeignKey(Comment)