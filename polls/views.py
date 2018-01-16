# from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
# from django.template import loader   # 用于HttpResponse
# from django.http import Http404    # 用于404
# 用于替换上面2个封装好的，直接使用，不需要HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Choice, Question

"""
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
	
	# 同样，还有一个get_list_or_404()方法，和下面的get_object_or_404()类似，只不过是用来替代filter()函数，当查询列表为空时弹出404错误。
	# （filter是模型API中用来过滤查询结果的函数，它的结果是一个列表集。而get则是查询一个结果的方法，和filter是一个和多个的区别！）
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question': question})



def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question': question})

"""


# 投票视图（vote()视图没有对应的html模板，它直接跳转到results视图去了。）
def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)

	try:
		# 查找这个问题的投票结果
		# request.POST是一个类似字典的对象，允许你通过键名（表单name）访问提交的数据。
		# 使用request.POST有可能触发一个KeyError异常，如果你的POST数据里没有提供choice键值。
		# PS：通常我们会给个默认值，防止这种异常的产生，例如request.POST[’choice’,None]，一个None解决所有问题。
		# pk表示通过主键（primary key）进行查询
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# 这个问题还没投过票
		# 发生choice未找到异常时，重新返回表单页面，并给出提示信息
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# 你成功处理POST数据后，应当保持一个良好的习惯，始终返回一个HttpResponseRedirect（不要停留在提交页面上，防止用户连续多次提交）。
		#　使用了一个reverse()函数。它能帮助我们避免在视图函数中硬编码URL，构造出一个url地址。把活扔给另外一个路由对应的视图去干。
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))




from django.views import generic   # 用于类视图


"""
重复做法：通过从URL传递过来的参数去数据库查询数据，加载一个模板，利用刚才的数据渲染模板，返回这个模板。
使用类视图，会帮你完成上面的步骤：
1.修改URLconf设置
2.删除一些旧的无用的视图
3.采用基于类视图的新视图
"""
# 这个还需将结果进行筛选
class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	# 覆盖默认提供的上下文变量question_list
	context_object_name = 'latest_question_list'
	def get_queryset(self):
	# 返回最近发布的5个问卷.
		return Question.objects.order_by('-pub_date')[:5]

# 最简单的类视图：直接从url获取数据然后到model里查找，将结果填充到视图模板上
class DetailView(generic.DetailView):
	# 每一种类视图都需要知道它要作用在哪个模型上，这通过model属性提供。
	# 默认提供上下文变量question
	model = Question
	# xxxView默认会提供一个模板，一般不会使用默认模板
	template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
	model = Question
	template_name ='polls/results.html'