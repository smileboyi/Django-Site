from django.shortcuts import render,render_to_response
from django.template import loader, Context
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django import forms
from io import BytesIO
from .models import *
import reportlab
import csv
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
    destination = open(os.path.join(BASE_DIR,'upload/', myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作  
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




# 使用系统自带的csv
def csv_view(request):
  # Create the HttpResponse object with the appropriate CSV header.
  response = HttpResponse(content_type='text/csv')
  # 响应对象获取了附加的Content-Disposition协议头，它含有CSV文件的名称。文件名可以是任意的；你想把它叫做什么都可以。浏览器会在”另存为“对话框中使用它，或者其它。
  # Content-Disposition以'attachment'开头，强制让浏览器弹出对话框来提示或者确认
  response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

  # csv.writer 函数接受一个类似于文件的对象，而HttpResponse 对象正好合适。
  # 如果数据量大，可以使用StreamingHttpResponse
  writer = csv.writer(response)
  writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
  writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

  return response

# 使用Django的csv
def csv_view2(request):
  # Create the HttpResponse object with the appropriate CSV header.
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

  # The data is hard-coded here, but you could load it from a database or
  # some other source.
  csv_data = (
      ('First row', 'Foo', 'Bar', 'Baz'),
      ('Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"),
  )
  # 使用模板
  t = loader.get_template('upload/my_template_name.txt')
  c = Context({
    'data': csv_data,
  })
  response.write(t.render(c))
  return response



def pdf_view(request):
  # 创建带有PDF头部定义的HttpResponse对象
  response = HttpResponse(content_type='application/pdf')
  response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

  # 创建一个PDF对象，并使用响应对象作为它要处理的‘文件’
  # Content-Disposition以'attachment'开头，强制让浏览器弹出对话框来提示或者确认
  p = canvas.Canvas(response)

  # 通过PDF对象的drawString方法，写入一条信息。具体参考模块的官方文档说明。
  p.drawString(100, 100, "Hello world.")

  # 关闭PDF对象
  p.showPage()
  p.save()
  return response


def pdf_view2(request):
  # Create the HttpResponse object with the appropriate PDF headers.
  response = HttpResponse(content_type='application/pdf')
  response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
  # 使用ReportLab创建复杂的PDF文档时，可以考虑使用io库作为PDF文件的临时保存地点。
  buffer = BytesIO()

  # Create the PDF object, using the BytesIO object as its "file."
  p = canvas.Canvas(buffer)

  # Draw things on the PDF. Here's where the PDF generation happens.
  # See the ReportLab documentation for the full list of functionality.
  p.drawString(100, 100, "Hello world2.")

  # Close the PDF object cleanly.
  p.showPage()
  p.save()

  # Get the value of the BytesIO buffer and write it to the response.
  pdf = buffer.getvalue()
  buffer.close()
  response.write(pdf)
  return response












