from django.shortcuts import render
from django.shortcuts import redirect
from . import models
# Create your views here.

def index(request):
  
  return render(request, 'login/index.html')


def login(request):
  if request.method == "POST":
    # 获取数据
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    message = "所有字段都必须填写！"
    # 验证用户
    if username and password:
      username = username.strip()
      # 用户是否存在
      try:
        user = models.User.objects.get(name=username)
        # 用户密码是否正确
        if user.password == password:
          return redirect('login/index/')
        else:
          message = "密码不正确！"
      except:
        message = "用户名不存在！"
    # 登录失败，附上错误提示信息
    return render(request, 'login/login.html', {"message": message})
  # 成功登录
  return render(request, 'login/index.html')


def register(request):
  return render(request, 'login/register.html')


def logout(request):
  return redirect("login/index/")