from django.db import models

# Create your models here.


from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

# 新增（权限）
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


class Snippet(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  title = models.CharField(max_length=100, blank=True, default='')
  code = models.TextField()
  linenos = models.BooleanField(default=False)
  # 设置代码片段的语言和样式
  language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
  style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

  # 新增（权限）
  """
  当前我们的API在编辑或者删除的时候没有任何限制，我们不希望有些人有高级的行为，确保：
  代码段始终与创建者相关联
  只允许授权的用户可以创建代码段
  只允许代码段创建者可以更新和删除
  没有认证的请求应该有一个完整的只读权限列表
  """
  # Snippet表和用户权限关联
  owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
  highlighted = models.TextField()
  def save(self, *args, **kwargs):
    """
    Use the `pygments` library to create a highlighted HTML
    representation of the code snippet.
    """
    lexer = get_lexer_by_name(self.language)
    linenos = self.linenos and 'table' or False
    options = self.title and {'title': self.title} or {}
    formatter = HtmlFormatter(style=self.style, linenos=linenos,
                              full=True, **options)
    self.highlighted = highlight(self.code, lexer, formatter)
    super(Snippet, self).save(*args, **kwargs)

  class Meta:
    ordering = ('created',)
    