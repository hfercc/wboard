from django.db import models
from django.contrib.auth.models import User

class Attachment(models.Model):
	
	storage_path  = models.CharField(max_length = 255)
	uploaded_time = models.DateTimeField()
	
	def __unicode__(self):
		return unicode('Attachment: %s' % self.storage_path)
		
class PrivateMessage(models.Model):

	sender      = models.ForeignKey(User, related_name = 'privatemessage_senders')
	receiver    = models.ForeignKey(User, related_name = 'privatemessage_receivers')
	body_text   = models.TextField()
	title       = models.CharField(max_length = 255)
	attachments = models.ManyToManyField(Attachment)
	has_read    = models.BooleanField()
	
	def __unicode__(self):
		return unicode('Attachment from %s to %s. %d attachments contained.' % (
				self.sender.first_name, 
				self.receiver.first_name,
				len(self.attachments)
			)
		)
	
	def make_read(self, flag):
		pass
