from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

from .managers import CustomUserManager


class StudentGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    courses_taught = models.ManyToManyField('courses.Course', related_name='course_teachers', blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    lockout_until = models.DateTimeField(null=True, blank=True)

    def is_account_locked(self):
        if self.lockout_until and datetime.now() < self.lockout_until:
            return True
        return False
    # Define user types
    USER_TYPE_CHOICES = (
        (1, 'student'),
        (2, 'teacher'),
        (3, 'admin'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    student_group = models.ForeignKey(
        StudentGroup, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='students'
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
