from django.contrib import admin
# 引入应用的models
from .models import Question   

# Register your models here.

# 将models注册到站点进行管理
admin.site.register(Question)