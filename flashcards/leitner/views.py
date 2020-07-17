from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import DeleteView

from flashcards.leitner.forms import CardCreationForm, DeckCreationForm, CardUpdateForm, \
    SessionSelectBoxForm
from flashcards.leitner.models import Deck, Card, Session


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
            deck = Deck.objects.create(description=form.cleaned_data['description'], created_by=request.user)
            deck.create_boxes()
            messages.success(request, 'Deck created successfully')
        else:
            messages.warning(request, 'Could not create the deck, make sure the field was not empty')
        return redirect('leitner:deck-list')


class DeckDetailView(LoginRequiredMixin, View):
    template_name = 'leitner/deckdetailview.html'
    login_url = reverse_lazy('users:login')

    def get(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, pk=kwargs['deck_pk'], created_by=request.user)
        boxes = deck.boxes.order_by('box_type')
        return render(request, self.template_name, {'deck': deck, 'boxes': boxes})


class DeckDeleteView(LoginRequiredMixin, DeleteView):
    model = Deck
    success_url = reverse_lazy('leitner:deck-list')
    template_name = "leitner/deckdeleteview.html"
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        return self.request.user.decks.all()


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
        return redirect('leitner:deck-detail', deck.pk)


class CardDeleteView(LoginRequiredMixin, View):
    template_name = "leitner/carddelete.html"
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


class SessionStartView(LoginRequiredMixin, View):
    """ View to create a study session """
    template_name = "leitner/session/start_session.html"
    login_url = reverse_lazy('users:login')
    form = SessionSelectBoxForm

    def get(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, pk=kwargs['deck_pk'], created_by=request.user)
        if deck.session.exists():
            if deck.session.get().is_finished:
                return redirect('leitner:session-finished', deck.pk)
            return redirect('leitner:session-cards', deck.pk)
        form = self.form(deck)
        return render(request, self.template_name, {'form': form, 'deck': deck})

    def post(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, pk=kwargs['deck_pk'], created_by=request.user)
        if deck.session.exists():
            return HttpResponseNotFound
        form = self.form(deck, request.POST)
        if form.is_valid():
            box = form.cleaned_data['current_box']
            if box.cards.count() == 0:
                messages.warning(request, 'The selected box is empty, use another')
                return redirect('leitner:session', deck.pk)
            box.in_session = True
            box.save()
            Session.objects.create(deck=deck, current_box=box,
                                   total_cards_on_box=box.cards.count(),
                                   is_finished=False)
            messages.success(request, 'Session started!')
        else:
            messages.warning(request, 'Could not start session, try again')
        return redirect('leitner:session', deck.pk)


class SessionCardsView(LoginRequiredMixin, View):
    """ View that shows every card from the selected box """
    template_name = 'leitner/session/study_session.html'
    login_url = reverse_lazy('users:login')

    def get(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, pk=kwargs['deck_pk'], created_by=request.user)
        if not deck.session.exists():
            return redirect('leitner:session', deck.pk)
        if (session := deck.session.get()).is_finished:
            return redirect('leitner:session-finished', deck.pk)
        if (card := session.current_card()) is not None:
            return render(request, self.template_name, {'card': card, 'deck': deck})
        session.is_finished = True
        session.save()
        return redirect('leitner:session-finished', deck.pk)

    def post(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, pk=kwargs['deck_pk'], created_by=request.user)
        if not deck.session.exists() or deck.session.get().is_finished:
            return HttpResponseNotFound
        session = deck.session.get()
        if (card := session.current_card()) is not None:
            if '_correct' in request.POST:
                card.correct_answer()
                messages.success(request, 'Got it! That\'s a correct answer!')
                return redirect('leitner:session-cards', deck.pk)
            elif '_incorrect' in request.POST:
                card.wrong_answer()
                messages.success(request, 'Dang :( Keep going and you\'ll get it next time!')
                return redirect('leitner:session-cards', deck.pk)
            else:
                return HttpResponseNotFound
        return redirect('leitner:session-finished', deck.pk)


class SessionFinishedView(LoginRequiredMixin, View):
    """ View to finish the study session """
    template_name = "leitner/session/finished_session.html"
    login_url = reverse_lazy('users:login')

    def get(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, pk=kwargs['deck_pk'], created_by=request.user)
        if not deck.session.exists():
            return redirect('leitner:session', deck.pk)
        if not deck.session.get().is_finished:
            return redirect('leitner:session-cards', deck.pk)
        return render(request, self.template_name, {'session': deck.session.get()})

    def post(self, request, *args, **kwargs):
        deck = get_object_or_404(Deck, pk=kwargs['deck_pk'], created_by=request.user)
        if not deck.session.exists():
            return HttpResponseNotFound
        elif not deck.session.get().is_finished:
            return HttpResponseNotFound
        session = deck.session.get()
        box = session.current_box
        box.last_used = timezone.now()
        box.in_session = False
        box.save()
        session.delete()
        messages.success(request, 'Study session finished!')
        return redirect('leitner:deck-detail', deck.pk)
