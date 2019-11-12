from django.urls import path
from .views import (
    LoginView,
    SignUpView,
    login_view,
    index,
    logout_view,
    UserBankDetailView
)
urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', SignUpView.as_view()),
    path('', login_view, name='normal_login'),
    path('index/', index, name='index'),
    path('logout/', logout_view, name='logout'),
    path('bank/', UserBankDetailView.as_view())
]
