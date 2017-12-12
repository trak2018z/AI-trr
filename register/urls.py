from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'official/$', views.official, name='official'),
	url(r'overview/(?P<what_choosed>\d{1})/$', views.overview, name='overview'),
]
