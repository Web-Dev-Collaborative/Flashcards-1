from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from .forms import CreateAccountForm


class SignupView(View):
    form_class = CreateAccountForm
    template_name = 'users/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/account/login/')
        else:  # Invalid form
            return HttpResponseRedirect('/account/signup/')


class UserDetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'users/details.html'
    login_url = reverse_lazy('users:login')
