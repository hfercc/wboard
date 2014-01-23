from django import forms
import models
from common import utils

class StatusForm(forms.Form):

	title     = forms.CharField(max_length = 255)
	body_text = forms.CharField()
	
class CommentForm(forms.Form):

	body_text = forms.CharField()
	status_id = forms.IntegerField()
	
	def _get_status(self):
		try:
			return self.__status
		except AttributeError:
			self.__status = utils.get_object_by_id(models.Status, self.cleaned_data.status_id)
			return __status
		
	status = property(_get_status)