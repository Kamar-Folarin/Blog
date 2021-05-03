from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (LoginFormView, RegisterView, ProfileListView, ProfileUpdateView,
                    activate, change_email, PasswordResetPageView, PasswordDoneView, PasswordConfirmView, PasswordCompleteView)

urlpatterns = [
    path('login/', LoginFormView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('profile/', ProfileListView.as_view(), name="profile"),
    path('profile/<int:pk>/update/', ProfileUpdateView.as_view(), name="profile-update"),
    path('activate/<str:email>/<uidb64>/<token>/', change_email, name='change-email'),
    path('password-reset/', PasswordResetPageView.as_view(), name="password_reset"),
    path('password-reset/done/', PasswordDoneView.as_view(), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordConfirmView.as_view(), name="password_reset_confirm"),
    path('password-reset-complete/', PasswordCompleteView.as_view(), name="password_reset_complete"),
]
