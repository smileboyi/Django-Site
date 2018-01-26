from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django import forms
from .models import *
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your views here.

# 不使用forms的简单版本
def upload_file(request): 
  """
    myFile.read()：从文件中读取整个上传的数据，这个方法只适合小文件；
    myFile.chunks()：按块返回文件，通过在for循环中进行迭代，可以将大文件按块写入到服务器中；
    myFile.multiple_chunks()：这个方法根据myFile的大小，返回True或者False，当myFile文件大于2.5M(默认为2.5M，可以调整)时，该方法返回True，否则返回False，因此可以根据该方法来选择选用read方法读取还是采用chunks方法：
      if myFile.multiple_chunks() == False:
        # 使用myFile.read()
      else:
        # 使用myFile.chunks()
    myFile.name：这是一个属性，不是方法，该属性得到上传的文件名，包括后缀，如123.exe；
    myFile.size：这也是一个属性，该属性得到上传文件的大小。
  """ 
  # 请求方法为POST时，进行处理
  if request.method == "POST":
    # 获取上传的文件，如果没有文件，则默认为None  
    # 上传的文件保存在files字典中，不是在post中，所以不能通过request.POST访问
    myFile =request.FILES.get("myfile", None)
    if not myFile:  
      return HttpResponse("no files for upload!")

    # 需要在应用下面建立一个upload文件夹，存放上传的文件
    destination = open(os.path.join(BASE_DIR, myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作  
    for chunk in myFile.chunks():      # 分块写入文件  
      destination.write(chunk)  
    destination.close()  
    return HttpResponse("upload over!")

  return render(request,'upload/upload.html')



# 使用forms的简单版本
class NormalUserForm(forms.Form):
  #form的定义和model类的定义很像
  username=forms.CharField()
  headImg=forms.FileField()
    
#在View中使用已定义的Form方法
def registerNormalUser(request):
  if request.method=="POST":
    # 实例化表单，必须将request.FILES传递到form的构造函数中
    uf = NormalUserForm(request.POST,request.FILES)

    # 验证数据是否合法，当合法时可以使用cleaned_data属性。
    if uf.is_valid():
      # 用来得到经过'clean'格式化的数据，会所提交过来的数据转化成合适的Python的类型。
      username = uf.cleaned_data['username']
      headImg = uf.cleaned_data['headImg']
      # write in database
      normalUser=NormalUser() # 实例化NormalUser Model对象
      normalUser.username = username
      normalUser.headImg = headImg
      normalUser.save() # 保存到数据库表中
      return HttpResponse('Upload Succeed!') # 重定向显示内容（跳转后内容）
  else:
    uf=NormalUserForm() # 实例化空表单

  return render(request,'upload/register.html',{'uf':uf})