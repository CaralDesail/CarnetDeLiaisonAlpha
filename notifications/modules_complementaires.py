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
        try :
            # print("check d'entrée de notif : non trouvé donc création de la ligne")
            Notifications.objects.create(user_id=request.user.pk)
        except:
            print("User non connecté_ pas de création de ligne")

    return


def stringTodict(stringToWork):
    # print("string d'entrée : ",stringToWork)
    listTemp = stringToWork.split(",")
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


""" 2d part : 
About notifications for common board 
"""

#update count in DB
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
def notif_fil_reset(request,carnet_id):
    print("appel de la fonction pour mettre à 0 la NotifFil de carnet ID chez User")

    #on récupère la ligne :
    entreeNotifIdUser = Notifications.objects.get(user_id=request.user.pk) #entry of user's notification table

    #on transforme la case Notiffil que l'on souhaite en dico :
    dicoTemp=stringTodict(entreeNotifIdUser.NotifFil)

    #on change la valeur du carnet_id et on la met à 0:
    dicoTemp[carnet_id]="0"

    # on retransforme dico en str
    newString=""
    for cle, valeur in dicoTemp.items():
        #    print("la clé " ,cle, " avec la valeur ", valeur)
        newString += (cle + ":" + valeur + ",")

    #on l'injecte dans la BD
    entreeNotifIdUser.NotifFil = newString
    entreeNotifIdUser.save()

# will get global count of fil notif for a specific user
def notif_fil_global_count(request):
    entreeNotifIdUser = Notifications.objects.get(user_id=request.user.pk) #entry of user's notification table
    dicoTemp=stringTodict(entreeNotifIdUser.NotifFil)
    somme=int()
    for valeur in dicoTemp.values():
        somme+=int(valeur)
    return somme

# will get count of fil notif by CNB
def notif_fil_by_CNB(request,carnet_id):

    try :
        print("Recherche de notif pour", carnet_id)
        entreeNotifIdUser = Notifications.objects.get(user_id=request.user.pk) #entry of user's notification table
        dicoTemp=stringTodict(entreeNotifIdUser.NotifFil)

        number_of_notifs=dicoTemp[str(carnet_id)]

    except :
        number_of_notifs =0

    return number_of_notifs


""" 3d part : 
About private direct messages
"""
