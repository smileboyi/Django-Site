from django.conf.urls import url
from . import views

app_name = 'login'
urlpatterns = [
	# 使用类视图形式
	# url(r'^$', views.IndexView.as_view(), name='index'),
]