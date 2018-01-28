from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^register/$', views.registerNormalUser),
  url(r'^uploadFile/$', views.upload_file),
  url(r'^csv/$', views.csv_view),
  url(r'^csv2/$', views.csv_view2),
  url(r'^pdf/$', views.pdf_view),
  url(r'^pdf2/$', views.pdf_view2),
  
]