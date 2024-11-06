from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .apps import UsersConfig
from .views import VerificationView, ErrorVerification, UserProfileView, UserManagerListView, \
    UserManagerProfileView, UserCreateView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('verification/', VerificationView.as_view(), name='verification'),
    path('verification/error/', ErrorVerification.as_view(), name='verification_error'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('users_list/', UserManagerListView.as_view(), name='users_list'),
    path('profile_manager/<int:pk>/', UserManagerProfileView.as_view(), name='profile_manager'),
    ]
