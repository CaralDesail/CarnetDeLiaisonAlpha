from .models import *
from django.contrib.auth.models import Permission, User


def list_AT_messages(request, id_carnet, id_correspondant):
    # print("Request : ",request," id carnet ",id_carnet," id correspondant ",id_correspondant)

    QueryMessagesFiltred = MessagePersoAT.objects.filter(AttachedChildNotebookID=id_carnet)

    ListMessagesFiltred = []
    for MessageATFiltred in QueryMessagesFiltred:
        # print("Message trouvé: ", MessageATFiltred.contenu, " adressé par ",MessageATFiltred.auteurID, " recu par ",
        #      MessageATFiltred.receiverID)

        #if message is not validated par RL
        if MessageATFiltred.validated != True:
            continue
        #if message is inactive (deleted, etc ...)
        if MessageATFiltred.activeMessage != True :
            continue

        # the two following will filter if id correspondant and user are each in emiter ou receiver ...
        if id_correspondant != MessageATFiltred.auteurID and id_correspondant != MessageATFiltred.receiverID:
            #    print ("Break car on cherche un id correspondant ",id_correspondant, " dans Auteur ou Receiver")
            continue
        if request.user.pk != int(MessageATFiltred.auteurID) and request.user.pk != int(MessageATFiltred.receiverID):
            #    print ("Break car on cherche un request.user n° ",request.user.pk, " dans Auteur ou Receiver")
            continue

        # we add status if user is emiter or receiver
        if int(MessageATFiltred.auteurID) == int(request.user.pk):
            #print("yes !")
            MessageATFiltred.isAuteur = True
        else:
            #print("no ! ")
            MessageATFiltred.isAuteur = False

        ListMessagesFiltred.append(MessageATFiltred)

    return ListMessagesFiltred
