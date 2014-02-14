from django.conf.urls import patterns, include, url

urlpatterns = patterns('webboard.views',
	(r'comment/list/$',         'comment_list'),
	(r'list/$',                 'status_list'),
	(r'verify/(\d+)/$',         'verify'),
	(r'modify/(\d+)/$',         'modify'),
	(r'comment/add/$',          'add_comment'),
	(r'comment/delete/(\d+)/$', 'delete_comment'),
	(r'delete/(\d+)/$',         'delete'),
	(r'add/$',                  'add'),
	(r'(\d+)/$',                'detail'),
)