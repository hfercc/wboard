from common import JsonObjectModel, fields, jsonobj, utils
from django.db import models
from django.contrib.auth.models import User

class UserProfile(jsonobj.JsonObjectModel):

	user      = fields.AutoOneToOneField(User, related_name = 'profile', primary_key = True)
	nick_name = models.CharField(max_length = 255, unique = True, blank = True)
	friends   = models.ManyToManyField(User, blank = True, related_name = 'friends_profile')
	
	json_filters = ['user']
	
	def __unicode__(self):
		return '%s\'sprofile.' % self.user.username
		
	def get_json_object(self):
		super(UserProfile, self).get_json_object()
		self.objects.update(
			utils.get_attributes(
					self.user, 
					self.user._meta.fields, 
					['password','email','first_name','last_name','is_active','is_superuser'], 
					'name',
					[utils.datetime_processor]
			)
		)
		return self.objects