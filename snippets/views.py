###########################
#版本一:使用django的request和response,使用rest_framework的json序列化和反序列化函数
##########################
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






























