from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Question, Choice
from django.urls import reverse
from django.utils import timezone
import sqlite3

def index(request):
    return render(request, 'polls/index.html')

@login_required
def polls(request):
    questions = Question.objects.order_by('-pub_date')
    context = { 'questions': questions }
    return render(request, 'polls/polls.html', context)

# fix 5:
# @login_required
@csrf_exempt
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

# fix 5:
# @login_required
@csrf_exempt
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('results', args=(question.id,)))

@login_required
def add_poll(request):
    if request.method == 'POST':
        question_text = request.POST.get('question')
        if not question_text:
            return HttpResponse("Question text is required.")
        new_question = Question.objects.create(question_text=question_text, pub_date=timezone.now())
        choices = []
        for i in range(1, 4):
            choice_text = request.POST.get(f'option{i}')
            if choice_text:
                choices.append(choice_text)
        if len(choices) < 3:
            return HttpResponse("Three choices are required.")
        for choice_text in choices:
            new_question.choice_set.create(choice_text=choice_text)
        return redirect('/add_poll')
    if request.method == 'GET':
        return render(request, 'polls/add_poll.html')

# flaw 1:
@csrf_exempt
# fix 5:
# @login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        notes = question.note_set.all()
    except:
        notes = []
    return render(request, 'polls/results.html', {'question': question, 'notes': notes})

# flaw 1:
@csrf_exempt
# fix 5:
# @login_required
def add_note(request, question_id):
    if request.method == 'POST':
        question = get_object_or_404(Question, pk=question_id)
        note_text = request.POST.get('note_text')
        if note_text:
            username = request.user.username
            dbname = './db.sqlite3'
            conn = sqlite3.connect(dbname)
            cursor = conn.cursor()
            # flaw 3:
            cursor.executescript("INSERT INTO polls_note (user, question_id, note_text) VALUES ('" + username + "', " + str(question_id) + ", '" + note_text + "')")

            # fix 3:
            # sql = "INSERT INTO polls_note (user, question_id, note_text) VALUES (?, ?, ?)"
            # values = (username, str(question_id), note_text)
            # cursor.execute(sql, values)

            conn.commit()
            conn.close()
            return redirect(f'/{question_id}/results', question_id=question_id)
        else:
            return render(request, 'polls/detail.html', {'question': question, 'error_message': 'Note text is required.'})
    else:
        return redirect(f'/{question_id}/results', question_id=question_id)
