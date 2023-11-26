from django.urls import path
from . import views

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('courses-with-enrollment/', views.get_courses_with_enrollment, name='courses_with_enrollment'),
    path('unenroll/<int:course_id>/', views.unenroll_course, name='unenroll_course'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('quizzes/results/<int:quiz_id>/', views.QuizResultsView.as_view(), name='quiz_results'),
    path('quizzes/submit/<int:quiz_id>/', views.submit_quiz, name='submit_quiz'),
    path('quizzes/<int:pk>/', views.QuizDetailView.as_view(), name='quiz-detail'),
    path('student/grades/', views.get_student_grades, name='student-grades'),
]
