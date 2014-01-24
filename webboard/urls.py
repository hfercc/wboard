from django.conf.urls import patterns, include, url

urlpatterns = patterns('webboard.views',
	(r'list/$',                 'status_list'),
	(r'(\d+)/$',                'detail'),
	(r'add/$',                  'add'),
	(r'modify/(\d+)/$',         'modify'),
	(r'verify/(/d+)/$',         'verify'),
	(r'comment/add/$',          'add_comment'),
	(r'comment/delete/(\d+)/$', 'delete_comment'),
) + patterns('',
	(r'delete/(\d+)/$',         'common.utils.views_splitter', {
			'GET':  'webboard.views.delete_get',
			'POST': 'webboard.views.delete_post'
		}
	)
)