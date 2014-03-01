import common
from common import exceptions, utils, kv
import sae
import json
from private_message import send_private_message
from wboard import settings

@common.ajax_request
def message(request):
	name = request.POST.get('from', '')
	msg = json.loads(request.POST.get('message', ''))
	pm = send_private_message(int(name.split('_')[0]), int(msg['to']), msg['message'], msg['attachments'])
	print pm
	kv.ChannelKV(msg['to']).send_message(pm.message(request.user))
	return {}
	
@common.ajax_request
def connected(request):
	name = request.POST.get('from', '')
	print 'connected', name
	id, s, chat = name.split('_')
	kv.ChannelKV(id).send_unread(name)
	return {}
	
@common.ajax_request
def disconnected(request):
	name = request.POST.get('from', '')
	print 'disconnected', name
	kv.ChannelKV(name.split('_')[0]).delete(name)
	return {}