# -*- coding: cp936 -*-
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
	
	json_extra   = ['kind', 'url', 'message']
	
	objects      = NotificationManager()
	
	def __unicode__(self):
		return u'%s ��֪ͨ��' % self.receiver.profile.nick_name
		
	def url(self):                    #abstract
		pass
		
	def mark_read(self, flag = True):        #abstract
		self.has_read = flag
		self.save()
		
	def message(self):                #abstract
		pass
		
	def kind(self):                   #abstract
		pass
	
	class Meta(jsonobj.JsonObjectModel.Meta):
		abstract = True
		ordering = ['-created_time']
		verbose_name = u'֪ͨ'
		
class PrivateMessageNotification(Notification):

	private_message = models.OneToOneField(PrivateMessage, related_name = 'notification')
	
	def kind(self):
		return 'pm'
		
	def __unicode__(self):
		return u'%s ��˽��֪ͨ��' % self.receiver.profile.nick_name
		
	def url(self):
		return '/pm/%d/' % self.private_message.id
		
	def message(self):
		return u'%s ���㷢��һ��˽�ţ�%s' % (
				self.private_message.sender.profile.nick_name,
				self.private_message.shorten
			)
			
	class Meta(jsonobj.JsonObjectModel.Meta):
		abstract = False
		ordering = ['created_time']
		verbose_name = u'˽��֪ͨ'
	
class StatusNotification(Notification):
	
	CATEGORY_CHOICES = {
			'POSTED': u'����',
			'REJECTED': u'�ܾ���ɾ��',
			'VERIFIED': u'��֤',
			'DELETED':  u'ɾ��'
	}
	
	status   = models.ForeignKey(Status, related_name = 'notifications')
	category = models.CharField(max_length = 10, choices = [
						('POSTED',   u'����'),
						('REJECTED', u'�ܾ���ɾ��'),
						('VERIFIED', u'��֤'),
						('DELETED',  u'ɾ��'),
	])
	
	def kind(self):
		return 'status'
		
	def __unicode__(self):
		return u'%s �Ĺ���֪ͨ��' % self.receiver.profile.nick_name
		
	def url(self):
		return '/webboard/status/%d/' % self.status.id
		
	def message(self):
		if self.category == 'POSTED':
			return u'%s ������һ�����棬������֤��%s' % (
				self.status.author.profile.nick_name,
				self.status.shorten()
			)
		else:
			return u'����Ա%s����Ĺ��棺%s' % (
				self.CATEGORY_CHOICES[self.category],
				self.status.shorten()
			)

	class Meta(jsonobj.JsonObjectModel.Meta):
		abstract = False
		ordering = ['-created_time']
		verbose_name = u'����֪ͨ'
		
class CommentNotification(Notification):
	
	comment = models.OneToOneField(Comment, related_name = 'notification')
	
	def kind(self):
		return 'comment'
		
	def __unicode__(self):
		return u'%s ������֪ͨ��' % self.receiver.profile.nick_name
		
	def url(self):
		return '/webboard/status/%d/#%d' % (
			self.comment.status.id,
			self.comment.id,
		)
	
	def message(self):
		return u'%s ��������Ĺ��棺%s' % (
			self.comment.author.profile.nick_name,
			self.comment.shorten()
		)
		
	class Meta(jsonobj.JsonObjectModel.Meta):
		abstract = False
		ordering = ['-created_time']
		verbose_name = u'����֪ͨ'