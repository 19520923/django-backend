from django.urls import path
from .views import *

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name = 'register'),
    path('auth/email-verify/', VerifyEmailView.as_view(), name = 'email-verify'),
    path('auth/login', LoginView.as_view(), name = 'login'),
    path('auth/logout', LogoutView.as_view(), name = 'logout'),
    path('user/user_search/', UserSearchListView.as_view(), name = 'user_search'),
    path('user/user_list/<int:id>', UserDetailView.as_view(), name = 'user_detail'),
    path('user/user_unactivate', UserUnactiveView.as_view(), name = 'user_unactivate'),
    path('user/user_follower_list', UserFollowerListView.as_view(), name = 'user_follower'),
    path('user/unfollow', UnfollowView.as_view(), name = 'unfollow')
]