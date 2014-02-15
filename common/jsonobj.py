try:
    import json
except ImportError:
    from django.utils import simplejson as json
		
from datetime import datetime
from copy import deepcopy
from django.db import models
from wboard import settings
import utils

class JsonObjectModel(models.Model):     #abstract

	json_filters = []
	json_extra   = []

	def get_json_object(self, request):
		if not hasattr(self, 'objects'):
			attrs = utils.get_model_fields(self)
			attrs.extend(self.json_extra)
			self.objects = utils.get_attributes(
				self, 
				attrs, 
				self.json_filters, 
				processors = [utils.datetime_processor, utils.many_related_processor],
				request = request
			)
		return self.objects
		
	def to_json(self):	
		if hasattr(self, 'json'):
			return self.json
		else:
			self.json = json.dumps(self.objects)
			return self.json
		
	def save(self, *args, **kw_args):
		if hasattr(self, 'objects'):
			del self.objects
		super(JsonObjectModel, self).save(*args, **kw_args)
		
	class Meta:
		abstract = True
		
is_user_instance = lambda x: x.__class__.__name__ == 'User' \
	and x.__class__.__module__ == 'django.contrib.auth.models'		
		
def serialize_models(obj, request):

	if isinstance(obj, JsonObjectModel):
		obj = obj.get_json_object(request)
	elif isinstance(obj, models.query.QuerySet):
		obj = list(obj)
	elif is_user_instance(obj):
		return obj.profile.get_json_object(request)

	if isinstance(obj, dict):
		iter_object = obj
	elif isinstance(obj, (list, tuple)):
		iter_object = range(len(obj))
	else:
		return obj
		
	new_obj = deepcopy(obj)
	
	for key in iter_object:
		if hasattr(new_obj[key], 'get_json_object'):
			new_obj[key] = new_obj[key].get_json_object(request)
		elif isinstance(new_obj[key], models.query.QuerySet):
			new_obj[key] = list(new_obj[key])
		elif is_user_instance(new_obj[key]):
			new_obj[key] = new_obj[key].profile.get_json_object(request)
		if isinstance(new_obj[key], (list, dict, tuple)):
			new_obj[key] = serialize_models(new_obj[key], request)
			
	return new_obj