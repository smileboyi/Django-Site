import os
from django.core.mail import EmailMultiAlternatives

# 由于我们是单独运行send_mail.py文件，所以无法使用Django环境，需要通过os模块对环境变量进行设置
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

if __name__ == '__main__':

  subject, from_email, to = '来自www.liujiangblog.com的测试邮件', 'xxx@sina.com', 'xxx@qq.com'
  text_content = '欢迎访问www.liujiangblog.com，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！'
  html_content = '<p>欢迎访问<a href="http://www.liujiangblog.com" target=blank>www.liujiangblog.com</a>，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！</p>'
  # text_content是用于当HTML内容无效时的替代txt文本
  msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
  msg.attach_alternative(html_content, "text/html")
  msg.send()