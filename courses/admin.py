from django.contrib import admin
from .models import (
    Course, Topic, Question, 
    AnswerChoice, Quiz, AnswerChoice, 
    QuizAttempt, AnswerSubmission,
    AssessmentCriteria,
)

from .forms import QuizForm, QuestionForm       

class AnswerChoiceInline(admin.TabularInline):
    model = AnswerChoice
    extra = 4  # Display 4 answer choices by default

class QuestionInline(admin.TabularInline):
    model = Question
    inlines = [AnswerChoiceInline]
    extra = 1  # One question by default

class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1  # One topic by default

class AssessmentCriteriaInline(admin.TabularInline):
    model = AssessmentCriteria
    extra = 3

class CourseAdmin(admin.ModelAdmin):
    inlines = [AssessmentCriteriaInline, TopicInline]

class TopicAdmin(admin.ModelAdmin):
    pass

class QuestionAdmin(admin.ModelAdmin):
    form = QuestionForm
    inlines = [AnswerChoiceInline]

class QuizAdmin(admin.ModelAdmin):
    form = QuizForm
    inlines = [QuestionInline]

class AnswerChoiceInline(admin.TabularInline):
    model = AnswerChoice
    extra = 4  # Display 4 answer choices by default

class QuestionInline(admin.TabularInline):
    model = Question
    inlines = [AnswerChoiceInline]
    extra = 1  # Display 1 question by default

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

class AnswerSubmissionInline(admin.TabularInline):
    model = AnswerSubmission
    readonly_fields = ('question', 'chosen_answer', 'is_correct')
    can_delete = False
    extra = 0

class QuizAttemptAdmin(admin.ModelAdmin):
    inlines = [AnswerSubmissionInline]
    readonly_fields = ('student', 'quiz', 'timestamp')
    list_display = ('student', 'quiz', 'timestamp')
    list_filter = ('quiz', 'student')

admin.site.register(Course, CourseAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(AnswerChoice)
admin.site.register(QuizAttempt, QuizAttemptAdmin)
