from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.forms.models import modelformset_factory # model form for querysets
from .forms import QuizForm, QuestionForm, OptionForm
from .models import Quiz, Question, Option

@login_required
def quiz_list_view(request):
    return

# QUIZ ADMIN (UNDER DEVELOPMENT)
@login_required
def admin_quiz_create_view(request):
    quiz_form = QuizForm(request.POST or None)
    QuestionFormset = modelformset_factory(Question, form=QuestionForm, extra=1)
    qs = Question.objects.none()
    question_formset = QuestionFormset(request.POST or None, queryset = qs)
    context = {
        "quiz_form": quiz_form,
        "question_formset": question_formset,
    }
    if all([quiz_form.is_valid(), question_formset.is_valid()]):
        parent = quiz_form.save(commit=False)
        parent.save()
        for question_form in question_formset:
            child = question_form.save(commit=False)
            child.quiz = parent
            child.save()
            context['message'] = 'Quiz created.'
        return redirect(parent.get_absolute_url(), context)
    else:
        quiz_form = QuizForm()

    return render(request, 'quiz/create_update_quiz.html', context)

@login_required
def admin_quiz_update_view(request, id=None):
    quiz = get_object_or_404(Quiz, id=id)
    quiz_form = QuizForm(request.POST or None, instance=quiz)
    QuestionFormset = modelformset_factory(Question, form=QuestionForm, extra=0)
    qs = quiz.questions.all()
    question_formset = QuestionFormset(request.POST or None, queryset=qs)

    context={
        "quiz_form": quiz_form, 
        "question_formset": question_formset,
        "quiz": quiz, 
    }
    if all([quiz_form.is_valid(), question_formset.is_valid()]):
        parent = quiz_form.save(commit=False)
        parent.save()
        for question_form in question_formset:
            child = question_form.save(commit=False)
            child.quiz = parent
            child.save()
        context['message'] = 'Data saved.'
    return render(request, "quiz/create_update_quiz.html",  context)

@login_required
def quiz_update_view():
    return