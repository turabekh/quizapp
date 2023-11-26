from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from django.db.models import Exists, OuterRef, Count, Case, When, IntegerField
from .models import (
    Course, Enrollment,
    Quiz, Question,
    AnswerChoice, Topic,
    QuizAttempt, AnswerSubmission,
    QuizAttempt, AnswerSubmission
)
from .serializers import (
    CourseSerializer, 
    EnrollmentSerializer,
    CourseWithEnrollmentSerializer,
    TopicSerializer,
    QuizSerializer,
    QuizSerializer2,
    AnswerSubmissionSerializer,
    QuizAttemptDetailSerializer,
    AnswerSubmissionSerializer2
)

class CourseListView(generics.ListAPIView):
    queryset = Course.objects.filter(active=True).all()
    serializer_class = CourseSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enroll_course(request, course_id):
    course = generics.get_object_or_404(Course, id=course_id)
    if not course.active:
        return Response({'message': 'Course is not active'}, status=status.HTTP_400_BAD_REQUEST)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
    if created:
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'message': 'Already enrolled'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_courses_with_enrollment(request):
    courses = Course.objects.annotate(
        is_enrolled=Exists(
            Enrollment.objects.filter(
                student=request.user,
                course=OuterRef('pk')
            )
        )
    )
    serializer = CourseWithEnrollmentSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unenroll_course(request, course_id):
    try:
        enrollment = Enrollment.objects.get(student=request.user, course_id=course_id)
        enrollment.delete()
        return Response({'message': 'Unenrolled successfully'}, status=status.HTTP_200_OK)
    except Enrollment.DoesNotExist:
        return Response({'message': 'Not enrolled in this course'}, status=status.HTTP_400_BAD_REQUEST)

class CourseDetailView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer  # Use an appropriate serializer

class TopicListView(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class QuizListView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizDetailView(RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer2


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_quiz(request, quiz_id):
    attempt = QuizAttempt.objects.create(student=request.user, quiz_id=quiz_id)
    serializer = AnswerSubmissionSerializer(data=request.data, many=True)
    
    if serializer.is_valid():
        for answer_data in serializer.validated_data:
            print("answer_data", answer_data)
            chosen_answer = answer_data['chosen_answer']
            is_correct = chosen_answer.is_correct
            AnswerSubmission.objects.create(
                attempt=attempt,
                question=answer_data['question'],
                chosen_answer=chosen_answer,
                is_correct=is_correct
            )
        # Additional logic here to calculate total score, etc.
        return Response({"message": "Quiz submitted successfully"}, status=status.HTTP_201_CREATED)
    else:
        attempt.delete()  # Rollback the attempt if there's an error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QuizResultsView(RetrieveAPIView):
    serializer_class = QuizAttemptDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        quiz_id = self.kwargs.get("quiz_id")
        return QuizAttempt.objects.filter(student=self.request.user, quiz_id=quiz_id).last()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_grades(request):
    user = request.user
    attempts = QuizAttempt.objects.filter(student=user).annotate(
        total_questions=Count('quiz__questions'),
        correct_answers=Count(Case(When(submissions__is_correct=True, then=1), output_field=IntegerField())),
    ).values('quiz__title', 'timestamp', 'total_questions', 'correct_answers', 'quiz__topic__title', 'quiz__course__name')

    grades = [
        {
            'quizTitle': attempt['quiz__title'],
            'attemptDate': attempt['timestamp'].strftime('%Y-%m-%d'),
            'topic': attempt['quiz__topic__title'],
            'course': attempt['quiz__course__name'],
            'score': round((attempt['correct_answers'] / attempt['total_questions']) * 100, 2)
            if attempt['total_questions'] else 0
        } for attempt in attempts
    ]

    return Response(grades)
