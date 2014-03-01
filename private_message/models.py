# -*- coding: cp936 -*-
from django.db import models
from common import jsonobj, kv
from wboard import settings
from django.contrib.auth.models import User

class Attachment(jsonobj.JsonObjectModel):
	
	url           = models.URLField()
	file_name     = models.CharField(max_length = 255)
	uploaded_time = models.DateTimeField(auto_now_add = True)
	
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
		if kind == '_all':
			return list(user.private_message_sent.all()) + \
				list(user.private_message_received.all())
		elif kind == 'sent':
			return user.private_message_sent.all()
		elif kind in ('all', 'received'):
			return user.private_message_received.all()
		elif kind == 'unread':
			return user.private_message_received.filter(has_read = False)
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
			
	def save(self, *args, **kw_args):
		super(PrivateMessage, self).save(*args, **kw_args)
		kv.ChannelKV(self.receiver).send_unread()
	
	def mark_read(self, flag = True):
		self.has_read = flag
		self.save()

	def delete(self):
		kv.ChannelKV(self.receiver).send_unread()
		super(PrivateMessage, self).delete()
		
	def shorten(self):
		if len(self.body_text)<10:
			return self.body_text
		else:
			return u'%s...' % self.body_text[:10]
			
	def message(self, user):
		result = {'message': self.body_text}
		result['attachments'] = '|'.join(('*'.join((i.url,i.file_name)) for i in self.attachments.all()))
		if user == self.sender:
			result['to'] = self.receiver.id
		else:
			result['from'] = self.sender.id
		result['id'] = self.id
		result['created_time'] = self.created_time.strftime(settings.JSON_DATETIME_FORMAT)
		return result
			
	class Meta(jsonobj.JsonObjectModel.Meta):
		abstract = False
		verbose_name = u'私信'
		ordering = ['-created_time']