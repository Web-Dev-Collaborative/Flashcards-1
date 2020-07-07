from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from flashcards.notes.models import Note


class NoteOwnerOnly:  # Is this kinda like a mixin?
    def get_queryset(self):
        return self.request.user.note_set.all()


class NoteListView(LoginRequiredMixin, ListView):
    template_name = 'notes/list.html'
    model = Note
    login_url = reverse_lazy('users:login')


class NoteCreateView(LoginRequiredMixin, CreateView):
    template_name = 'notes/createupdate.html'
    model = Note
    fields = ['title', 'content']
    login_url = reverse_lazy('users:login')
    extra_context = {'action': 'Create'}

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class NoteDetailView(LoginRequiredMixin, NoteOwnerOnly, DetailView):
    template_name = 'notes/detail.html'
    model = Note
    login_url = reverse_lazy('users:login')


class NoteUpdateView(LoginRequiredMixin, NoteOwnerOnly, UpdateView):
    model = Note
    fields = ['title', 'content']
    template_name = "notes/createupdate.html"
    login_url = reverse_lazy('users:login')
    extra_context = {'action': 'Update'}


class NoteDeleteView(LoginRequiredMixin, NoteOwnerOnly, DeleteView):
    model = Note
    success_url = reverse_lazy('notes:list')
    login_url = reverse_lazy('users:login')
    template_name = "notes/delete.html"
