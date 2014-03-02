from django.conf.urls import patterns, include, url

urlpatterns = patterns('chat.views',
	('message$', 'message'),
    ('disconnected$', 'disconnected'),
	('connected$', 'connected'),
)