from django.db import models
from django.contrib.auth.models import User

class Attachment(models.Model):
	
	url           = models.URLField()
	file_name     = models.CharField(max_length = 255)
	uploaded_time = models.DateTimeField()
	
	def __unicode__(self):
		return unicode('Attachment %s at %s' % (self.file_name, self.url))
		
class PrivateMessageManager(models.Manager):		
	
	def unread_messages(self, user):
		return self.filter(receiver = user.id, has_read = False)
		
	def posted_messages(self, user):
		return self.filter(sender = user.id)

class PrivateMessage(models.Model):

	sender       = models.ForeignKey(User, related_name = 'privatemessage_senders')
	receiver     = models.ForeignKey(User, related_name = 'privatemessage_receivers')
	body_text    = models.TextField()
	created_time = models.DateTimeField(auto_now_add = True)
	attachments  = models.ManyToManyField(Attachment)
	has_read     = models.BooleanField(default = False)
	#Manager
	objects      = PrivateMessageManager()
	
	def __unicode__(self):
		return unicode('Attachment from %s to %s. %d attachments contained.' % (
				self.sender.get_profile().nick_name, 
				self.receiver.get_profile().nick_name,
				len(self.attachments)
			)
		)
	
	def mark_read(self, flag = True):
		self.has_read = flag
		self.save()
