from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class ProCreatForm(UserCreationForm):
    Categorie_Professionnelle = forms.ModelChoiceField(queryset=CategoriePro.objects.all())
    Identifiant_Professionnel = forms.CharField(max_length=30, required=True)
    Telephone = forms.CharField(max_length=30, required=True)
    class Meta :
        model = User
        #fields = '__all__'
        fields = ('username', 'first_name','last_name','email',)

    def save(self, commit=True):
     if not commit:
      raise NotImplementedError("Can't create User and UserProfile without database save")
     user = super(ProCreatForm, self).save(commit=True)
     user_profile = Profil(user=user, rolePro=self.cleaned_data['Categorie_Professionnelle'],
      num_ident=self.cleaned_data['Identifiant_Professionnel'],
      phone=self.cleaned_data['Telephone'])
     user_profile.save()
     return user, user_profile

class RLCreatForm(UserCreationForm):
    Statut_Responsable_Legal = forms.CharField(max_length=30, required=True)
    Identifiant_Personnel_Unique = forms.CharField(max_length=30, required=True)
    Telephone = forms.CharField(max_length=30, required=True)
    class Meta :
        model = User
        #fields = '__all__'
        fields = ('username', 'first_name','last_name','email',)

    def save(self, commit=True):
     if not commit:
      raise NotImplementedError("Can't create User and UserProfile without database save")
     user = super(RLCreatForm, self).save(commit=True)
     user_profile = Profil(user=user, statusRL=self.cleaned_data['Statut_Responsable_Legal'],
      num_ident=self.cleaned_data['Identifiant_Personnel_Unique'],
      phone=self.cleaned_data['Telephone'])
     user_profile.save()
     return user, user_profile

class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

class NewArticleForm(forms.ModelForm):
    class Meta :
        model = Article
        #fields = '__all__'
        fields = ('title', 'content','list_to_notify',)

class ChildSNotebookCreatForm(forms.ModelForm):
    class Meta:
        model = ChildSNotebook
        #fields = '__all__'
        fields = ('name','forename','date_of_birth','num_ident')

class ContactUsForm(forms.ModelForm):
    class Meta:
        model=ContactUs
        fields = '__all__'
