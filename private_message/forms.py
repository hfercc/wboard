from django import forms
from common import utils, exceptions
from django.contrib.auth.models import User
import models

class PrivateMessageForm(forms.Form):
	
	body_text  = forms.CharField()
	receivers  = forms.CharField()
	attachment = forms.CharField()
	
	def _get_users_received(self):
		try:
			return [User.objects.get(username = name) for name in self.cleaned_data.receivers.split('|')]
		except:
			raise exceptions.DataFieldMissed
	
	def _get_attachments(self):
		try:
			return self.__attachments
		except:
			self.__attachments = []
		for attachment in self.cleaned_data.attachment.split('|'):
			url, file_name = attachment.split('*')
			a = models.Attachment(url = url, file_name = file_name)
			a.save()
			self.__attachments += [a]
	
	users_received = property(_get_users_received)
	attachments    = property(_get_attachments)