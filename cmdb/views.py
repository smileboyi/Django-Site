from django.shortcuts import render
# from django.shortcuts import HttpResponse
from cmdb import models  # models和数据库相关

# Create your views here.

# # 创建一个用户信息列表，预定义2个数据(如果服务重启，那么数据就会回到原始状态)
# user_list = [
#   {"user":"jack", "pwd":"abc"},
#   {"user":"tom", "pwd":"ABC"},
# ]



# request参数必须有，名字是类似self的默认规则，可以改，它封装了用户请求的所有内容。
def index(request):
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
  # 从数据库中读取所有数据
  user_list = models.UserInfo.objects.all()


    # temp = {"user":username, "pwd":password}
    # user_list.append(temp)

  # 当你想返回一个html时，就用render方法
  # 第一个参数固定，第二个参数就是指定的文件,第三个参数是字典
  return render(request, 'cmdb/index.html',{"data": user_list})