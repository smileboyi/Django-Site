import datetime
from django.db import models
# Django推荐使用timezone.now()代替python内置的datetime.datetime.now()
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

# 运行python manage.py makemigrations为改动创建迁移记录；
# 运行python manage.py migrate，将操作同步到数据库。
# github不和数据库直接打交道，也没法和你本地的数据库通信。但是分开之后，你只需要将你的migration文件（例如上面的0001）上传到github，它就会知道一切。


# Create your models here.
# 模型对应数据表，类变量对应字段，类实例对应一行数据
@python_2_unicode_compatible 
class Question(models.Model):
  # 每一个字段都是Field类的一个实例
  question_text = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date published')

  # <Question: Question object>是一个不可读的内容展示，你无法从中获得任何直观的信息
  # 定义一个打印的方法，之后不用通过question_text字段，会字节展示出来
  def __str__(self): 
    return self.question_text

  # 用于判断问卷是否最近时间段内发布度的
  def was_published_recently(self):
    return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

# python_2_unicode_compatible 会自动做一些处理去适应python不同的版本，以便有更好地兼容性。 
@python_2_unicode_compatible   # 当你想支持python2版本的时候才需要这个装饰器
class Choice(models.Model):
  # 定义外键，每一个Choice关联到一个对应的Question
  question = models.ForeignKey(Question, on_delete = models.CASCADE)
  choice_text = models.CharField(max_length=200)
  votes = models.IntegerField(default=0)

  def __str__(self):    # 在python2版本中使用的是__unique__
    return self.choice_text