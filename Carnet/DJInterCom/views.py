from django.shortcuts import render
from .models import *
from .forms import *
from .ModulesComplementaires import *

def home(request):
    print("Appel home")

    listeMessages=List_Messages_By_Access(request)
    try:
        groupQS = request.user.groups.all()
        userGroupName = groupQS[0].name
        print("User group = ", userGroupName)

    except :
        print("userAnonymous")
        userGroupName = ""

    return render(request,'DJInterCom/accueil.html',locals())


def new_MessagePerso(request):

    #print(form.Categorie_Professionnelle)
    id_of_current_user = request.user.pk
    idCarnet = 0
    listProRLToPrint = listProRLPerso(idCarnet)  # set idCarnet to 0 for all registred users access
    print(listProRLToPrint)
    form = MessagePersoForm(request.POST or None)
    premodel = MessagePerso(auteurID=id_of_current_user)
    form = MessagePersoForm(request.POST or None, instance=premodel)

    if form.is_valid():
        print("Message Envoyé")
        envoi=True
        form.save()
        lastEntryToAddinCorrespondanceTable(request)

    return render(request, 'DJInterCom/new_MessagePerso.html', locals())