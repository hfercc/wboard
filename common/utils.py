from django.http import HttpResponse
from django.utils.encoding import iri_to_uri
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from datetime import datetime
from wboard import settings
from django.http import Http404
import exceptions
import sys

class HttpResponseReload(HttpResponse):
    """
    Reload page and stay on the same page from where request was made.

    example:

    def simple_view(request):
        if request.POST:
            form = CommentForm(request.POST):
            if form.is_valid():
                form.save()
                return HttpResponseReload(request)
        else:
            form = CommentForm()
        return render_to_response('some_template.html', {'form': form})
    """
    status_code = 302

    def __init__(self, request):
        HttpResponse.__init__(self)
        referer = request.META.get('HTTP_REFERER')
        self['Location'] = iri_to_uri(referer or "/")

#reflect

def datetime_processor(obj):
	if isinstance(obj, datetime):
		print obj
		return obj.strftime(settings.JSON_DATETIME_FORMAT)
		
def many_related_processor(obj):
	if 'RelatedManager' in obj.__class__.__name__:
		return obj.all()

def get_attributes(obj, attrs, filters = [], attr_name = '', processors = []):
	
	def get_attr_name(attr):
		if not attr_name:
			return attr
		else:
			return getattr(attr, attr_name)

	result = {}
	for attr in attrs:
		name = get_attr_name(attr)
		if name in filters:
			continue
		a = getattr(obj, name)
		result[name] = a() if callable(a) else a
		for processor in processors:
			process_result = processor(result[name])
			if process_result is not None:
				result[name] = process_result
	return result				
				
def get_model_fields(obj):
	return [attr.name for attr in obj._meta.local_fields]

#Paginate				

def paginate(objects, objects_per_page = 20, page = 1):
	p = Paginator(objects, objects_per_page)
	try:
		objs = p.page(page)
	except (EmptyPage, InvalidPage):
		objs = p.page(p.num_pages)
	return objs
	
def paginate_by_request(objects, request, objects_per_page = 20):
	try:
		page = int(request.GET.get('page',1))
	except ValueError:
		page = 1
	try:
		objects_per_page = int(request.GET.get('limit','') or request.POST.get('limit',''))
	except:
		pass
	return paginate(objects, objects_per_page, page)
	
def paginate_to_dict(objects, request, objects_per_page = 20, ajax_by_request = True, is_ajax = True):
	page = paginate_by_request(objects, request, objects_per_page)
	if ajax_by_request:
		ajax = request.method == 'POST'
	else:
		ajax = is_ajax
	if not ajax:
		return {'objects': page}
	response = {'objects': page.object_list}
	response.update(get_attributes(page, ['has_next', 'has_previous',
		 'number'], attr_name = ''))
	return response
	
#get object
def get_object_by_id(cls, id, raise_404 = False, method = ''):
	try:
		return cls.objects.get(id = int(id))
	except:
		if method:
			raise_404 = method == 'GET'
		if raise_404:
			raise Http404
		else:
			raise exceptions.ObjectNoFound
		
#file upload
def upload_file(request, field_name):
	'''
	return format:
	(
		url : The URL of the file,
		name: File name
	)
	'''
	# import sae.storage
	# client = sae.storage.Client()
	# filename = datetime.now.strftime('%Y%m%d%H%M%s%f')
	# file = request.FILES[field_name]
	# obj = sae.storage.Object(file.read())
	# url = client.put(settings.SAE_STORAGE_DOMAIN_NAME, obj)
	# return (url, file.name)
	import sae.storage
	bucket = sae.storage.Bucket('t')
	filename = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
	file = request.FILES[field_name]
	bucket.put_object(filename, file)
	url = bucket.generate_url(filename)
	return (url, file.name)
	
#GET&POST
def to_callable(object_name):
	if callable(object_name):
		return object_name
	splitter = object_name.rfind('.')
	try:
		module_name = object_name[:splitter] if splitter>=0 else ''
		method_name = object_name[splitter+1:]
		if splitter >= 0:
			method = getattr(__import__(module_name, fromlist = [1]), method_name)
		else:
			method = getattr(sys.modules[__name__], method_name)
		print method 
		return method
	except ImportError:
		raise exceptions.MethodError, 'Module name error.'
	except AttributeError:
		raise exceptions.MethodError, 'Method name error.'

def views_splitter(request, **kw_args):
	get = kw_args.pop('GET', '')
	post = kw_args.pop('POST', '')
	if get and request.method == 'GET':
		return to_callable(get)(request, **kw_args)
	elif post and request.method == 'POST':
		return to_callable(post)(request, **kw_args)
	else:
		raise exceptions.MethodError
		
def verify_user(request, users):
	try:
		iter(users)
	except:
		users = [users]
	if not filter(lambda user: request.user == user, users):
		raise exceptions.AccessDenied