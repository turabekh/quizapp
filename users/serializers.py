from django.contrib.auth.forms import PasswordResetForm
from rest_framework import serializers
from django.contrib.auth import (
    get_user_model, 
    authenticate,
    password_validation
)
from rest_framework_simplejwt.tokens import RefreshToken
from .models import StudentGroup  # Import the StudentGroup model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    student_group = serializers.PrimaryKeyRelatedField(
        queryset=StudentGroup.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'student_group')

    def create(self, validated_data):
        student_group = validated_data.pop('student_group', None)
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            user_type=1,  # Default to student
            student_group=student_group
        )
        return user

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'profile_image', 'student_group')
        extra_kwargs = {
            'profile_image': {'required': False},
            'student_group': {'required': False},
            'phone_number': {'required': False},
        }

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value
    
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)

    def validate_email(self, value):
        # Create Password Reset Form to validate email
        self.reset_form = PasswordResetForm(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError("Error in password reset form.")
        return value

    def save(self):
        request = self.context.get('request')
        # Use the form's save method to generate the token and send the email
        self.reset_form.save(
            use_https=request.is_secure(),
            from_email=None,
            request=request,
            email_template_name='password_reset_email.html'
        )

class StudentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGroup
        fields = ['id', 'name']