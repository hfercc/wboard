from django import forms
import models
from common import utils, exceptions

class StatusForm(forms.Form):

	title     = forms.CharField(max_length = 255)
	body_text = forms.CharField()
	
class CommentForm(forms.Form):

	body_text = forms.CharField()
	status_id = forms.IntegerField()
	
	def clean_status_id(self):
		try:
			self.status = utils.get_object_by_id(models.Status, self.cleaned_data.status_id)
		except exceptions.ObjectNoFound:
			raise forms.ValidationError('Cannot find the object!')