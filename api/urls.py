from django.urls import path
from .views import FarmerListAPIView,FarmerSummaryAPIView,BotUserCheckAPIView

urlpatterns = [
    path("farmers/", FarmerListAPIView.as_view(), name="api_farmers"),
    path("farmers/summary/", FarmerSummaryAPIView.as_view()),
    path("bot-user/check/", BotUserCheckAPIView.as_view()), 
]
