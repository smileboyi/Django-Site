from django import forms
from . import models
from captcha.fields import CaptchaField



# 编写Django的form表单，非常类似我们在模型系统里编写一个模型。
# 在模型中，一个字段代表数据表的一列，而form表单中的一个字段代表<form>中的一个<input>元素。
class UserForm(forms.Form):
  username = forms.CharField(label="用户名", max_length=128,  widget=forms.TextInput(attrs={'class': 'form-control'}))
  # label用于label标签，widget用于指定表单元素,并添加样式
  password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
  # 关于captcha的功能，你可以设置六位、八位验证码，可以对图形噪点的生成模式进行定制
  captcha = CaptchaField(label='验证码')



"""
# 因为表单类和模型类的类属性是对应关系，可以直接参考模型类
# 整合model模型和forms表单，你连表单类都不用写，直接使用数据模型User生成表单类
# Form所有的钩子ModelForm都有（is_valid()）
class UserForm(forms.ModelForm):
  class Meta:
    model = models.User
    fields = ['name', 'password']

  def __init__(self, *args, **kwargs):
    super(UserForm, self).__init__(*args, *kwargs)
    self.fields['name'].label = '用户名'
    self.fields['password'].label = '密码'
"""



















