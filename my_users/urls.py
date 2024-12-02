from django.urls import path
from .views import AuthView, VerifyCodeView, ProfileView


urlpatterns = [
    path('auth/', AuthView.as_view(), name='auth'),
    path('verify/', VerifyCodeView.as_view(), name='verify'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
]