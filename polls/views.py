# from django.shortcuts import render
from django.http import HttpResponse
# from django.template import loader   # 用于HttpResponse
# from django.http import Http404    # 用于404
# 用于替换上面2个封装好的，直接使用，不需要HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Question

# Create your views here.
# Django通过对比请求的URL地址来选择对应的视图
def index(request):
	# 主页展示，数据从数据库中获取
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {'latest_question_list': latest_question_list}

	# template = loader.get_template('polls/index.html')
	# return HttpResponse(template.render(context, request))
	return render(request, 'polls/index.html', context)


# question_id参数由路由提供
def detail(request, question_id):
	# try:
	# 	question = Question.objects.get(pk=question_id)
	# except Question.DoesNotExist:
	# 	# 如果没有找到数据返回404页面
	# 	raise Http404("Question does not exist")
	
	# """
	# 同样，还有一个get_list_or_404()方法，和下面的get_object_or_404()类似，只不过是用来替代filter()函数，当查询列表为空时弹出404错误。
	# （filter是模型API中用来过滤查询结果的函数，它的结果是一个列表集。而get则是查询一个结果的方法，和filter是一个和多个的区别！）
	# """
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question': question})




def results(request, question_id):
	response = "You're looking at the results of question %s."
	return HttpResponse(response % question_id)


def vote(request, question_id):
	return HttpResponse("You're voting on question %s." % question_id)





