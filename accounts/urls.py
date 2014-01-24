from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

urlpatterns = patterns('accounts.views',
	(r'login/$', 'login'),
	(r'logout/$', 'logout'),
	(r'info/(\d+)/$', 'info'),
	(r'mf/$', 'make_friends'),
)