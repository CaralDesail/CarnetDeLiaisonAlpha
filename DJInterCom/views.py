from django.shortcuts import render
from .models import *
from .forms import *
from .ModulesComplementaires import *
from django.views.generic import FormView
from django.utils import timezone
from django.contrib.messages.views import SuccessMessageMixin



class TemplateNewMessageFormView(SuccessMessageMixin,FormView):
    template_name = 'DJInterCom/form.html'
    success_url = 'accueilMessager'
    success_message = "Message envoyé"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        #print("ok valide, valeurs : ",form.cleaned_data["titre"])
        correspondantsIDtemp=form.cleaned_data["correspondants"]
        correspondantsID=";".join(correspondantsIDtemp)
        titre=form.cleaned_data["titre"]
        contenu=form.cleaned_data["contenu"]
        timeNdate=timezone.now()
        userid=self.request.user.id

        newEntryMessage=MessagePerso(auteurID=userid,titre=titre,contenu=contenu,accessUserID=correspondantsID,date=timeNdate)
        newEntryMessage.save()

        lastEntryToAddinCorrespondanceTable(self.request)

        return super().form_valid(form)


def home(request):
    print("Appel home")

    #from ModulesComplementaires
    listeMessages=list_messages_by_access(request)

    try:
        groupQS = request.user.groups.all()
        userGroupName = groupQS[0].name
        print("User group = ", userGroupName)

    except :
        print("userAnonymous ou sans groupe")
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

def messageAboutTo(request,id_carnet,id_correspondant):
    print("A propos du carnet ", id_carnet, " et du correspondant ",id_correspondant )
    return render(request,'DJInterCom/accueil.html',locals())