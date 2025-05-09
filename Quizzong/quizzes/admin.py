from django.contrib import admin
from .models import Quiz, Question


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    fields = ['text', 'type', 'points', 'order', 'correct_answer']
    show_change_link = True

class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'available_until', 'available_from', 'due_date', 'time_limit']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [QuestionInline]

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz', 'type', 'points', 'order']
    list_filter = ['quiz', 'type']
    search_fields = ['text', 'quiz__title']
    readonly_fields = ['created_at', 'updated_at']

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
