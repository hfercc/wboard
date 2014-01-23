class Redirect(Exception):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

class MethodError(Exception):
	pass
	
class AjaxError(Exception):
	
	error = {'code': 0, 'error': ''}
	
class ObjectNoFound(AjaxError):
	
	error = {'code': 1, 'error': 'Object no found!'}
	
class DataFieldMissed(AjaxError):

	error = {'code': 2, 'error': 'Data Field(s) missed!'}
	
class AccessDenied(AjaxError):

	error = {'code': 3, 'error': 'Access denied!'}
	
class FileUploadFailed(AjaxError):

	error = {'code': 4, 'error': 'File upload failed!'}