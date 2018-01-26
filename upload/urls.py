from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^register/$', views.registerNormalUser),
  url(r'^uploadFile/$', views.upload_file),
  
]