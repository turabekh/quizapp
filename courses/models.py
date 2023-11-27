from django.db import models
from django.conf import settings


class Course(models.Model):
    name = models.CharField(max_length=200)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="taught_courses", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    learning_outcomes = models.TextField(null=True, blank=True)
    academic_year = models.CharField(max_length=9, choices=(
        ('2023-2024', '2023-2024'),
        ('2024-2025', '2024-2025'),
        ('2025-2026', '2025-2026'),
        ('2026-2027', '2026-2027'),
        ('2027-2028', '2027-2028'),
        ('2028-2029', '2028-2029'),
        ('2029-2030', '2029-2030'),
        ('2030-2031', '2030-2031'),
        ('2031-2032', '2031-2032'),
    ), default= '2023-2024')
    semester = models.CharField(max_length=20, choices=(
        ('first', 'First Semester'),
        ('second', 'Second Semester'),
        ('summer', 'Summer'),
    ), default='first')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.teacher.first_name} {self.teacher.last_name}   {self.academic_year} {self.semester}"

class AssessmentCriteria(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='assessment_criteria')
    criteria = models.TextField(null=True, blank=True)
    criteria_type = models.CharField(max_length=20, 
                                     choices=(("pass", "Pass"), ("merit", "Merit"), ("distinction", "Distinction")),
                                     default="pass"
                                     )
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.criteria
    
class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    date_enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f'{self.student} enrolled in {self.course}'


class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes', null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.text

class AnswerChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    
class QuizAttempt(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student} attempt at {self.quiz.title} on {self.timestamp}'

class AnswerSubmission(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='submissions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chosen_answer = models.ForeignKey(AnswerChoice, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'Submission for {self.question.text} by {self.attempt.student}'
