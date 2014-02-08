# -*- coding: cp936 -*-
from django.db import models
from django.contrib.auth.models import User
from common import jsonobj

class StatusManager(models.Manager):
	
	def statuses(self, user):
		return self.filter(author = user.id)
		
	def verified_statuses(self, user = None):
		if user:
			return self.filter(author = user.id, has_verified = True)
		else:
			return self.filter(has_verified = True)

class Status(jsonobj.JsonObjectModel):
	
	title        = models.CharField(max_length = 255)
	body_text    = models.TextField()
	author       = models.ForeignKey(User, related_name = 'statuses')
	created_time = models.DateTimeField(auto_now_add = True)
	has_verified = models.BooleanField(default = False)

	#Manager
	objects      = StatusManager()
	
	json_extra   = ['comments']
	
	def __unicode__(self):
		return unicode(self.title)
		
	def reject(self):
		self.delete()
		
	def verify(self):
		self.has_verified = True
		self.save()

	def delete(self):
		for notification in self.notifications.all():
			if notification.category != 'DELETED':
				notification.delete()
		for comment in self.comments.all():
			comment.delete()
		super(Status, self).delete()
		
	def shorten(self):
		if len(self.body_text)<10:
			return self.body_text
		else:
			return u'%s...' % self.body_text[:10]
		
	class Meta:
		permissions = (
				('post', 'Can post statuses'),
				('verify', 'Can verify statuses'),
				('delete_modify', 'Can delete or modify statuses'),
				('comment', 'Can comment statuses'),
			)
		verbose_name = u'公告'
		ordering = ['-created_time']
		
class CommentManager(models.Manager):

	def comments(self, user):
		return self.filter(author = user.id)
		
class Comment(jsonobj.JsonObjectModel):

	author           = models.ForeignKey(User, related_name = 'comments')
	body_text        = models.TextField()
	created_time     = models.DateTimeField(auto_now_add = True)
	status           = models.ForeignKey(Status, related_name = 'comments')
	
	#Manager
	objects          = CommentManager()
	
	json_filters     = ['status']
	
	def __unicode__(self):
		return unicode('%s\'s comment' % (self.author.profile.nick_name))
		
	def delete(self):
		self.notification.delete()
		super(Comment, self).delete()
		
	def shorten(self):
		if len(self.body_text)<10:
			return self.body_text
		else:
			return u'%s...' % self.body_text[:10]
			
	class Meta:
		verbose_name = u'评论'
		ordering = ['created_time']