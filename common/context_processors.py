import kv
from kv import ChannelKV
#kv.kv.set("1","")
def channel_url(request):
	print "referer",request.META.get("HTTP_REFERER","")
	if not request.user.is_authenticated() or request.method == 'POST' or "admin" in request.META["PATH_INFO"] or request.META.get("HTTP_REFERER", "") == request.META["PATH_INFO"]:
		return {}
	chat = 'pm/chat' in request.META['PATH_INFO']
	kv = ChannelKV(request.user.id)
	return {"channel_url": kv.add(chat)}