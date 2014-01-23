from django.http import HttpResponse
from django.utils.encoding import iri_to_uri
from django.core.panginator import Paginator, EmptyPage, InvalidPage
from datetime import datetime
from wboard import settings
import exceptions

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
	return paginate(objects, object_per_page, page)
	
#get object
def get_object_by_id(cls, id):
	try:
		return cls.objects.get(id = int(id))
	except:
		return None
		
#file upload
def upload_file(request, field_name):
'''
	return format:
	(
		url : The URL of the file,
		name: File name
	)
'''
	import sae.storage
	client = sae.storage.Client()
	filename = datetime.now.strftime('%Y%m%d%H%M%s%f')
	file = request.FILES[field_name]
	obj = sae.storage.Object(file.read())
	url = client.put(settings.SAE_STORAGE_DOMAIN_NAME, obj)
	return (url, file.name)
	
#GET&POST
def to_callable(object_name):
	if callable(object_name):
		return object_name
	splitter = object_name.rfind('.')
	try:
		module_name = object_name[:splitter]
		mothod_name = object_name[splitter+1:]
		return getattr(__import__(module_name), method_name)
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