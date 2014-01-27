import common

@common.render_to('test.html')
def index(request):
	return {}