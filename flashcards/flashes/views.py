from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from flashcards.flashes.models import Flash


class FlashcardOwnerOnly:  # Is this kinda like a mixin?
    def get_queryset(self):
        return self.request.user.flash_set.all()


class FlashcardListView(LoginRequiredMixin, ListView):
    template_name = 'flashes/list.html'
    model = Flash
    login_url = reverse_lazy('users:login')


class FlashcardCreateView(LoginRequiredMixin, CreateView):
    template_name = 'flashes/createupdate.html'
    model = Flash
    fields = ['title', 'content']
    login_url = reverse_lazy('users:login')
    extra_context = {'action': 'Create'}

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class FlashcardDetailView(LoginRequiredMixin, FlashcardOwnerOnly, DetailView):
    template_name = 'flashes/detail.html'
    model = Flash
    login_url = reverse_lazy('users:login')


class FlashcardUpdateView(LoginRequiredMixin, FlashcardOwnerOnly, UpdateView):
    model = Flash
    fields = ['title', 'content']
    template_name = "flashes/createupdate.html"
    login_url = reverse_lazy('users:login')
    extra_context = {'action': 'Update'}


class FlashcardDeleteView(LoginRequiredMixin, FlashcardOwnerOnly, DeleteView):
    model = Flash
    success_url = reverse_lazy('flashes:list')
    login_url = reverse_lazy('users:login')
    template_name = "flashes/delete.html"
