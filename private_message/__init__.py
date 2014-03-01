import models
from models import PrivateMessage, Attachment
from django.contrib.auth.models import User
import notification

def send_private_message(sender, receiver, message, attachments = ''):
	if isinstance(sender, int):
		sender = User.objects.get(id = sender)
	if isinstance(receiver, int):
		receiver = User.objects.get(id = receiver)
	pm = PrivateMessage(sender = sender, receiver = receiver, body_text = message)
	pm.save()
	if attachments:
		for s in attachments.split("|"):
			url, file_name = s.split("*")
			attachment = Attachment(url = url, file_name = file_name)
			attachment.save()
			pm.attachments.add(attachment)
	return pm
	
# def send_private_message_and_notify(sender, receiver, message, attachments = []):
	# pm = send_private_message(sender, receiver, message)
	# if pm.sender != pm.receiver:
		# notification.send_notification(pm.receiver, 'pm', private_message = pm)
	# return pm