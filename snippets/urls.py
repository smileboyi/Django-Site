from django.conf.urls import url,include
from snippets import views
# 用于API URL尾部添加格式后缀，比如http://example.com/api/items/4.json.
from rest_framework.urlpatterns import format_suffix_patterns

# 版本一、二
# urlpatterns = [
# 	url(r'^snippets/$', views.snippet_list),
# 	url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
# ]

# 版本三、四、五
urlpatterns = [
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