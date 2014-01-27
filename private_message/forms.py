from django import forms
from common import utils, exceptions
from django.contrib.auth.models import User
import models

class PrivateMessageForm(forms.Form):
	
	body_text  = forms.CharField()
	receivers  = forms.CharField()
	attachment = forms.CharField(required = False)
	
	def clean_receivers(self):
		try:
			self.users_received = [User.objects.get(username = name) for name in  \
				self.cleaned_data['receivers'].split('|')]
		except:
			raise forms.ValidationError('Cannot find the object!')
		return self.cleaned_data['receivers']
		
	def clean_attachment(self):
		self.attachments = []
		data = self.cleaned_data.get('attachment', '')
		if not data:
			return data
		try:
			for attachment in data.split('|'):
				url, file_name = attachment.split('*')
				a = models.Attachment(url = url, file_name = file_name)
				a.save()
				self.attachments += [a]
		except:
			raise forms.ValidationError('Cannot find the attachment!')
		return data