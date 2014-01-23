from django.conf.urls import patterns, include, url

urlpatterns = patterns('private_message.views',
	(r'list/$',   'private_message_list'),
	(r'(\d+)/$',  'detail'),
) + patterns('common.utils',
	(r'delete/(\d+)/$', 'views_splitter', {
		'GET':  'private_message.views.delete_get',
		'POST': 'private_message.views.delete_post'
	}),
	(r'write/$',        'views_splitter', {
		'GET':  'private_message.views.write_get',
		'POST': 'private_message.views.write_post',
	}),
)