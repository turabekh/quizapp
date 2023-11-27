from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import (
    Course, Enrollment,
    Quiz, Question, 
    AnswerChoice, Topic,
    AnswerSubmission,
    QuizAttempt,
    AssessmentCriteria,
)


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name']


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['course', 'date_enrolled']

class AssessmentCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentCriteria
        fields = ['id', 'criteria', 'criteria_type']

class CourseWithEnrollmentSerializer(serializers.ModelSerializer):
    is_enrolled = serializers.BooleanField()
    teacher = TeacherSerializer(read_only=True)  # Nested serializer for the teacher
    assessment_criteria = AssessmentCriteriaSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'description', 
            'academic_year', 'is_enrolled', 
            'teacher', 'semester', 'active',
            'learning_outcomes', 'assessment_criteria'
            ]


class AnswerChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerChoice
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    choices = AnswerChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'choices']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'questions']

class TopicSerializer(serializers.ModelSerializer):
    quizzes = QuizSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'title', 'description', 'quizzes']

class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)
    topics = TopicSerializer(many=True, read_only=True)
    assessment_criteria = AssessmentCriteriaSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = [
            'id', 'name', 'description', 
            'academic_year', 'semester', 
            'active', 'teacher', 'topics',
            'learning_outcomes', 'assessment_criteria',
            ]


class AnswerChoiceSerializer2(serializers.ModelSerializer):
    class Meta:
        model = AnswerChoice
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer2(serializers.ModelSerializer):
    choices = AnswerChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'choices']

class QuizSerializer2(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'questions']

class AnswerSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerSubmission
        fields = ['question', 'chosen_answer']

class AnswerSubmissionSerializer2(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    chosen_answer = AnswerChoiceSerializer(read_only=True)
    class Meta:
        model = AnswerSubmission
        fields = ['question', 'chosen_answer']


class QuizAttemptDetailSerializer(serializers.ModelSerializer):
    submissions = AnswerSubmissionSerializer2(many=True, read_only=True)

    class Meta:
        model = QuizAttempt
        fields = ['id', 'quiz', 'timestamp', 'submissions']

