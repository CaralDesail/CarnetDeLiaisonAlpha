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
    #listeMessages = MessagePerso.objects.all()
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
            CorrespondingMessage.Correspondantsstring=\
                callOfCorrespondantList(request,CorrespondingMessage,messageID) # call above function


            list_to_return.append(CorrespondingMessage)
        except :
            print("Message {} non valide".format(messageID))
    return list_to_return

def callOfCorrespondantList (request,CorrespondingMessage,messageID): # return a string with the name of correspondants
    try:
        listCorrespondants=[]
        for correspondant in (CorrespondingMessage.accessUserID).split(";") :
            Correspondant=str(User.objects.get(pk=correspondant).first_name)+" "+str(User.objects.get(pk=correspondant).last_name)
            listCorrespondants.append(Correspondant)

        listCorrespondants=" , ".join(listCorrespondants)
        print(listCorrespondants)
        return listCorrespondants

    except:
        print("Echec de la récupération des correspondants ",messageID)


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
    #first part that add writer id to access list
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
            add_sentToCorrespondanttoAccessList() # call the next function that will add
            # correspondants to access list in CorrespondanceTalbeMessagesByUser

    else:
        print("non identique : ",myPk, " vs ",MessagePerso.objects.order_by('-id')[0].auteurID)

def add_sentToCorrespondanttoAccessList():
    print("Appel de la seconde fonction qui va inscrire les correpondants à la liste autorisée à la lecture du message")
    LastMessage=MessagePerso.objects.order_by('-id')[0]
    IDCorrString=LastMessage.accessUserID
    IDCorrList=IDCorrString.split(";") # gives list of users purposed in message field "accessUserID"
    for idTOCheck in IDCorrList:
        UserItemInCorrespondanceLine = CorrespondanceTableMessagesByUser.objects.get(idUser=idTOCheck)
        StringOfUsersinTable=UserItemInCorrespondanceLine.messagesAccess
        ListOfUsersIntable=StringOfUsersinTable.split(";") # gives the list of access to messages in correspondance table
        if (LastMessage.id in ListOfUsersIntable):
            print(LastMessage.id, " est déjà dans la liste ")
        else :
            UserItemInCorrespondanceLine.messagesAccess += (";"+str(LastMessage.id))
            print("ID ajouté : ", LastMessage.id , " a l'user ", idTOCheck)
            UserItemInCorrespondanceLine.save()



def listProRLPerso(idCarnet):
    print("l'ID du carnet :" ,idCarnet)

    listToreturn=[]

    if (idCarnet==0): #if idCarnet is 0, then add all Users
        print("Inclusion de tous les utilisateurs")
        listModelUser=User.objects.all()
    else :
        listModelUser = User.objects.all()
        #################################################
        # TO CREATE : use a selection of autorized users and return it as listModelUser#
        #################################################


    for userId in listModelUser: #will add function of user to userId ... before returning the true list
        print(userId.first_name, " ", userId.last_name, )
        print("son id est :",userId.id)
        try:
            profilId=Profil.objects.get(user_id=userId.id)
        except:
            print("Incohérence sur la récupération du profil de user ", userId.id)
        try:
            groupsUser=userId.groups.all()
            userGroupName = groupsUser[0].name
            if (userGroupName=="SuperUser"):
                userId.function="SuperUtilisateur"
            if (userGroupName=="Professionnel"):
                userId.function=CategoriePro.objects.get(id=profilId.rolePro_id).name
            if (userGroupName=="Responsable légal"):
                userId.function=profilId.statusRL
            #print(userId.function)
        except:
            print("Probleme d'algorythme d'utilisation de case selon groupage")

        keyT=userId.id
        valueK=userId.first_name+" "+userId.last_name+" "+userId.function
        keyAndValue=(keyT,valueK)

        listToreturn.append(keyAndValue)


    return listToreturn