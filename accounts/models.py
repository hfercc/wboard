# -*- coding: cp936 -*-
from common import JsonObjectModel, fields, jsonobj, utils, exceptions
from django.db import models
from django.contrib.auth.models import User

class UserProfile(jsonobj.JsonObjectModel):

	user      = fields.AutoOneToOneField(User, related_name = 'profile', primary_key = True)
	nick_name = models.CharField(max_length = 255, unique = True, blank = True)
	friends   = models.ManyToManyField(User, blank = True, related_name = 'friends_profile')
	
	json_filters = ['user']
	json_extra = ['is_friend__request']
	
	def is_friend__request(self, request):
		user = request.user
		if not user.is_authenticated():
			raise exceptions.AuthenticatedFailed
		else:
			return self.user in user.profile.friends.all()
	
	def __unicode__(self):
		return u'%s的个人信息。' % self.nick_name
		
	def get_json_object(self, request):
		super(UserProfile, self).get_json_object(request)
		self.objects.update(
			utils.get_attributes(
					self.user, 
					self.user._meta.fields, 
					['password','email','first_name','last_name','is_active','is_superuser'], 
					'name',
					[utils.datetime_processor],
					request
			)
		)
		return self.objects
		
	class Meta(jsonobj.JsonObjectModel.Meta):
		abstract = False
		verbose_name = u'用户信息'