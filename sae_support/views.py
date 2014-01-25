from common import utils#, exceptions
import common

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
		pass#raise common.exceptions.FileUploadFailed