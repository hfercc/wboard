from django.conf.urls import patterns, include, url

urlpatterns = patterns('sae_support.views',
	(r'upload/$',  'upload'),
)