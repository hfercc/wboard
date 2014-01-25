import models
from models import PrivateMessage, Attachment
import notification

def send_private_message(sender, receiver, message, attachments = []):
	if isinstance(sender, str):
		sender = User.objects.get(username = sender)
	if isinstance(receiver, str):
		receiver = User.objects.get(username = receiver)
	pm = PrivateMessage(sender = sender, receiver = receiver, body_text = message)
	for attachment in attachments:
		pm.attachments.add(attachment)
	pm.save()
	return pm
	
def send_private_message_and_notify(sender, receiver, message, attachments = []):
	pm = send_private_message(sender, receiver, message)
	notification.send_notification(pm.receiver, 'pm', private_message = pm)
	return pm