from django.shortcuts import render
from django.views.generic import TemplateView
from users.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin


class ChatUserView(TemplateView):
    template_name = "chat/room.html"

    def get(self, request):
        x = CustomUser.objects.values()
        return render(request, self.template_name, {"data": x})


class PrivateChatView(TemplateView):
    template_name = "chat/chat.html"

    def get(self, request, other):

        return render(request, self.template_name, {"other": other})
