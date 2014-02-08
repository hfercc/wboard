from django.conf.urls import patterns, include, url

urlpatterns = patterns('notification.views',
	(r'list/$', 'notifications_list'),                    
	(r'delete/(\d+)/$', 'delete'),                
	(r'(\d+)/$', 'detail'),
)