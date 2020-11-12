from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import ModelForm, Textarea


class MessagePersoATForm(forms.ModelForm):
    class Meta :
        model = MessagePersoAT
        #fields = '__all__'
        fields = ('contenu',)
        widgets = {
          'contenu': Textarea(attrs={'rows':5, 'cols':40}),
        }