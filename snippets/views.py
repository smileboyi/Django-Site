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