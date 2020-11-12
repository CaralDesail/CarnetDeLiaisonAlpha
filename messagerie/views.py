from django.shortcuts import render
from .models import *
from .forms import *
from .modulesATComplementaires import *
from django.views.generic import FormView
from django.utils import timezone
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
def messageAboutTo(request, id_carnet, id_correspondant):
    # print("Appel pour le carnet ",id_carnet, "et le correspondant ",id_correspondant)

    ContactSel = User.objects.get(id=id_correspondant)


    # catch existing messages
    listeMessagesAT = list_AT_messages(request, id_carnet, id_correspondant)


    # answer form part
    form = MessagePersoATForm(request.POST or None)
    premodel = MessagePersoAT(auteurID=request.user.pk, AttachedChildNotebookID=id_carnet, receiverID=id_correspondant)
    form = MessagePersoATForm(request.POST or None, instance=premodel)

    if form.is_valid():
        print("Message Envoyé")
        envoi = True
        form.save()

    return render(request, 'messagerie/messageAboutTo.html', locals())
