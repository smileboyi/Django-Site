from django.shortcuts import render
from django.shortcuts import HttpResponse
from cmdb import models  # models和数据库相关

import time
import django.dispatch
from django.dispatch import receiver

from django.core import serializers
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def index(request):
  return HttpResponse('Welcome come to index page')


"""
# 创建一个用户信息列表，预定义2个数据(如果服务重启，那么数据就会回到原始状态)
user_list = [
  {"user":"jack", "pwd":"abc"},
  {"user":"tom", "pwd":"ABC"},
]
"""



# request参数必须有，名字是类似self的默认规则，可以改，它封装了用户请求的所有内容。
def cmdb(request):
  # request.POST,
  # request.GET

  # 不能直接返回字符串，必须是有这个类封装起来，这是django的规则，不是python的。
  # return HttpResponse('hello world!')

  # 如果有表单请求，先获取表单信息，然后返回一个页面（刷新）
  if request.method == "POST":
    username = request.POST.get('username',None)
    password = request.POST.get('password',None)

    # 将数据保存到数据库中
    models.UserInfo.objects.create(user=username,pwd=password)

    # 成功后返回给前端的消息
    messages.add_message(request, messages.INFO, 'create user : %s' % username, extra_tags='dragonball')
    # messages.info(request, 'create user : %s' % username, extra_tags='dragonball')

    """
    可以通过get_messages获取消息
    from django.contrib.messages import get_messages
    storage = get_messages(request)  存储后端的一个实例
    """

  # 从数据库中读取所有数据
  user_list = models.UserInfo.objects.all()

  # temp = {"user":username, "pwd":password}
  # user_list.append(temp)

  # 当你想返回一个html时，就用render方法
  # 第一个参数固定，第二个参数就是指定的文件,第三个参数是字典
  return render(request, 'cmdb/index.html',{"data": user_list})


# 序列化UserInfo模型数据
def cmdb_xml(request):
  data = serializers.serialize("xml", models.UserInfo.objects.all())
  # 通过网页源码查看xml
  return HttpResponse(data)


def user_show(request):
  user_list = models.UserInfo.objects.all()
  paginator = Paginator(user_list, 5) # 每页显示25条

  page = request.GET.get('page')
  try:
    # page()返回指定页面的对象列表,相当于querySet
    users = paginator.page(page)
  except PageNotAnInteger:
    # 如果请求的页数不是整数，返回第一页。
    users = paginator.page(1)
  except EmptyPage:
    # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
    users = paginator.page(paginator.num_pages)
  return render(request, 'cmdb/list.html', {'users': users})





  # 定义一个信号
work_done = django.dispatch.Signal(providing_args=['path', 'time'])


# 信号发送器，参数(sender, **kwargs)
def create_signal(request):
  url_path = request.path
  print("我已经做完了工作。现在我发送一个信号出去，给那些指定的接收器。")

  # 发送信号，将请求的url地址和时间一并传递过去
  work_done.send(create_signal, path=url_path, time=time.strftime("%Y-%m-%d %H:%M:%S"))
  return HttpResponse("200,ok")


#信号接收器  Signal.connect(receiver, sender=None, weak=True, dispatch_uid=None)[source]
@receiver(work_done, sender=create_signal)   #另一种写法：work_done.connect(signal_callback, sender=create_signal)
def signal_callback(sender, **kwargs):
  print("我在%s时间收到来自%s的信号，请求url为%s" % (kwargs['time'], sender, kwargs["path"]))

