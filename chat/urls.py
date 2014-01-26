from django.conf.urls import patterns, include, url

urlpatterns = patterns('views',
	('message$', 'message'),
	('connected$', 'connected'),
	('disconnected$', 'disconnected'),
)