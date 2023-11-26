from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileUpdateSerializer,
    PasswordChangeSerializer,
    PasswordResetSerializer,
    StudentGroupSerializer
)
from .models import StudentGroup

User = get_user_model()
MAX_LOGIN_ATTEMPTS = 5  # Maximum failed attempts
LOCKOUT_TIME = 30  # Lockout time in minutes

def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token_data = serializer.get_tokens_for_user(user)
            user_data = serializer.data
            user_data.update(token_data)
            return Response({
                "user": user_data, 
                "access": token_data['access'],
                "refresh": token_data['refresh']
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data
            if user.is_account_locked():
                return Response({"message": "Account is locked. Try again later."}, status=status.HTTP_403_FORBIDDEN)

            # Reset failed login attempts after successful login
            user.failed_login_attempts = 0
            user.lockout_until = None
            user.save()

            token_data = generate_tokens_for_user(user)
            return Response({
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "user_type": user.user_type,
                    "student_group": user.student_group_id,
                },
                "access": token_data['access'],
                "refresh": token_data['refresh']
            }, status=status.HTTP_200_OK)

        else:
            email = request.data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= MAX_LOGIN_ATTEMPTS:
                    user.lockout_until = make_aware(datetime.now() + timedelta(minutes=LOCKOUT_TIME))
                user.save()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset e-mail has been sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StudentGroupListView(generics.ListAPIView):
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer