from django.http import HttpResponseRedirect
from django.http.request import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from .models import Question, Choise

class IndexView(generic.ListView):
  template_name = "polls/index.html"
  context_object_name = "latest_question_list"

  def get_queryset(self):
    return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
  model = Question
  template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
  model = Question
  template_name = "polls/detail.html"

def vote(request: HttpRequest, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice: Choise = question.choise_set.get(pk=request.POST["choice"])
  except (KeyError, Choise.DoesNotExist):
    return render(request, "polls/detail.html", { "error_message": "missing choice" })
  else:
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

# from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
# from django.shortcuts import render, get_object_or_404
# from django.urls import reverse
# from .models import Question, Choise

# def index(request):
#   latest_question_list = Question.objects.order_by("-pub_date")[:5]
#   context = {
#     'latest_question_list': latest_question_list
#   }
#   return render(request, "polls/index.html", context)

# def detail(request, question_id):
#   question = get_object_or_404(Question, pk=question_id)
#   return render(request, "polls/detail.html", { "question": question })

# def results(request, question_id):
#   question = get_object_or_404(Question, pk=question_id)
#   return render(request, "polls/results.html", { 'question': question })