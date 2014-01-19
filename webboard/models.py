from django.db import models
from django.contrib.auth.models import User

class Status(models.Model):
	
	title        = models.CharField(max_length = 100)
	body_text    = models.TextField()
	author       = models.ForeignKey(User)
	created_time = models.DateTimeField()
	has_verified = models.BooleanField()

	def __unicode__(self):
		return unicode(title)

class Comment(models.Model):

	author           = models.ForeignKey(User)
	body_text        = models.TextField()
	created_time     = models.DateTimeField()
	status           = models.ForeignKey(Status)
	
	def __unicode__(self):
		return unicode('%s\'s comment' % (self.author.first_name))