from django.conf.urls import url,include
from snippets import views
# 用于API URL尾部添加格式后缀，比如http://example.com/api/items/4.json.
from rest_framework.urlpatterns import format_suffix_patterns
from snippets.views import SnippetViewSet, UserViewSet
from rest_framework import renderers
from rest_framework.routers import DefaultRouter




# 版本一、二
"""
urlpatterns = [
	url(r'^snippets/$', views.snippet_list),
	url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
]
"""




# 版本三、四、五
"""
from snippets.views import api_root # 版本五、六


urlpatterns = [
	# 版本五
	url(r'^$', api_root),

	# name用于给url取个别名，与序列化中view_name对应
	url(r'^snippets/$', views.SnippetList.as_view(),name="snippet-list"),
	url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view(),name="snippet-detail"),
	url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view(),name='snippet-highlight'),
	
	# 新增（权限）
	url(r'^users/$', views.UserList.as_view(),name='user-list'),
	url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(),name='user-detail'),

	# 登录视图url
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# 如果不是以格式后缀结尾，就以'/'结尾。
urlpatterns = format_suffix_patterns(urlpatterns)
"""




# 版本六--A版：将viewsets和urls明确绑定
# 当我们定义URLConf时，处理程序方法只绑定到动作。要看看发生了什么，我们首先从我们的ViewSets显式创建一组视图。
# 从每个ViewSet类创建多个视图
"""
snippet_list = SnippetViewSet.as_view({
	'get': 'list',
	'post': 'create'
})
snippet_detail = SnippetViewSet.as_view({
	'get': 'retrieve',
	'put': 'update',
	'patch': 'partial_update',
	'delete': 'destroy'
})
snippet_highlight = SnippetViewSet.as_view({
	'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
	'get': 'list'
})
user_detail = UserViewSet.as_view({
	'get': 'retrieve'
})

urlpatterns = format_suffix_patterns([
	url(r'^$', api_root),
	url(r'^snippets/$', snippet_list, name='snippet-list'),
	url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
	url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', snippet_highlight, name='snippet-highlight'),
	url(r'^users/$', user_list, name='user-list'),
	url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
])
"""




# 版本六--B版：使用了ViewSet,就不需要手动定义url
# 使用路由器注册适当的视图集，而其余的资源连接到视图和网址的约定可以使用Router类自动处理。
# DefaultRouter类自动创建了根URL，所以可以在views中移除api_root了
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
	url(r'^', include(router.urls)),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]


