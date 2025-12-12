
from django.urls import path

from . import views


urlpatterns = [
    path('demo/v1/chat/completions', views.DemoChatCompletionView.as_view(), name='demo_chat_completions'),
]
