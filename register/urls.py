from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^register/$',views.register_page),
	url(r'official/$', views.official_panel),
	url(r'official/lookonall/$', views.official_show_all),
	url(r'official/lookonnonactual/$', views.official_show_non_actual),
	url(r'overview/(?P<what_choosed>\d{1})/$', views.overview, name='overview'),
	url(r'ovw/$', views.overview_panel),
	url(r'ovw/myoverviews/$', views.show_my_overview),
	url(r'^login/$',views.user_login),
    	url(r'^logout/$',views.logout_page),
	url(r'^moveto/$',views.moveto),
	url(r'^logout/$',views.user_logout)
]
