from django import forms
from django.forms import Textarea, TextInput


from .models import Feed

class FeedForm(forms.ModelForm):

    class Meta:
        model = Feed
        fields = ('link',)
        widgets = {
            'link': TextInput(attrs={'width': 300}),
        }
