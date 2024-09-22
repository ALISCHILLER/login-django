# accounts/views.py

# accounts/urls.py

from django.urls import path
from .views import SignupView, LoginView,VerifyTokenView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),

    path('verify-token/', VerifyTokenView.as_view(), name='verify_token'),
]
