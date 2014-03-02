import common
from webboard.models import Status

@common.render_to('index.html')
def index(request):
	return {'hottest': Status.objects.filter(has_verified = True).order_by("-created_time")[:3]}