from django.shortcuts import render
from notifications.models import *

""" 

Here are the differents modules/functions that will manage notification system : 
First part is about common fonctions (CheckNCreateNotifField[will create new line in notification base],
                                        StrinToDict[will ... convert string in dict !])
Second part will manage global field "fil" notifications 
Third part will manage private direct messages notification

"""


def CheckNCreateNotifField(request):  # will check if a "notification" entry exist for this user, if not create
    # will be used for first connection to avoid notif bug (but can be replaced by a global try except on notif ?)

    try:
        # print("appel du check d'entrée de notif CheckNCreateNotifField pour l'user ", request.user.pk)
        entreeNotifIdUser = Notifications.objects.get(user_id=request.user.pk)  # will catch the userspecific line
        # print(entreeNotifIdUser)

    except:
        try:
            # print("check d'entrée de notif : non trouvé donc création de la ligne")
            Notifications.objects.create(user_id=request.user.pk)
        except:
            print("User non connecté_ pas de création de ligne")

    return

def CheckNCreateNotifFieldForIdCorrespondant(request,id_correspondant):  # will check if a "notification" entry exist for this user, if not create
    # will be used for first connection to avoid notif bug (but can be replaced by a global try except on notif ?)
    #if exist, will return the line

    try:
        # print("appel du check d'entrée de notif CheckNCreateNotifField pour l'user ", id_correspondant)
        entreeNotifIdUser = Notifications.objects.get(user_id=id_correspondant)  # will catch the userspecific line
        # print(entreeNotifIdUser)

    except:
        try:
            # print("check d'entrée de notif : non trouvé donc création de la ligne")
            Notifications.objects.create(user_id=id_correspondant)
            entreeNotifIdUser = Notifications.objects.get(user_id=id_correspondant)
        except:
            print("Problème de création de l'entrée des notifications")

    return entreeNotifIdUser


def stringTodict(stringToWorkWith):
    # print("string d'entrée : ",stringToWork)
    listTemp = stringToWorkWith.split(",")
    # print("liste temporaire: ",listTemp)

    dictCreated = {}
    for item in listTemp:
        if item != '':
            # print("l'item individuel de la liste est : ",item)
            minilist = item.split(":")
            # print("la minilist : ", minilist)
            dictCreated[minilist[0]] = minilist[1]
    # print(dictCreated)
    return dictCreated

def stringToList(stringToWorkWith):

    ListToReturn=stringToWorkWith.split(";")
    print('string splitée en liste : ',ListToReturn)
    return ListToReturn

def listToString(stringToWorkWith):
    ListToReturn=';'.join(stringToWorkWith)
    print('list rejointe en string : ',ListToReturn)
    return ListToReturn

""" 2d part : 
About notifications for common board 
"""


# update count in DB
def UpdateNotifFilValue(dicoNotifNumberInFilByCarnet, id_carnet, NewValue, entryInNotifications):
    # will take a dictionnary with all fil notifications value (as value) by carnet (as key) and update id_carnet value
    # with NewValue
    # print ("Dico ou on veut injecter la valeur : ",dicoNotifNumberInFilByCarnet)
    dicoNotifNumberInFilByCarnet[id_carnet] = str(NewValue)
    # print ("Nouveau dico avec la valeur injectée : ",dicoNotifNumberInFilByCarnet)
    newString = ""
    for cle, valeur in dicoNotifNumberInFilByCarnet.items():
        #    print("la clé " ,cle, " avec la valeur ", valeur)
        newString += (cle + ":" + valeur + ",")
    # print("la new string = "+newString)
    entryInNotifications.NotifFil = newString
    entryInNotifications.save()


# will add one to notif_fil of each correspondent
def notif_fil_add_one(request, id_carnet, list_of_correspondents):
    # check if each correspondant has notif entry, and if not create
    for correspondant in list_of_correspondents:
        try:
            # print("appel du check d'entrée de notif CheckNCreateNotifField pour le correspondant ", correspondant.id)
            entreeNotifIdUser = Notifications.objects.get(user_id=correspondant.id)  # will catch the userspecific line


        except:
            # print("check d'entrée de notif : non trouvé donc création de la ligne")
            Notifications.objects.create(user_id=correspondant.id)

    # check if the (x:x) exist, if not gives to NotifFil (x:1) value. if exist, increment value
    for correspondant in list_of_correspondents:
        entreeNotifIdUser = Notifications.objects.get(user_id=correspondant.id)
        print("la valeur initiale de Notiffil : ", entreeNotifIdUser.NotifFil)
        dicoNotifNumberInFilByCarnet = stringTodict(entreeNotifIdUser.NotifFil)

        try:
            found_Value = dicoNotifNumberInFilByCarnet[id_carnet]
            print("Référence au carnet ", id_carnet, " pour correspondant ", correspondant.id,
                  "trouvée, au compte de : ", found_Value)
            NewValue = int(found_Value) + 1  # so we'll have to inject NewValue and it's key in NotifFil
            UpdateNotifFilValue(dicoNotifNumberInFilByCarnet, id_carnet, NewValue, entreeNotifIdUser)


        except:
            print("Référence au carnet ", id_carnet, " pour correspondant ", correspondant.id, "non trouvée donc créé")
            entreeNotifIdUser.NotifFil += (id_carnet + ":1,")
            entreeNotifIdUser.save()


# will set to 0 the amount of notif fil
def notif_fil_reset(request, carnet_id):
    #print("appel de la fonction pour mettre à 0 la NotifFil de carnet ID chez User")

    # on récupère la ligne :
    entreeNotifIdUser = Notifications.objects.get(user_id=request.user.pk)  # entry of user's notification table

    # on transforme la case Notiffil que l'on souhaite en dico :
    dicoTemp = stringTodict(entreeNotifIdUser.NotifFil)

    # on change la valeur du carnet_id et on la met à 0:
    dicoTemp[carnet_id] = "0"

    # on retransforme dico en str
    newString = ""
    for cle, valeur in dicoTemp.items():
        #    print("la clé " ,cle, " avec la valeur ", valeur)
        newString += (cle + ":" + valeur + ",")

    # on l'injecte dans la BD
    entreeNotifIdUser.NotifFil = newString
    entreeNotifIdUser.save()


# will get global count of fil notif for a specific user
def notif_fil_global_count(request):
    entreeNotifIdUser = Notifications.objects.get(user_id=request.user.pk)  # entry of user's notification table
    dicoTemp = stringTodict(entreeNotifIdUser.NotifFil)
    somme = int()
    for valeur in dicoTemp.values():
        somme += int(valeur)
    return somme


# will get count of fil notif by CNB
def notif_fil_by_CNB(request, carnet_id):
    try:
        #print("Recherche de notif pour", carnet_id)
        entreeNotifIdUser = Notifications.objects.get(user_id=request.user.pk)  # entry of user's notification table
        dicoTemp = stringTodict(entreeNotifIdUser.NotifFil)

        number_of_notifs = dicoTemp[str(carnet_id)]

    except:
        number_of_notifs = 0

    return number_of_notifs


""" 3d part : 
About private direct messages
"""


def notifDirectMessageAddOne(request, id_carnet, id_correspondant):
    print("Ici, mettre dans la DB de  ", id_correspondant, " l'info que a propos du carnet", id_carnet,
          "il a été contacté par ", request.user.pk)
    # will check if correspondant has a notif entry in DB, else create
    NotifTempLine=CheckNCreateNotifFieldForIdCorrespondant(request,id_correspondant)


    # will check if correspondant has a NotifMessage field fullfield with (id_carnet:id_correspondant1;idcorrespondant2;id...) in his notif entry
    #print(NotifTempLine.NotifMessages)
    NotifTempDict=stringTodict(NotifTempLine.NotifMessages)

    #will seach if in NotifTempDict, there is an entry , and if yes, , add user.pk
    try:
        foundvalue=NotifTempDict[id_carnet]
        #now search if user.pk is in the part of id_carnet... if not addit
        listTemp=stringToList(foundvalue)
        if str(request.user.pk) in listTemp :
            print("l'user", request.user.pk , "a été trouvé dans la liste", listTemp, "on ne change rien")

        else :
            #print("l'user", request.user.pk , "n'a pas été trouvé dans la liste", listTemp)
            listTemp.append(str(request.user.pk))
            #print("la nouvelle listTemp : ", listTemp)
            ReString=listToString(listTemp)
            #print("La nouvelle string à injecter : ",ReString)
            NotifTempDict[id_carnet]=ReString
            #print("La nouvelle valeur correponsant a IdCarnet : ",NotifTempDict[id_carnet])
            #print("ce qui fait que l'ensemble des carnets : ",NotifTempDict)
            newString = ""
            for cle, valeur in NotifTempDict.items():
                #    print("la clé " ,cle, " avec la valeur ", valeur)
                newString += (cle + ":" + valeur + ",")
            #print("donc la nouvelle string modifiée : ",newString)
            NotifTempLine.NotifMessages=newString
            NotifTempLine.save()

    except:
        #print("il faut créer l'item correspondant au carnet et mettre la valeur userpk")
        newValueToAdd=str(id_carnet)+":"+str(request.user.pk)+","
        NotifTempLine.NotifMessages = NotifTempLine.NotifMessages+str(newValueToAdd)

        #print("Le truc qui va être réécrit : ",NotifTempLine.NotifMessages+str(newValueToAdd))
        NotifTempLine.save()


    return True



def getGlobalCountOfDirectMessage(request):
    #the purpose is to claim the total count of direct messages notifications

    # will check if user has a notif entry in DB, else create
    NotifTempLine=CheckNCreateNotifFieldForIdCorrespondant(request,request.user.pk)

    StringNotifsMessagesForUser=NotifTempLine.NotifMessages

    #number of concerned carnets:
    #print("ma string : ",StringNotifsMessagesForUser, "du type ",type(StringNotifsMessagesForUser))

    if "," in StringNotifsMessagesForUser:
        splitedStringByCarnets = StringNotifsMessagesForUser[:-1].split(",") #:-1 to delete coma
    else: #if there is no coma, it means that there is no value at all
        splitedStringByCarnets=[]=[]

    totalnumber=int()
    for CarnetNotif in splitedStringByCarnets:
        #print("valeur intermédiaire", len(CarnetNotif.split(";"))," pour la chaine ",CarnetNotif.split(";"))
        totalnumber+=len(CarnetNotif.split(";"))



    return totalnumber

def notif_message_by_CNB(request,carnet_id):
    NotifTempLine = Notifications.objects.get(user_id=request.user.pk)
    NotifTempDict=stringTodict(NotifTempLine.NotifMessages)
    try :
        foundvalue = NotifTempDict[str(carnet_id)]
        numberOfFoundValues=len(foundvalue.split(";"))

        #print(foundvalue)
        returnValue=numberOfFoundValues
    except :
        #print("Le carnet ", carnet_id, "n'a pas été trouvé dans la chaine", NotifTempDict)
        returnValue=0

    return returnValue

def notif_message_by_CNB_and_Correspondant(request,carnet_id,correspondant_id):
    #print("On va récupérer les notifications de l'utilisateur ",request.user.pk, "correspondant au carnet ",carnet_id, " et du correspondant ",correspondant_id)

    #we catch all the notifications about the current carnet
    try:
        NotifTempLine = Notifications.objects.get(user_id=request.user.pk)
        NotifTempDict = stringTodict(NotifTempLine.NotifMessages)
        StringOfNotifAboutMessagesForSpectificCNB = NotifTempDict[str(carnet_id)]
        ListOfNotifByCarnet=StringOfNotifAboutMessagesForSpectificCNB.split(';')
        #print("la valeur de la liste à cet endroit est : ",ListOfNotifByCarnet)

        # and we have to catch the right part according to correspondant id :
        if correspondant_id in [int(x) for x in ListOfNotifByCarnet] :
            ValueToReturn=1
        else:
            ValueToReturn=0

    except :
        #print("Erreur de récupération des notifications en message de ce carnet : soit bug, soit vide")
        ValueToReturn=0

    #print("La valeur dans ces conditions est : ",ValueToReturn)

    return ValueToReturn

def NotifMessagesReset(request,id_carnet,id_correspondant):
    #print("RAZ pour le carnet ", id_carnet, "et le correspondant ", id_correspondant, "chez user", request.user.pk)

    NotifTempLine = Notifications.objects.get(user_id=request.user.pk)
    NotifTempDict = stringTodict(NotifTempLine.NotifMessages)

    try :
        StringOfNotifAboutMessagesForSpectificCNB = NotifTempDict[str(id_carnet)]
        ListOfNotifByCarnet = StringOfNotifAboutMessagesForSpectificCNB.split(';')
        #print("la valeur de la liste à cet endroit est : ",ListOfNotifByCarnet)
        listEnInt=[int(x) for x in ListOfNotifByCarnet]


        listEnInt.remove(int(id_correspondant))
        #print("nouvelle liste : ", listEnInt)
        ReString = listToString([str(x) for x in listEnInt])
        # print("La nouvelle string à injecter : ",ReString)
        NotifTempDict[id_carnet] = ReString
        # print("La nouvelle valeur correponsant a IdCarnet : ",NotifTempDict[id_carnet])
        #print("ce qui fait que l'ensemble des carnets : ",NotifTempDict)
        newString = ""
        for cle, valeur in NotifTempDict.items():
            #    print("la clé " ,cle, " avec la valeur ", valeur)
            if valeur == "":
                continue
            newString += (cle + ":" + valeur + ",")
        #print("donc la nouvelle string modifiée : ",newString)
        NotifTempLine.NotifMessages = newString
        NotifTempLine.save()
    except :
        print("")
        #print("Pas de suppression possible, mais c'est peut être que la liste est nulle ?")



