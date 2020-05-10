from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from datetime import datetime
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import Permission, User
from django.contrib.auth.decorators import permission_required



def List_Messages_By_Access(request):
    myPk=request.user.id
    listeMessages = MessagePerso.objects.all()
    IDListAllow=CorrespondanceTableMessagesByUser.objects.get(idUser=myPk).messagesAccess
    print(IDListAllow)
    listOfDiffID=IDListAllow.split(";")
    print(listOfDiffID)
    list_to_return=[]
    for messageID in listOfDiffID:
        try:
            CorrespondingMessage=MessagePerso.objects.get(id=messageID)
            autorID=CorrespondingMessage.auteurID
            CorrespondingMessage.auteur_first_name=User.objects.get(pk=autorID).first_name
            CorrespondingMessage.auteur_last_name=User.objects.get(pk=autorID).last_name
            list_to_return.append(CorrespondingMessage)
        except :
            print("Message {} non trouvé".format(messageID))
    return list_to_return

def correspondanceTableMessages_check(request): # will check if corresponding item in correspondance table exist, if not create
    liste_new=[]
    for userSel in User.objects.all():
        pkSel=userSel.pk
        print(pkSel)
        try:
            carnet = CorrespondanceTableMessagesByUser.objects.get(idUser=pkSel)
            print(carnet)
        except:
            print("pas trouvé")
            newEntry=CorrespondanceTableMessagesByUser(idUser=pkSel)
            newEntry.save()
            liste_new.append(pkSel)

    return HttpResponse("Table verifiee, nouvelle ligne pour users :",liste_new)

def lastEntryToAddinCorrespondanceTable(request): #add id of message in correspondanceTable
    myPk = request.user.id
    if (int(myPk) == int(MessagePerso.objects.order_by('-id')[0].auteurID)):  # will check identity of writer to avoid
        print("identique : ", myPk)                                      # double message at the same time fail
        IDListAllow = CorrespondanceTableMessagesByUser.objects.get(idUser=myPk).messagesAccess
        listOfDiffID = IDListAllow.split(";")
        print(listOfDiffID)
        idOfNewMessage=MessagePerso.objects.order_by('-id')[0].id
        if (idOfNewMessage in listOfDiffID):
            print("Article {} déjà dans la liste".format(idOfNewMessage))
        else :
            print("ajout de l'article {} dans la liste d'accès".format(idOfNewMessage))

            correspondanceItem=CorrespondanceTableMessagesByUser.objects.get(idUser=myPk)
            correspondanceItem.messagesAccess  +=(";"+str(idOfNewMessage))
            correspondanceItem.save()

    else:
        print("non identique : ",myPk, " vs ",MessagePerso.objects.order_by('-id')[0].auteurID)