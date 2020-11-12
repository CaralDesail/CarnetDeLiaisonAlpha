from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class MessagePersoATForm(forms.ModelForm):
    class Meta :
        model = MessagePersoAT
        #fields = '__all__'
        fields = ('contenu',)
