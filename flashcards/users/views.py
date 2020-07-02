from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from .forms import LoginForm, SignupForm


class LoginView(View):
    # TODO: Next time, using AuthenticationForm could be a better idea
    form_class = LoginForm
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password'])
            if user is not None:  # Valid username and password
                login(request, user)
                return HttpResponseRedirect('/account/')
            else:  # User does not exist, wrong password or access denied
                return HttpResponseRedirect('/account/login')


class SignupView(View):
    form_class = SignupForm
    template_name = 'users/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.create_user()
            return HttpResponseRedirect('/account/login/')
        else:  # Invalid form
            return HttpResponseRedirect('/account/signup/')


class UserDetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'users/details.html'
    login_url = '/account/login'


class LogoutView(LoginRequiredMixin, View):
    template_name = 'users/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, self.template_name)
