from django.conf.urls import patterns, include, url

urlpatterns = patterns('notification.views',
	(r'list/(comment|status|pm)/$', 'notifications_list'),                    
	(r'delete/(comment|status|pm)/(\d+)/$', 'delete'),                
	(r'(comment|status|pm)/(\d+)/$', 'detail'),
)