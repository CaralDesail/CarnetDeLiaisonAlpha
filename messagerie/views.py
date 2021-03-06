from django.shortcuts import render
from .models import *
from tablecom.models import ChildSNotebook
from .forms import *
from .modulesATComplementaires import *
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import FormView
from django.utils import timezone
from django.contrib.messages.views import SuccessMessageMixin
from tablecom.views import GlobalCarrier
from notifications.modules_complementaires import notifDirectMessageAddOne,NotifMessagesReset

# Create your views here.
def messageAboutTo(request, id_carnet, id_correspondant):
    # print("Appel pour le carnet ",id_carnet, "et le correspondant ",id_correspondant)

    NotifMessagesReset(request,id_carnet,id_correspondant)


    ContactSel = User.objects.get(id=id_correspondant)


    # catch existing messages
    listeMessagesAT = list_AT_messages(request, id_carnet, id_correspondant)


    # answer form part
    premodel = MessagePersoAT(auteurID=request.user.pk, AttachedChildNotebookID=id_carnet, receiverID=id_correspondant)
    form = MessagePersoATForm(request.POST or None, instance=premodel)

    carnet = get_object_or_404(ChildSNotebook, id=id_carnet)

    if form.is_valid():
        print("Message Envoyé")
        envoi = True
        form.save()
        # call of notification put
        notifDirectMessageAddOne(request,id_carnet,id_correspondant)



    CarrierList=GlobalCarrier(request)#will carry all necessary variables (for notification, ...)

    return render(request, 'messagerie/messageAboutTo.html', locals())
