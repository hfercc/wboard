import common
from common import exceptions, utils
import sae
from private_message import send_private_message
from wboard import settings

@common.ajax_request
def message(request):
	name = request.POST.get('from', '')
	sender, receiver = name.split(name, settings.CHANNEL_NAME_SPLITTER)
	msg = request.POST.get('message', '')
	send_private_message(sender, receiver, msg)
	to_name = '%s%s%s' % (receiver, settings.CHANNEL_NAME_SPLITTER, sender)
	sae.channel.send_message(to_name, msg)
	return {}
	
@common.ajax_request
def connected(request):
	return {}
	
@common.ajax_request
def disconnected(request):
	return {}