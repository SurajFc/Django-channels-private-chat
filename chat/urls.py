from django.urls import path
from .views import (
    ChatUserView, PrivateChatView
)

app_name = 'chat'
urlpatterns = [
    path("mychats", ChatUserView.as_view(), name="mychat"),
    path('<int:other>', PrivateChatView.as_view(), name="pchat")
]
