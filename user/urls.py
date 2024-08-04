from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import JoinView, LoginView, ChangePasswordView, EncryptedUserView

urlpatterns = [
    path('join/', JoinView.as_view(), name='join'),
    path('login/', LoginView.as_view(), name='login'),
    path('google/', include('allauth.socialaccount.providers.google.urls')),
    path('kakao/', include('allauth.socialaccount.providers.kakao.urls')),
    path('account/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('account/', EncryptedUserView.as_view(), name='account'),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
]
