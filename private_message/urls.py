from django.conf.urls import patterns, include, url

urlpatterns = patterns('private_message.views',
	(r'list/$',   'private_message_list'),
	(r'delete/(\d+)/$', 'delete'),
	(r'(\d+)/$',  'detail'),
) + patterns('common.utils',
	(r'write/$',        'views_splitter', {
		'GET':  'private_message.views.write_get',
		'POST': 'private_message.views.write_post',
	}),
)