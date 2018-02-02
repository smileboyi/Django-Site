from django.contrib.sitemaps import Sitemap
from polls.models import Question,Choice
from django.urls import reverse

# polls站点主页
class PollsSitemap(Sitemap):
	changefreq = "never"  # 目录更新频率
	priority = 0.7   # 当前目录权重（0-1），权重高的目录会排列在后面

	# items必需
	def items(self):
		return Question.objects.all()

	# 使用了这个，就不用使用get_absolute_url返回路径
	def location(self, obj):
  	# polls:index(没有参数传递)对应的视图为IndexView
		return reverse('polls:index')

	# 最后更新时间
	def lastmod(self, obj):
		return obj.pub_date


# 问题详情页(投票页)
class VoteSitemap(Sitemap):
	changefreq = "never"
	priority = 0.6

	def items(self):
		return Question.objects.all()

	def location(self, obj):
  	# obj表示Choice
		# url polls:detail对应的视图为DetailView，DetailView对应的模型为Question
		return reverse('polls:detail', kwargs={'pk': obj.id})