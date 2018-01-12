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

#导入对应app的views文件
from cmdb import views    

urlpatterns = [
    # '''
    # cmdb
    # '''

    # admin后台的路由(直接导入视图函数)
    path(r'cmdb/', views.index),
    

    # '''
    # polls
    # '''

    # 分发（使用include）到二级路由上（上级到下级的匹配顺序）
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
]
