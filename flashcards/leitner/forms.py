from django import forms

from flashcards.leitner.models import Box, Card


class BoxCreationForm(forms.Form):
    description = forms.CharField(label='Box description', max_length=150)

    class Meta:
        model = Box
        fields = ('description',)


class CardCreationForm(forms.Form):
    front_text = forms.CharField(label='Front text', max_length=150)
    back_text = forms.CharField(widget=forms.Textarea, label='Back text')
    on_box = forms.ModelChoiceField(label='Where to place this card?', queryset=Box.objects.none())

    class Meta:
        model = Card
        fields = [
            'front_text',
            'back_text',
            'on_box'
        ]

    # Note to myself: Read this link if you don't remember what is going on here
    # https://simpleisbetterthancomplex.com/questions/2017/03/22/how-to-dynamically-filter-modelchoices-queryset-in-a-modelform.html
    # I have no idea how to test this form tho....
    def __init__(self, deck, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['on_box'].queryset = Box.objects.filter(deck=deck)
