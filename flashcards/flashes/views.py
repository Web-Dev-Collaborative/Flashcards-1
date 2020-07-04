from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView

from flashcards.flashes.models import Flash


class FlashcardListView(LoginRequiredMixin, ListView):
    template_name = 'flashes/list.html'
    model = Flash

    def get_login_url(self):
        return reverse('users:login')


class FlashcardDetailView(LoginRequiredMixin, DetailView):
    template_name = 'flashes/detail.html'
    model = Flash

    def get_queryset(self):
        """Only allows the creator to see the flashcard"""
        # Can also filter from the model
        return super().get_queryset().filter(created_by=self.request.user)

    def get_login_url(self):
        return reverse('users:login')


class FlashcardCreateView(LoginRequiredMixin, CreateView):
    template_name = 'flashes/create.html'
    model = Flash
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('flashes:list')

    def get_login_url(self):
        return reverse('users:login')
