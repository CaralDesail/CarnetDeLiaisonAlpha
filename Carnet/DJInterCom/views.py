from django.shortcuts import render
from .models import *
from .forms import *
from .ModulesComplementaires import *

def home(request):
    print("Appel home")

    listeMessages=List_Messages_By_Access(request)


    return render(request,'DJInterCom/accueil.html',locals())


def new_MessagePerso(request):
    form = MessagePersoForm(request.POST or None)
    #print(form.Categorie_Professionnelle)
    id_of_current_user = request.user.pk
    premodel = MessagePerso(auteurID=id_of_current_user)
    form = MessagePersoForm(request.POST or None, instance=premodel)
    if form.is_valid():
        print("Message Envoyé")
        envoi=True
        form.save()
        lastEntryToAddinCorrespondanceTable(request)

    return render(request, 'DJInterCom/new_MessagePerso.html', locals())