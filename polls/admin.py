from django.contrib import admin
# 引入应用的models
# 决定哪些模型需要在admin内进行管理，在admin.py文件中注册它们。
from .models import Choice, Question   

# Register your models here.

"""
用python manage.py createsuperuser命令创建管理员账户。
"""

## 1.将models注册到站点进行管理(然后站点将提供Question管理的服务页面)
# admin.site.register(Question)


# admin下有不同模型定制类
class ChoiceInline(admin.TabularInline):  #admin.StackedInline
  model = Choice
  extra = 3


# 2.如果你想自定义该页面的外观和工作方式，可以在注册对象的时候告诉Django你的自定义选项。
# 需要继承模型管理类
class QuestionAdmin(admin.ModelAdmin):
  fieldsets = [
    # 字段集合fieldsets中每一个元组的第一个元素是该字段集合的标题。
    (None,               {'fields': ['question_text']}),
    ('Date information', {'fields': ['pub_date']}),
  ]
  # a.Choice对象将在Question管理页面进行编辑，默认情况，请提供3个Choice对象的编辑区域。
  inlines = [ChoiceInline]

  # 默认情况下，只会显示__str__内容，可以通过list_display指定要显示的字段
  # list_display会覆盖__str__，所以要重新指定__str__代表的那个字段
  list_display = ('question_text', 'pub_date', 'was_published_recently')
  
  # 添加字段过滤功能
  list_filter = ['pub_date']

  # 添加字段搜索功能
  search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)

# b.Choice对象单独建一个表单页
# admin.site.register(Choice)
