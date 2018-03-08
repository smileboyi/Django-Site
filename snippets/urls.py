from django.conf.urls import url
from snippets import views
# 用于API URL尾部添加格式后缀，比如http://example.com/api/items/4.json.
from rest_framework.urlpatterns import format_suffix_patterns

# 版本一、二
# urlpatterns = [
#     url(r'^snippets/$', views.snippet_list),
#     url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
# ]

# 版本三、四、五
urlpatterns = [
    url(r'^snippets/$', views.SnippetList.as_view()),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
]
# 如果不是已格式后缀结尾，就以'/'结尾。
urlpatterns = format_suffix_patterns(urlpatterns)