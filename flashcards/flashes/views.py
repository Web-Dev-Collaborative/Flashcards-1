from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views.generic import CreateView, ListView, DetailView
from flashcards.flashes.models import Flash


class FlashcardListView(LoginRequiredMixin, ListView):
    login_url = '/account/login'
    template_name = 'flashes/list.html'
    model = Flash


class FlashcardDetailView(LoginRequiredMixin, DetailView):
    login_url = '/account/login'
    template_name = 'flashes/detail.html'
    model = Flash
    
    def get_queryset(self):
        """Only allows the creator to see the flashcard"""
        qs = super().get_queryset().filter(created_by=self.request.user)
        return qs


class FlashcardCreateView(LoginRequiredMixin, CreateView):
    login_url = '/account/login'
    template_name = 'flashes/create.html'
    model = Flash
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.last_change_date = datetime.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('flashes:list')
