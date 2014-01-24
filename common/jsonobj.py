try:
    import json
except ImportError:
    from django.utils import simplejson as json
		
from django.db import models

class JsonObjectModel(models.Model):     #abstract

	def to_json(self):
		if not hasattr(self, 'objects'):
			self.objects = {attr.name: getattr(self, attr.name) for attr in self._meta.fields}
		return json.dumps(self.objects)
		
	def save(self, *args, **kw_args):
		del self.objects
		super(models.Model, self).save(*args, **kw_args)