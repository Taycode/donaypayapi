from django.urls import path
from .views import (
    CreateDonayPage,
    ViewDonayPage,
    CollectPayment,
    VerifyPayment,
    ViewAllDonayPages
    )


urlpatterns = [
    path('create/', CreateDonayPage.as_view()),
    path('<int:pk>/', ViewDonayPage.as_view()),
    path('<int:pk>/pay/', CollectPayment.as_view()),
    path('<int:pk>/verify_pay/', VerifyPayment.as_view()),
    path('all/', ViewAllDonayPages.as_view())
]
