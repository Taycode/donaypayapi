from django.urls import path
from .views import (
    CreateDonayPage,
    ViewDonayPage,
    CollectPayment,
    VerifyPayment
    )


urlpatterns = [
    path('create/', CreateDonayPage.as_view()),
    path('<int:pk>/', ViewDonayPage.as_view()),
    path('<int:pk>/pay/', CollectPayment.as_view()),
    path('<int:pk>/verify_pay/', VerifyPayment.as_view())
]
