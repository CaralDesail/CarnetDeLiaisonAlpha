from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django_select2.forms import  Select2MultipleWidget
from .ModulesComplementaires import listProRLPerso

CorrespondantUsers = listProRLPerso(0)


class MessagePersoForm(forms.ModelForm):
    class Meta :
        model = MessagePerso
        #fields = '__all__'
        fields = ('titre','contenu')


class Message_SW(forms.Form):
    correspondants = forms.MultipleChoiceField(widget=Select2MultipleWidget, choices=CorrespondantUsers, required=False, label="Correspondants")
    titre = forms.CharField(label="Titre", max_length=400)
    contenu = forms.CharField(widget=forms.Textarea)

