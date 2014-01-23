from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

	nick_name = models.CharField(max_length = 255, unique = True)
	friends   = models.ManyToManyField(User)
	user      = models.OneToOneField(User, related_name = 'user')
	
	def __unicode__(self):
		return '%s\'sprofile.' % user.username