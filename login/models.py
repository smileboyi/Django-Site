from django.db import models

# Create your models here.

# 使用sqlite3数据库

class User(models.Model):
  genter = (
    ('male', '男'),
    ('femals', '女'),
  )
  name = models.CharField(max_length=128, unique=True)
  password = models.CharField(max_length=256)
  email = models.EmailField(unique=True)
  sex = models.CharField(max_length=32, choices=genter, default='男')
  c_time = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name

  class Meta:
    ordering = ["-c_time"]
    verbose_name = "用户"
    verbose_name_plural = "用户"