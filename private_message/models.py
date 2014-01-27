# -*- coding: cp936 -*-
from django.db import models
from common import jsonobj
from django.contrib.auth.models import User

class Attachment(jsonobj.JsonObjectModel):
	
	url           = models.URLField()
	file_name     = models.CharField(max_length = 255)
	uploaded_time = models.DateTimeField()
	
	def __unicode__(self):
		return u'URL为%s的附件 %s。' % (self.url, self.file_name)
		
	class Meta(jsonobj.JsonObjectModel.Meta):
		abstract = False
		verbose_name = u'附件'
		
class PrivateMessageManager(models.Manager):		
	
	def unread_messages(self, user):
		return self.filter(receiver = user.id, has_read = False)
		
	def posted_messages(self, user):
		return self.filter(sender = user.id)
		
	def filter_messages(self, user, kind = 'all'):
		if kind == 'all':
			return list(user.private_message_sent.all()) + \
				list(user.private_message_received.all())
		elif kind == 'sent':
			return user.private_message_sent.all()
		elif kind == 'received':
			return user.private_message_received.all()
		else:
			return []

class PrivateMessage(jsonobj.JsonObjectModel):

	sender       = models.ForeignKey(User, related_name = 'private_message_sent')
	receiver     = models.ForeignKey(User, related_name = 'private_message_received')
	body_text    = models.TextField()
	created_time = models.DateTimeField(auto_now_add = True)
	attachments  = models.ManyToManyField(Attachment)
	has_read     = models.BooleanField(default = False)
	#Manager
	objects      = PrivateMessageManager()
	
	json_extra   = ['attachments']
	
	def __unicode__(self):
		return u'%s 给 %s 的私信。包含 %d 个附件。' % (
				self.sender.profile.nick_name, 
				self.receiver.profile.nick_name,
				len(self.attachments.all())
			)
	
	def mark_read(self, flag = True):
		self.has_read = flag
		self.save()

	def delete(self):
		self.notification.delete()
		super(PrivateMessage, self).delete()
		
	def shorten(self):
		if len(self.body_text)<10:
			return self.body_text
		else:
			return u'%s...' % self.body_text[:10]
			
	class Meta(jsonobj.JsonObjectModel.Meta):
		abstract = False
		verbose_name = u'私信'
		ordering = ['-created_time']