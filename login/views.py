from django.shortcuts import render
from django.shortcuts import redirect
from . import models, forms
# Create your views here.

def index(request):
  
  return render(request, 'login/index.html')


"""
# 使用手工书写表单时对应的视图
def login(request):
  if request.method == "POST":
    # 从表单中获取数据（需要一个一个获取）
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
          # 重定向的url前面要加/
          return redirect('/login/index/')
        else:
          message = "密码不正确！"
      except:
        message = "用户名不存在！"
    # 登录失败，附上错误提示信息
    return render(request, 'login/login.html', {"message": message})
  # 渲染的url前面不加/
  return render(request, 'login/login.html')
"""

# 使用forms书写表单时对应的视图
def login(request):
  if request.method == "POST":
    # 因为表单元素是用forms生成的，所以从forms中获取数据（类实例）
    login_form = forms.UserForm(request.POST)
    message = "请检查填写的内容！"
    # 表单类自带的is_valid()检验数据（包括图片验证码）
    if login_form.is_valid():
      # 检验成功后就可以获取数据
      username = login_form.cleaned_data['username']
      password = login_form.cleaned_data['password']
      try:
        # 这里的逻辑和上面的一样
        user = models.User.objects.get(name=username)
        if user.password == password:
          return redirect('/login/index/')
        else:
          message = "密码不正确！"
      except:
        message = "用户不存在！"
    # locals：python内置函数，它返回当前所有的**本地变量**字典。
    # 类似于{'message':message, 'login_form':login_form}，但可能会出现多余的变量数据
    return render(request, 'login/login2.html', locals())

  login_form = forms.UserForm()
  return render(request, 'login/login2.html', locals())



def register(request):
  return render(request, 'login/register.html')


def logout(request):
  return redirect("login/index/")