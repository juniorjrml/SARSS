from django import forms
from django.forms import Textarea, TextInput


from .models import Feed

class tagForm(forms.ModelForm):

    class Meta:
        model = Feed
        fields = ('title',)
        widgets = {
            'link': TextInput(attrs={'width': 300, 'class': "form-control", "placeholder": "Digite o Nome da Tag"}),
        }
