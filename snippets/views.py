###########################
#版本一:使用django的request和response,使用rest_framework的json序列化和反序列化函数
###########################
"""
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


class JSONResponse(HttpResponse):
  # 将HttpResponse序列化为json格式
  def __init__(self, data, **kwargs):
    content = JSONRenderer().render(data)
    kwargs['content_type'] = 'application/json'
    super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt  # 在post测试的时候无法获取到Django的csrf token，所以使用@csrf_exempt将此视图排除，不检查csrf token。
def snippet_list(request):
  # 列出所有的实例，或创建一个新的实例.
  if request.method == 'GET':
    snippets = Snippet.objects.all()
    # 可以序列化querysets对象来代替model instances，因此在序列化的时候需要添加many=True参数
    serializer = SnippetSerializer(snippets, many=True)
    return JSONResponse(serializer.data)

  elif request.method == 'POST':
    data = JSONParser().parse(request)
    # model instances
    serializer = SnippetSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return JSONResponse(serializer.data, status=201)
    return JSONResponse(serializer.errors, status=400)



@csrf_exempt
def snippet_detail(request, pk):
  # 检索、更新和删除代码段
  try:
    snippet = Snippet.objects.get(pk=pk)
  except Snippet.DoesNotExist:
    return HttpResponse(status=404)

  if request.method == 'GET':
    serializer = SnippetSerializer(snippet)
    return JSONResponse(serializer.data)

  elif request.method == 'PUT':
    data = JSONParser().parse(request)
    serializer = SnippetSerializer(snippet, data=data)
    if serializer.is_valid():
      serializer.save()
      return JSONResponse(serializer.data)
    return JSONResponse(serializer.errors, status=400)

  elif request.method == 'DELETE':
    snippet.delete()
    return HttpResponse(status=204)

"""



###########################
# 版本二:，使用rest_framework的Request和Response替换HttpRequest、JSONResponse,
# 我们不再明确打印我们的对指定内容类型的请求或响应。也就是不使用rest_framework的json序列化和反序列化函数
# request.data能够处理json请求！！！但是它也能处理其他格式！！
###########################
"""
# REST framework为每个状态码提供了更加明确的标示
from rest_framework import status
from rest_framework.decorators import api_view
# Response是一种TemplateResponse类型，它渲染文本内容，并根据内容决定返回给客户端的数据类型
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


# @api_view 装饰器用在函数的view中，@APIView 装饰器用在类的view中，能够根据内容协商渲染装饰器还提供了一些行为
# 如适当的返回405 Method Not Allowed不允许请求的响应，以及当访问request.data发生格式错误时处理任何ParseError异常
@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
  # format=None表示response不再是单一的格式内容，让我们在API URL尾部添加格式后缀，用格式后缀给我们明确参考指定格式的URL，类似于http://example.com/api/items/4.json.
  # Request封装了HttpRequest, request.data可供 'POST', 'PUT' and 'PATCH' 等请求使用.
  if request.method == 'GET':
    snippets = Snippet.objects.all()
    serializer = SnippetSerializer(snippets, many=True)
    return Response(serializer.data)

  elif request.method == 'POST':
    serializer = SnippetSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
  try:
    snippet = Snippet.objects.get(pk=pk)
  except Snippet.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = SnippetSerializer(snippet)
    return Response(serializer.data)

  elif request.method == 'PUT':
    serializer = SnippetSerializer(snippet, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  elif request.method == 'DELETE':
    snippet.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

"""


###########################
# 版本三:使用类来编写view，跟基于方法的视图差别不多
###########################
"""
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SnippetList(APIView):
  def get(self, request, format=None):
    snippets = Snippet.objects.all()
    serializer = SnippetSerializer(snippets, many=True)
    return Response(serializer.data)

  # 调用的方法名和请求名一致
  def post(self, request, format=None):
    serializer = SnippetSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
  def get_object(self, pk):
    try:
      return Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
      raise Http404

  def get(self, request, pk, format=None):
    snippet = self.get_object(pk)
    serializer = SnippetSerializer(snippet)
    return Response(serializer.data)

  def put(self, request, pk, format=None):
    snippet = self.get_object(pk)
    serializer = SnippetSerializer(snippet, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    snippet = self.get_object(pk)
    snippet.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

"""



###########################
# 版本四:使用mixins来编写view
###########################
"""
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
# 我们使用的创建/检索/更新/删除操作对于我们创建的任何模型支持的API视图将非常相似。这些常见的行为是在REST框架的mixin类中实现的。
from rest_framework import mixins
# 和from django.views import generic一样，提供类视图
from rest_framework import generics


class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
  # 使用mixins需要设置queryset和serializer_class
  # queryset：要操作的数据集；serializer_class：指定一个序列化类
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  # mixin类提供.list()和.create()操作。然后，我们将明确的绑定get和post方法绑定到适当的操作。
  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)


class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  # GenericAPIView类来提供核心功能，并混入增加提供.retrieve()，.update()和.destroy()行动。
  def get(self, request, *args, **kwargs):
    return self.retrieve(request, *args, **kwargs)

  def put(self, request, *args, **kwargs):
    return self.update(request, *args, **kwargs)

  def delete(self, request, *args, **kwargs):
    return self.destroy(request, *args, **kwargs)

"""


###########################
# 版本五:使用class-based（泛类）来编写view
# 人生苦短，我用python
###########################
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
# REST框架提供了一组已经混合（mixins）的通用视图
from rest_framework import generics

# 新增（权限）
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly


# generics.ListCreateAPIView实际上继承了mixins中的mixins.ListModelMixin,mixins.CreateModelMixin,
# 等于在又把mixins类根据get post put delete请求方式重新封装了一层。
class SnippetList(generics.ListCreateAPIView):
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  # 新增（权限）
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

  # 新增（权限）
  # 覆盖.perform_create（）方法，允许我们修改实例保存的方式，并处理在传入请求或请求的URL中隐含的任何信息。
  def perform_create(self, serializer):
    # 当我们的serializer里create()方法被调用时，将自动添加owner字段和验证合法的请求数据
    serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  # 新增（权限）
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)


# 新增（权限）
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer










