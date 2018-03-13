from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User


"""
class SnippetSerializer(serializers.Serializer):
  # 第一部分定义了序列化和反序列化的字段
  # 把变量从内存中变成可存储或传输的过程称之为序列化，在Python中叫pickling，在其他语言中也被称之为serialization，marshalling，flattening等等
  # 序列化之后，就可以把序列化后的内容写入磁盘，或者通过网络传输到别的机器上。反过来，把变量内容从序列化的对象重新读到内存里称之为反序列化，即unpickling。
  id = serializers.IntegerField(read_only=True)
  title = serializers.CharField(required=False, allow_blank=True, max_length=100)
  code = serializers.CharField(style={'base_template': 'textarea.html'})
  linenos = serializers.BooleanField(required=False)
  language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
  style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

  # 第二部分定义了符合要求的已序列化snippet实例如何反序列化
  # create()和update()方法定义了当调用serializer.save()时如何对实例进行创建或修改,
  # serializer和django的form非常类似，而且包括一些类似的验证字段的方法，如required,max_lengthanddefault.
  def create(self, validated_data):
    # 新建Snippet实例
    return Snippet.objects.create(**validated_data)

  def update(self, instance, validated_data):
    # 更新Snippet示例
    instance.title = validated_data.get('title', instance.title)
    instance.code = validated_data.get('code', instance.code)
    instance.linenos = validated_data.get('linenos', instance.linenos)
    instance.language = validated_data.get('language', instance.language)
    instance.style = validated_data.get('style', instance.style)
    instance.save()
    return instance
"""



"""
我们的SnippetSerializer类很多信息和Snippet model中是重复的，
为了保证我们代码的简洁，减少重复代码，
类似于django的提供的form和modelform，REST framework也提供了Serializerand ModelSerializer
重要的是要记住 ModelSerializer 不做任何格外的配置，它只是创建序列化类的快捷方式：
根据model里的字段自动定义字段集,简单的实现 create() and update() 方法
"""
"""
class SnippetSerializer(serializers.ModelSerializer):
  # 新增（权限）
  # source参数用于控制那个属性被用来填充字段，并且可以指向序列化实例上的任何属性。 
  # ReadOnlyField总是只读的，并且将用于序列化表示，但不会用于在反序列化时更新模型实例。另一种CharField（read_only = True）。
  owner = serializers.ReadOnlyField(source='owner.username')

  class Meta:
    model = Snippet
    fields = ('id', 'title', 'code', 'linenos', 'language', 'style', 'owner')


# 新增（权限）
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
  # 因为'snippets'（owner字段，子表）是User模型（父表）上的反向关系，所以在使用ModelSerializer类时，它不会被默认包含，因此我们需要为它添加一个显式字段。
  # 反向关系：从父表找子表的信息，但是父表中没有子表的信息。通过关联字段related_name查找
  snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

  class Meta:
    model = User
    # 一般情况下序列化得到的外键的内容只是id，所以将snippets添加到序列列表中
    fields = ('id', 'username', 'snippets')

"""


"""

使用HyperlinkedModelSerializer代替ModelSerializer,实例之间用超链接形式
HyperlinkedModelSerializer不会自动包含pk field,HyperlinkedModelSerializer会自动包括url field

"""
class SnippetSerializer(serializers.HyperlinkedModelSerializer):
  owner = serializers.ReadOnlyField(source='owner.username')
  # https://stackoverflow.com/questions/27484344/assertion-error-at-django-rest-framework
  highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html',read_only=True)

  class Meta:
    model = Snippet
    fields = ('url', 'highlight', 'owner','title', 'code', 'linenos', 'language', 'style')


class UserSerializer(serializers.HyperlinkedModelSerializer):
  # 关系使用的是HyperlinkedRelatedField而不是PrimaryKeyRelatedField
  snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail',read_only=True)

  class Meta:
    model = User
    fields = ('url', 'username', 'snippets')