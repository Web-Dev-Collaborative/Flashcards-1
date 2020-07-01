from django.shortcuts import render
from django.views.generic import TemplateView


class FlashcardListView(TemplateView):
    template_name = 'flashes/list.html'


class FlashcardCreateView(TemplateView):
    template_name = 'flashes/create.html'
