from common import utils#, exceptions
import common
import sae
from django.contrib.auth.models import User
from wboard.settings import CHANNEL_NAME_SPLITTER

@common.login_required
@common.method('POST')
@common.ajax_request
def upload(request):
	try:
		url, file_name = utils.upload_file(request, 'file')
		return {'status': 'success',
						'url':    url,
						'file_name': file_name}
	except:
		raise common.exceptions.FileUploadFailed
		
@common.login_required
@common.method('POST')
@common.ajax_request
def chat_start(request):
	user = utils.get_object_by_id(User, request.POST.get('user_id',''))
	name = '%s%s%s' % (
			request.user.username, 
			CHANNEL_NAME_SPLITTER, 
			user.username
		)
	url = sae.channel.create_channel(name)
	return {'url': url}