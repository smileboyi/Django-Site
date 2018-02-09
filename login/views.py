from django.shortcuts import render
from django.shortcuts import redirect
from . import models, forms
import datetime
import hashlib  # 密码加密
from django.conf import settings


# Create your views here.

# 哈希加密
def hash_code(s, salt='mysite'):
  h = hashlib.sha256()  # sha256算法
  s += salt             # 加点盐
  h.update(s.encode())  # update方法只接收bytes类型
  return h.hexdigest()

#　注册确认码
def make_confirm_string(user):
  now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  code = hash_code(user.name, now)
  models.ConfirmString.objects.create(code=code, user=user,)
  return code

# 发送邮件给注册用户
def send_email(email, code):
  from django.core.mail import EmailMultiAlternatives

  subject = '来自www.liujiangblog.com的注册确认邮件'
  text_content = '''感谢注册www.liujiangblog.com，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！\
                  如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''
  html_content = '''
                  <p>感谢注册<a href="http://{}/login/confirm/?code={}" target=blank>www.liujiangblog.com</a>，\
                  这里是刘江的博客和教程站点，专注于Python和Django技术的分享！</p>
                  <p>请点击站点链接完成注册确认！</p>
                  <p>此链接有效期为{}天！</p>
                  '''.format('127.0.0.1:8080', code, settings.CONFIRM_DAYS)
  msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
  msg.attach_alternative(html_content, "text/html")
  msg.send()




def index(request):
  return render(request, 'login/index.html')



"""
# 使用手工书写表单时对应的视图
def login(request):
  # 用户是否登录，防止用户重复登录
  if request.session.get('is_login',None):
    return redirect("/login/index/")

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
          # 登录成功设置会话
          request.session['is_login'] = True
          request.session['user_id'] = user.id
          request.session['user_name'] = user.name
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
  if request.session.get('is_login',None):
    return redirect("/login/index/")

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
        
        if not user.has_confirmed:
          message = "该用户还未通过邮件确认！"
          return render(request, 'login/login.html', locals())

        if user.password == hash_code(password):
          # 登录成功设置会话
          request.session['is_login'] = True
          request.session['user_id'] = user.id
          request.session['user_name'] = user.name
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
  if request.session.get('is_login',None):
    return redirect("/login/index/")

  if request.method == "POST":
    register_form = forms.RegisterForm(request.POST)
    message = "请检查填写的内容！"
    if register_form.is_valid():  # 验证数据正确性
      username = register_form.cleaned_data['username']
      password1 = register_form.cleaned_data['password1']
      password2 = register_form.cleaned_data['password2']
      email = register_form.cleaned_data['email']
      sex = register_form.cleaned_data['sex']

      # 验证数据关联性（注意验证顺序，先验证满足注册的基本条件，再验证重复和唯一的条件）
      if password1 != password2:  # 判断两次密码是否相同
        message = "两次输入的密码不同！"
        return render(request, 'login/register.html', locals())
      else:
        same_name_user = models.User.objects.filter(name=username)
        if same_name_user:  # 用户名唯一
          message = '用户已经存在，请重新选择用户名！'
          return render(request, 'login/register.html', locals())

        same_email_user = models.User.objects.filter(email=email)
        print(same_email_user)
        if same_email_user:  # 邮箱地址唯一
          message = '该邮箱地址已被注册，请使用别的邮箱！'
          return render(request, 'login/register.html', locals())

        # 当一切都OK的情况下，创建新用户
        # 利用ORM的API，创建一个用户实例，然后保存到数据库内。
        new_user = models.User.objects.create()
        new_user.name = username
        new_user.password = hash_code(password1)
        new_user.email = email
        new_user.sex = sex
        new_user.save()

        code = make_confirm_string(new_user)
        send_email(email, code)

        message = '请前往注册邮箱，进行邮件确认！'
        return render(request, 'login/confirm.html', locals())  # 跳转到等待邮件确认页面。

  register_form = forms.RegisterForm()
  return render(request, 'login/register.html', locals())




def logout(request):
  
  if not request.session.get('is_login', None):
    # 如果本来就未登录，也就没有登出一说
    return redirect("/login/index/")
  request.session.flush()
  # 或者使用下面的方法
  # del request.session['is_login']
  # del request.session['user_id']
  # del request.session['user_name']
  return redirect("/login/index/")



def user_confirm(request):
  # 获取确认码
  code = request.GET.get('code', None)
  message = ''
  try:
    confirm = models.ConfirmString.objects.get(code=code)
  except:
    message = '无效的确认请求!'
    return render(request, 'login/confirm.html', locals())

  c_time = confirm.c_time
  now = datetime.datetime.now()
  if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
    confirm.user.delete()
    message = '您的邮件已经过期！请重新注册!'
    return render(request, 'login/confirm.html', locals())
  else:
    # 如果未超期，修改用户的has_confirmed字段为True，并保存，表示通过确认了。
    # 然后删除注册码，但不删除用户本身。最后返回confirm.html页面，并提示。
    confirm.user.has_confirmed = True
    confirm.user.save()
    confirm.delete()
    message = '感谢确认，请使用账户登录！'
    return render(request, 'login/confirm.html', locals())