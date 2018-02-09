from django.conf.urls import url
from . import views

app_name = 'login'
urlpatterns = [
	url(r'^index/$', views.index),
	url(r'^login/$', views.login),
	url(r'^register/$', views.register),
	url(r'^logout/$', views.logout),
	url(r'^confirm/$', views.user_confirm),
]