from django.db import models

# Create your models here.


# 要继承这个models.Model类，固定写法
class UserInfo(models.Model):
  # 创建2个字段，类型为char,最大长度32
  user = models.CharField(max_length=32)
  pwd = models.CharField(max_length=32)
