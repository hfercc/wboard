from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
	(r'login/$', login),
	(r'logout/$', logout),
	(r'info/(\d+)/$', 'accounts.views.info'),
	(r'mf/$', 'accounts.views.make_friends'),
)