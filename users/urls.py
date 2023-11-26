from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileUpdateView,
    PasswordChangeView,
    PasswordResetView,
    StudentGroupListView,
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('password/change/', PasswordChangeView.as_view(), name='password-change'),
    path('password/reset/', PasswordResetView.as_view(), name='password-reset'),
    path('student-groups/', StudentGroupListView.as_view(), name='student-groups'),
]
