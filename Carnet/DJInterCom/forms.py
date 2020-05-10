from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class MessagePersoForm(forms.ModelForm):
    class Meta :
        model = MessagePerso
        #fields = '__all__'
        fields = ('titre','contenu')


