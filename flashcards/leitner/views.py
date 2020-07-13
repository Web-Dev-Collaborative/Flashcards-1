from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView

from flashcards.leitner.forms import BoxCreationForm, CardCreationForm
from flashcards.leitner.models import Deck, Box, Card


class DeckListView(LoginRequiredMixin, ListView):
    template_name = None  # Todo
    model = Deck
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        return self.request.user.decks.all()


class DeckCreationView(LoginRequiredMixin, CreateView):
    template_name = None  # Todo
    model = Deck
    fields = ('description',)
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class DeckDetailView(LoginRequiredMixin, CreateView):
    template_name = None  # Todo
    model = Deck
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        return self.request.user.decks.all()


class BoxCreationView(LoginRequiredMixin, View):
    # ToDo: Write the template
    template_name = None
    form_class = BoxCreationForm
    login_url = reverse_lazy('users:login')

    def get(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, pk=kwargs['deck_pk'], created_by=request.user)
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'deck': deck})

    def post(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, pk=kwargs['deck_pk'], created_by=request.user)
        form = self.form_class(request.POST)
        if form.is_valid():
            Box.objects.create(
                description=form.cleaned_data['description'],
                deck=deck
            )
        else:
            return render(request, self.template_name, {'form': form, 'deck': deck})


class BoxDetailView(LoginRequiredMixin, View):
    template_name = None  # Todo: Write this template
    login_url = reverse_lazy('users:login')

    def get(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, pk=kwargs['deck_pk'], created_by=request.user)
        box = get_object_or_404(Box, pk=kwargs['box_pk'], deck=deck)
        context = {'box': box, 'deck': deck}
        return render(request, self.template_name, context)


class CardCreationView(LoginRequiredMixin, View):
    form_class = CardCreationForm
    template_name = None  # Todo: Write this template
    login_url = reverse_lazy('users:login')

    def get(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, pk=kwargs['deck_pk'], created_by=request.user)
        form = self.form_class(deck)
        return render(request, self.template_name, {'form': form, 'deck': deck})

    def post(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, pk=kwargs['deck_pk'])
        form = self.form_class(deck, request.POST)
        if form.is_valid():
            Card.objects.create(
                front_text=form.cleaned_data['front_text'],
                back_text=form.cleaned_data['back_text'],
                on_box=form.cleaned_data['on_box'],
                on_deck=deck
            )
            messages.success(request, 'Card created successfully')
            return redirect('leitner:deck-detail', args=(deck.pk,))
        else:
            return render(request, self.template_name, {'form': form, 'deck': deck})
