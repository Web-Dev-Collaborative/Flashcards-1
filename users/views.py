from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = 'users/login.html'


class SignupView(TemplateView):
    template_name = 'users/signup.html'


class UserDetailsView(TemplateView):
    template_name = 'users/details.html'