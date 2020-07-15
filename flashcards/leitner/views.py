from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView

from flashcards.leitner.forms import BoxCreationForm, CardCreationForm, DeckCreationForm, CardUpdateForm, \
    SessionSelectBoxForm
from flashcards.leitner.models import Deck, Box, Card, Session


class DeckListView(LoginRequiredMixin, View):
    template_name = "leitner/decklistview.html"
    login_url = reverse_lazy('users:login')
    form_class = DeckCreationForm

    def get(self, request, *args, **kwargs):
        decks_qs = request.user.decks.all()
        form = self.form_class()
        return render(request, self.template_name, {'decks': decks_qs, 'form': form})

    def post(self, request, *args, **kwargs):
        # This is used to create a box in the same view
        form = self.form_class(request.POST)
        if form.is_valid():
            Deck.objects.create(
                description=form.cleaned_data['description'],
                created_by=request.user
            )
            messages.success(request, 'Deck created successfully')
        else:
            messages.warning(request, 'Could not create the deck, make sure the field was not empty')
        return redirect('leitner:deck-list')


class DeckDetailView(LoginRequiredMixin, DetailView):
    template_name = "leitner/deckdetailview.html"
    model = Deck
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        return self.request.user.decks.all()


class BoxCreationView(LoginRequiredMixin, View):
    template_name = "leitner/boxcreationview.html"
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
            messages.success(request, 'Box created succesfully')
            return redirect("leitner:deck-detail", deck.pk)
        else:
            return render(request, self.template_name, {'form': form, 'deck': deck})


class BoxDetailView(LoginRequiredMixin, View):
    template_name = "leitner/boxdetailview.html"
    login_url = reverse_lazy('users:login')

    def get(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, pk=kwargs['deck_pk'], created_by=request.user)
        box = get_object_or_404(Box, pk=kwargs['box_pk'], deck=deck)
        context = {'box': box, 'deck': deck}
        return render(request, self.template_name, context)


class CardCreationView(LoginRequiredMixin, View):
    form_class = CardCreationForm
    template_name = "leitner/cardcreationview.html"
    login_url = reverse_lazy('users:login')

    def get(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, pk=kwargs['deck_pk'], created_by=request.user)
        form = self.form_class(deck)
        return render(request, self.template_name, {'form': form, 'deck': deck, 'action': 'Create'})

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
            return redirect('leitner:deck-detail', deck.pk)
        else:
            messages.warning(request, 'Could not create the card, try again')
            return render(request, self.template_name, {'form': form, 'deck': deck})


class CardListView(LoginRequiredMixin, View):
    template_name = "leitner/cardlistview.html"
    login_url = reverse_lazy('users:login')

    def get(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, pk=kwargs['deck_pk'], created_by=request.user)
        return render(request, self.template_name, {'cards': (deck.cards.all()), 'deck': deck})


class CardUpdateView(LoginRequiredMixin, View):
    template_name = "leitner/cardcreationview.html"
    form_class = CardUpdateForm
    login_url = reverse_lazy('users:login')

    def get(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, pk=kwargs['deck_pk'], created_by=request.user)
        card = get_object_or_404(Card, pk=kwargs['card_pk'], on_deck=deck)
        initial_form = {'front_text': card.front_text, 'back_text': card.back_text}
        form = self.form_class(initial=initial_form)
        return render(request, self.template_name, {'form': form, 'card': card, 'deck': deck, 'action': 'Edit'})

    def post(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, pk=kwargs['deck_pk'], created_by=request.user)
        card = get_object_or_404(Card, pk=kwargs['card_pk'], on_deck=deck)
        initial_form = {'front_text': card.front_text, 'back_text': card.back_text}
        form = self.form_class(request.POST, initial=initial_form)
        if form.is_valid() and form.has_changed():
            card.front_text = form.cleaned_data['front_text']
            card.back_text = form.cleaned_data['back_text']
            card.save()
            messages.success(request, 'Card modified correctly')
        else:
            messages.warning(request, 'No changes have been made to the card')
        return redirect('leitner:card-list', deck.pk)


class CardDeleteView(LoginRequiredMixin, View):
    template_name = "letner/carddelete.html"
    login_url = reverse_lazy('users:login')

    def get(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, pk=kwargs['deck_pk'], created_by=request.user)
        card = get_object_or_404(Card, pk=kwargs['card_pk'], on_deck=deck)
        return render(request, self.template_name, {'card': card, 'deck': deck})

    def post(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, pk=kwargs['deck_pk'], created_by=request.user)
        card = get_object_or_404(Card, pk=kwargs['card_pk'], on_deck=deck)
        card.delete()
        messages.success(request, 'Card deleted successfully')
        return redirect('leitner:deck-detail', deck.pk)


class StudySession(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')
    start_session_template = None
    study_session_template = None
    session_finished_template = None
    select_box_form = SessionSelectBoxForm

    def get(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, pk=kwargs['deck_pk'], created_by=request.user)
        if not deck.session.exists():
            form = self.select_box_form(deck)
            return render(request, self.start_session_template, {'deck': deck, 'form': form})
        else:
            session = deck.session.get()
            if not session.is_finished:
                box = session.current_box
                return render(request, self.study_session_template, {'deck': deck, 'session': session, 'box': box})
            return render(request, self.session_finished_template, {'deck': deck, 'session': session})

    def post(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, pk=kwargs['deck_pk'], created_by=request.user)
        if not deck.session.exists():
            # Todo: Create a form to select a box to use, update the box to reflect it is currently in use
            form = self.select_box_form(deck, request.POST)
            if form.is_valid():
                Session.objects.create(

                )
