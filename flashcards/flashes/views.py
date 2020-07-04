from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from flashcards.flashes.models import Flash


class FlashcardListView(LoginRequiredMixin, ListView):
    template_name = 'flashes/list.html'
    model = Flash
    login_url = reverse_lazy('users:login')


class FlashcardDetailView(LoginRequiredMixin, DetailView):
    template_name = 'flashes/detail.html'
    model = Flash
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        """Only allows the creator to see the flashcard"""
        # Can also filter from the model
        return super().get_queryset().filter(created_by=self.request.user)


class FlashcardCreateView(LoginRequiredMixin, CreateView):
    template_name = 'flashes/create.html'
    model = Flash
    fields = ['title', 'content']
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class FlashcardUpdateView(LoginRequiredMixin, UpdateView):
    model = Flash
    fields = ['title', 'content']
    template_name = "flashes/create.html"
    login_url = reverse_lazy('users:login')


class FlashcardDeleteView(LoginRequiredMixin, DeleteView):
    model = Flash
    success_url = reverse_lazy('flashes:list')
    login_url = reverse_lazy('users:login')
    template_name = "flashes/delete.html"
