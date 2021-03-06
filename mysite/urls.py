"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
# 可以使用这个类快速构建网站地图
# from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from polls.sitemaps import PollsSitemap, VoteSitemap
from polls.models import Question
#导入对应app的views文件
from cmdb import views


sitemaps={
	'polls': PollsSitemap,
	'vote': VoteSitemap
}

urlpatterns = [

	path(r'', views.index),
	# url(r'^$', views.index),

	##### cmdb #####
	# admin后台的路由(直接导入视图函数)
	# 如果是一级路由，前面加上^
	path(r'cmdb/', views.cmdb),
	path(r'cmdb/xml', views.cmdb_xml),
	path(r'cmdb/listing', views.user_show),

	##### polls #####
	# 分发（使用include）到二级路由上（上级到下级的匹配顺序）
	url(r'^polls/', include('polls.urls')),

	##### admin doc #####
	# pip3 install docutils
	url(r'^polls/set/doc/',include('django.contrib.admindocs.urls')),


	# 管理站点，使用前先python manage.py createsuperuser，创建一个管理者
	# 一般不会使用简单的管理站点url，不要太暴露
	# url(r'^admin/', admin.site.urls),
	# 使用别人不容易猜到的url
	url(r'^mysite/set/', admin.site.urls),


	##### upload #####
	url(r'^upload/', include('upload.urls')),


	##### login #####
	url(r'^login/', include('login.urls')),
	

	##### snippets #####
	url(r'^snippets/', include('snippets.urls')),


	##### sitemap #####
	# 当用户访问/sitemap.xml时，Django将生成并返回一个网站地图。
	# 如果sitemap.xml位于根目录中，它会引用网站中的任何URL。 但是如果站点地图位于/content/sitemap.xml，则它只能引用以/content/开头的网址。
	url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap'),


	##### sitemap #####
	# 信号视图
	url(r'^signal/$', views.create_signal),

	##### captcha #####
	url(r'^captcha', include('captcha.urls'))
]



