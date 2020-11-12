
from django.urls import path
from . import views

urlpatterns = [
    path('', views.BotView.as_view(), name='chatbot')
]
