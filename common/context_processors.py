from kv import ChannelKV

def channel_url(request):
	if not request.user.is_authenticated():
		return {}
	kv = ChannelKV(request.user.id)
	return {"channel_url": kv.add_and_get_url()}