import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy

from bank.models import Bank, Declaration
from fruits.models import Fruit, Log
from users.models import Message


# Create your views here.
class MainView(LoginView):
    template_name = 'users/index.html'

    def get_redirect_url(self):
        return reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.datetime.now()
        context['fruits'] = Fruit.objects.all()
        context['messages'] = Message.objects.all()[:40][::-1]
        context['bank'] = Bank.objects.first()
        context['count_docs'] = len(Declaration.objects.filter(
            date__day=date.strftime('%d'),
            date__month=date.strftime('%m'),
            date__year=date.strftime('%Y'),
        ))
        context['logs'] = Log.objects.all()
        return context


class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'users/index.html'
    next_page = reverse_lazy('main')