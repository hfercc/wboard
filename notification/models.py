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
		return u'%s 的通知。' % self.receiver.profile.nick_name
		
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
		verbose_name = u'通知'
		
class PrivateMessageNotification(Notification):

	private_message = models.OneToOneField(PrivateMessage, related_name = 'notification')
	
	def kind(self):
		return 'pm'
		
	def __unicode__(self):
		return u'%s 的私信通知。' % self.receiver.profile.nick_name
		
	def url(self):
		return '/pm/%d/' % self.private_message.id
		
	def message(self):
		return u'%s 给你发了一条私信：%s' % (
				self.private_message.sender.profile.nick_name,
				self.private_message.shorten
			)
			
	class Meta(jsonobj.JsonObjectModel.Meta):
		abstract = False
		ordering = ['created_time']
		verbose_name = u'私信通知'
	
class StatusNotification(Notification):
	
	CATEGORY_CHOICES = {
			'POSTED': u'发布',
			'REJECTED': u'拒绝并删除',
			'VERIFIED': u'认证',
			'DELETED':  u'删除'
	}
	
	status   = models.ForeignKey(Status, related_name = 'notifications')
	category = models.CharField(max_length = 10, choices = [
						('POSTED',   u'发布'),
						('REJECTED', u'拒绝并删除'),
						('VERIFIED', u'认证'),
						('DELETED',  u'删除'),
	])
	
	def kind(self):
		return 'status'
		
	def __unicode__(self):
		return u'%s 的公告通知。' % self.receiver.profile.nick_name
		
	def url(self):
		return '/webboard/status/%d/' % self.status.id
		
	def message(self):
		if self.category == 'POSTED':
			return u'%s 发布了一条公告，请求认证：%s' % (
				self.status.author.profile.nick_name,
				self.status.shorten()
			)
		else:
			return u'管理员%s了你的公告：%s' % (
				self.CATEGORY_CHOICES[self.category],
				self.status.shorten()
			)

	class Meta(jsonobj.JsonObjectModel.Meta):
		abstract = False
		ordering = ['-created_time']
		verbose_name = u'公告通知'
		
class CommentNotification(Notification):
	
	comment = models.OneToOneField(Comment, related_name = 'notification')
	
	def kind(self):
		return 'comment'
		
	def __unicode__(self):
		return u'%s 的评论通知。' % self.receiver.profile.nick_name
		
	def url(self):
		return '/webboard/status/%d/#%d' % (
			self.comment.status.id,
			self.comment.id,
		)
	
	def message(self):
		return u'%s 评论了你的公告：%s' % (
			self.comment.author.profile.nick_name,
			self.comment.shorten()
		)
		
	class Meta(jsonobj.JsonObjectModel.Meta):
		abstract = False
		ordering = ['-created_time']
		verbose_name = u'评论通知'