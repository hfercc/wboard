from django.db import models
from django.contrib.auth.models import User

class StatusManager(models.Manager):
	
	def statuses(self, user):
		return self.filter(author = user.id)
		
	def verified_statuses(self, user = None):
		if user:
			return self.filter(author = user.id, has_verified = True)
		else:
			return self.filter(has_verified = True)

class Status(models.Model):
	
	title        = models.CharField(max_length = 255)
	body_text    = models.TextField()
	author       = models.ForeignKey(User, related_name = 'statuses')
	created_time = models.DateTimeField(auto_now_add = True)
	has_verified = models.BooleanField(default = False)

	#Manager
	objects      = StatusManager()
	
	def __unicode__(self):
		return unicode(title)
		
	def reject(self):
		self.delete()
		
	def verify(self):
		self.has_verified = True
		self.save()

	def delete(self):
		for notification in self.notifications:
			notification.delete()
		for comment in self.comments:
			comment.delete()
		super(Status, self).delete()
		
class CommentManager(models.Manager):

	def comments(self, user):
		return self.filter(author = user.id)
		
class Comment(models.Model):

	author           = models.ForeignKey(User, related_name = 'comments')
	body_text        = models.TextField()
	created_time     = models.DateTimeField(auto_now_add = True)
	status           = models.ForeignKey(Status, related_name = 'comments')
	
	#Manager
	objects          = CommentManager()
	
	def __unicode__(self):
		return unicode('%s\'s comment' % (self.author.get_profile().nick_name))
		
	def delete(self):
		self.notification.delete()
		super(Comment, self).delete()