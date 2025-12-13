from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .helpers import Helpers
from .models import Question, TeamChoice, PlayerChoice, CoachChoice
from django.db.models import F
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

class IndexView(generic.ListView):

    seq_size = 17
    fibo_limit = 1500
    nums = range(-100, 100)

    hello_info = ("Let me print you first a fibonacci sequence of size: " +
                  str(seq_size) + " & a max limit (last fibonacci seq # should be < than this #) of: " +
                  str(fibo_limit))
    helper = Helpers()
    fibo_sequence = "Fibonacci Sequence: " + str(helper.get_fibonacci(seq_size, fibo_limit))
    prime_numbers_txt = (" Extra Bonus - Send you the prime numbers until 100 ... Prime Numbers " +
                         "(" + str(nums[0]) + " : " + str(nums[-1]) + "):")
    prime_numbers = str(helper.get_prime_nums(nums))

    template_name = "soccerpoll/index.html"
    context_object_name = "latest_q_list"
    extra_context = {"hello_info": hello_info, "fibo_seq": fibo_sequence,
                     "prime_nums_txt": prime_numbers_txt, "prime_nums": prime_numbers}

    def get_queryset(self):
        """ Return the last 10 published qs (not including future ones)."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:10]

#class DetailView(generic.DetailView):
#    model = Question
#    template_name = "spoll/detail.html"
#    def get_queryset(self):
#        """Excludes any questions that aren't published yet."""
#        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "soccerpoll/results.html"

def detail(request, q_id):

    q = get_object_or_404(Question.objects.filter(pub_date__lte=timezone.now()), pk=q_id)

    if q.type.name == "player":
        q_choices = q.playerchoice_set.all
    elif q.type.name == "team":
        q_choices = q.teamchoice_set.all
    else:
        q_choices = q.coachchoice_set.all

    return render(  # Redisplay the question voting form
        request, "soccerpoll/detail.html",
        {"q": q, "q_choices": q_choices
            , "err_msg": "You didn't select a choice ..."}
    )

def vote(request, q_id):
    q = get_object_or_404(Question, pk=q_id)
    selected_choice = get_selected_choice(request, q)
    selected_choice.save()
    # Always return an HttpResponseRedirect after successfully dealing with POST data.
    # This prevents data from being posted twice if a user hits the Back button.
    return HttpResponseRedirect(reverse("soccerpoll:results", args=(q.id,)))

def get_selected_choice(request, q):

    if q.type.name == "player":
        try:
            selected_choice = q.playerchoice_set.get(pk=request.POST["choice"])
        except (KeyError, PlayerChoice.DoesNotExist):
            return get_render(request, q)
        else:
            selected_choice.votes = F("votes") + 1
    elif q.type.name == "team":
        try:
            selected_choice = q.teamchoice_set.get(pk=request.POST["choice"])
        except (KeyError, TeamChoice.DoesNotExist):
            return get_render(request, q)
        else:
            selected_choice.votes = F("votes") + 1
    else:
        try:
            selected_choice = q.coachchoice_set.get(pk=request.POST["choice"])
        except (KeyError, CoachChoice.DoesNotExist):
            return get_render(request, q)
        else:
            selected_choice.votes = F("votes") + 1

    return selected_choice

def get_render(req, q):

    return render(  # Redisplay the question voting form
        req, "soccerpoll/detail.html",
        {"q": q, "error_message": "You didn't select a choice ..."}
    )