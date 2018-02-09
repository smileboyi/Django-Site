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
  has_confirmed = models.BooleanField(default=False)

  def __str__(self):
    return self.name

  class Meta:
    ordering = ["-c_time"]
    verbose_name = "用户"
    verbose_name_plural = "用户"


"""
User模型新增了has_confirmed字段，这是个布尔值，默认为False，也就是未进行邮件注册；
ConfirmString模型保存了用户和注册码之间的关系，一对一的形式；
code字段是哈希后的注册码；
user是关联的一对一用户；
c_time是注册的提交时间。
"""
# 邮件确认注册需要一张表单独存放便于管理，而不是放在user表中
class ConfirmString(models.Model):
  code = models.CharField(max_length=256)
  user = models.OneToOneField('User', on_delete=models.CASCADE,)
  c_time = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.user.name + ":   " + self.code

  class Meta:
    ordering = ["-c_time"]
    verbose_name = "确认码"
    verbose_name_plural = "确认码"