from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from datetime import datetime
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import Permission, User
from django.contrib.auth.decorators import permission_required
from .modules_complementaires import *
from .admin_compl_tools import *
from .permissions import *
from notifications.modules_complementaires import *


def home(request):

    date=datetime.now()

    try:
        groupQS = request.user.groups.all()
        userGroupName = groupQS[0].name
        print("User group = ", userGroupName)

    except :
        print("userAnonymous")
        userGroupName = ""

    return render(request,'tablecom/accueil_tablecom.html',locals())

def ContactUs(request):
    print("clic contact us")
    form = ContactUsForm(request.POST or None)
    #print(form.Categorie_Professionnelle)
    if form.is_valid():
        print("Formulaire validé")
        envoi=True
        form.save()
        try:
            formTitle=form.cleaned_data['title']
            formContent=form.cleaned_data['content']
            formEmail=form.cleaned_data['email']
            formUsername=form.cleaned_data['username']
            formFirst_name=form.cleaned_data['first_name']
            formLast_name=form.cleaned_data['last_name']

            formPhone=form.cleaned_data['phone']
            formRLouPro=form.cleaned_data['RLorPro']
            formStatusRL=form.cleaned_data['statusRL']
            formRolePro=form.cleaned_data['rolePro']
            formChildAccess=form.cleaned_data['child_access_asked']

            stringTosend="Envoi du formulaire Contact Us :\n "+ "Titre = " +formTitle+"\n Contenu : "+formContent+\
                         "\n Username : "+formUsername+"\n Email : "+formEmail+\
                         "\n First Name : "+formFirst_name+"\n Last Name : "+formLast_name+"\n Telephone : "+formPhone+\
                         "\n RLorPro : " + str(formRLouPro) +"\n Status RL : " + str(formStatusRL) + "\n Role Pro : " + str(formRolePro)+\
                         "\n Demande d'accès aux enfants : " + formChildAccess



            send_a_mail("Envoi du questionnaire ContactUs depuis le site Handebook",stringTosend)
        except:
            raise
            print("Problème : Mail non envoyé")
        #print(form.data)
    return render(request, 'tablecom/ContactUs.html',locals())

def MyProfile(request):
    CarrierList=GlobalCarrier(request)#will carry all necessary variables (for notification, ...)

    groupQS = request.user.groups.all()
    userGroupName = groupQS[0].name
    userProfil = Profil.objects.get(user_id=request.user.pk)

    roleProNum = userProfil.rolePro_id
    nameRole = CategoriePro.objects.get(id=roleProNum).name

    print(userProfil)
    return render(request, 'tablecom/MyProfile.html',locals())

def EditUserForm(request,editzone):
    myProfilInstance = Profil.objects.get(user_id=request.user.pk)

    if request.method == 'POST': # if form has been validated
        if editzone == "email" :
            print("edit du mail")
            form = EditUserMail(request.POST,instance=request.user)

        if editzone == "phone" :
            form = EditUserPhone(request.POST,instance=myProfilInstance)

        if form.is_valid():
            print("Formulaire validé")
            envoi=True
            form.save()
            return redirect("MyProfile")
        else :
            print("form non valide ")

    else : # if not still validated
        if editzone == "email" :
            print("edit du mail")
            form = EditUserMail(instance=request.user)

        if editzone == "phone" :
            form = EditUserPhone(instance=myProfilInstance)



    return render(request, 'tablecom/EditUser.html', locals())

def deconnexion(request):
    logout(request)
    return redirect('accueil')

def ChildSNotebookListVisu(request):
    CarrierList=GlobalCarrier(request)#will carry all necessary variables (for notification, ...)

    CheckNCreateNotifField(request) # will call the creation of notification entry if dont exist

    datetrans = datetime.now()
    ChildSNBsInput=list(ChildSNotebook.objects.all())
    ChildSNBs=[]
    for CSNB in ChildSNBsInput:
        pkAct=CSNB.pk

        #print("ID du carnet actuel= ",pkAct)
        if request.user.has_perm("tablecom.CSNB{0}_access".format(pkAct)):
            #print("acces")
            CSNB.notif_fil=notif_fil_by_CNB(request, pkAct)
            CSNB.notif_message=notif_message_by_CNB(request, pkAct)
            ChildSNBs.append(CSNB)
        else:
            #print("No acces to ",CSNB.pk)
            True


    print(ChildSNBs)
    return render(request, 'tablecom/ChildSNotebookListVisu.html', {'liste_carnets': ChildSNBs,'date':datetrans, 'CarrierList':CarrierList})

def ChildSNotebookVisu(request,id_carnet):

    if request.user.has_perm("tablecom.CSNB{0}_access".format(id_carnet)):

        carnet = get_object_or_404(ChildSNotebook, id=id_carnet)
        print("Ouverture d'un carnet",id_carnet, carnet)

        carnet.notif_message = notif_message_by_CNB(request, id_carnet)

        listArticlesString= carnet.articles_id #catch list of articles ID

        newListOfArticles=list_of_articles(listArticlesString)
        newListOfArticles.reverse() #reverse list of articles to makes the last wroten the first printend

        """about notifications ..."""
        notif_fil_reset(request,id_carnet) #will call this function in notifications/modules_complementaires.py
        CarrierList = GlobalCarrier(request)  # will carry all necessary variables (for notification, ...)


        return render(request, 'tablecom/ChildSNotebook.html', locals())

def Message_Contact_ListView(request, id_carnet):
    CarrierList = GlobalCarrier(request)  # will carry all necessary variables (for notification, ...)

    if request.user.has_perm("tablecom.CSNB{0}_access".format(id_carnet)):
        #call the list of contacts
        #print("le carnet appelé est ",id_carnet)
        carnet = get_object_or_404(ChildSNotebook, id=id_carnet)
        listProfString = carnet.id_prof_auth  # catch list of id of profs
        newListOfProf = list_of_prof(request,listProfString,id_carnet)  # call external function that returns list of contacts
        #print("Liste des pros : ",newListOfProf)

        listRLString = carnet.id_RespLeg # catch list of id of RL
        newListOfRL = list_of_prof(request,listRLString,id_carnet) # use same function that return list of RL
        #print("Liste des RL", newListOfRL)

        return render(request, 'tablecom/message_contact_list.html', locals())

def NewArticle(request,id_carnet):

    if request.user.has_perm("tablecom.CSNB{0}_access".format(id_carnet)):
        CarrierList = GlobalCarrier(request)  # will carry all necessary variables (for notification, ...)

        carnet=get_object_or_404(ChildSNotebook, id=id_carnet)
        id_of_current_user=request.user.pk
        premodelNA=Article(id_Professionnal=id_of_current_user, DeletedDate="2000-01-01 01:01:01.000000")
        form = NewArticleForm(request.POST or None, instance=premodelNA)
        if form.is_valid():
            carnet = get_object_or_404(ChildSNotebook, id=id_carnet)
            list_of_correspondants = list_of_prof(request,carnet.id_prof_auth + carnet.id_RespLeg,id_carnet)
            notif_fil_add_one(request, id_carnet, list_of_correspondants)
            print("Formulaire validé")
            envoi = True
            form.save()
            dernier_article=Article.objects.latest('date')
            print(dernier_article.pk)

            carnet.articles_id+=(";"+str(dernier_article.pk)) #will add article reference to carnet
            carnet.save()

        return render(request, 'tablecom/NewArticle.html', locals())

def DelArticle(request,id_carnet, id_article):

    print("Après vérif des droits d'accès au carnet {0} d'une part, et que l'article {1} à supprimer à bien été écrit "
          "par  {2} d'autre part".format(id_carnet,id_article,request.user.pk))
    carnet = get_object_or_404(ChildSNotebook, id=id_carnet)
    article= get_object_or_404(Article, id=id_article)

    if request.user.has_perm("tablecom.CSNB{0}_access".format(id_carnet)) and article.id_Professionnal==request.user.pk :
        print("acces au carnet {0} ok".format(id_carnet))
        article.active=False
        article.DeletedDate=datetime.now()
        article.save()

    else :
        print("Problème d'accès soit au carnet, soit à l'article dont vous n'êtes pas l'auteur")


    return redirect('ChildSNotebookVisu', id_carnet=id_carnet)

def GlobalCarrier(request):
    # will contain list of variables necessary in each page
    try:
        NumberOfFilNotifications = notif_fil_global_count(request)

    except:
        NumberOfFilNotifications = "0"


    try :
        NumberOfMessagesNotifications=getGlobalCountOfDirectMessage(request)
    except :
        raise
        NumberOfMessagesNotifications="0"

    CarrierList = [NumberOfMessagesNotifications, NumberOfFilNotifications]
        
    return (CarrierList)

def AdminTools(request):
    return render(request,'tablecom/AdminTools.html',locals())


@permission_required('auth.add_user')
@permission_required('tablecom.add_profil')
def ChildSNotebookCreatView(request):
    form = ChildSNotebookCreatForm(request.POST or None)
    #print(form.Categorie_Professionnelle)
    if form.is_valid():
        print("Formulaire validé")
        envoi=True
        form.save()
        PermCreationAccessLastEntry(ChildSNotebook)
        #print(form.data)

    return render(request, 'tablecom/ChildSNotebookCreat.html', locals())

@permission_required('auth.add_user')
@permission_required('tablecom.add_profil')
def ProCreatView(request):
    form = ProCreatForm(request.POST or None)
    #print(form.Categorie_Professionnelle)
    if form.is_valid():
        print("Formulaire validé")
        envoi=True
        form.save()

    return render(request, 'tablecom/ProCreat.html', locals())

@permission_required('auth.add_user')
@permission_required('tablecom.add_profil')
def RLCreatView(request):
    form = RLCreatForm(request.POST or None)
    #print(form.Categorie_Professionnelle)
    if form.is_valid():
        print("Formulaire validé")
        envoi = True
        form.save()

    return render(request, 'tablecom/RLCreat.html', locals())

@permission_required('auth.change_permission')
def AdminTools_PermissionCarnetRecreation(request): #will regenerate all permissions of different carnets
    PermCreationAllEntry(ChildSNotebook)
    return render(request,'tablecom/AdminTools.html',locals())

def AdminTools_PermCoherenceAll(request):
    PermCoherenceAll()
    return render(request, 'tablecom/AdminTools.html', locals())

@permission_required('auth.change_permission')
def PermissionsManagement_Main(request):
    ChildSNBs=list(ChildSNotebook.objects.all().order_by("-pk"))
    return render(request, 'tablecom/PermissionsManagement_Main.html', locals())

@permission_required('auth.change_permission')
def PermissionsManagement_Detail(request,id_carnet):
    print(id_carnet)
    carnet = get_object_or_404(ChildSNotebook, id=id_carnet)
    usersPro=User.objects.filter(groups="2") #group 2 is "Professionnals"
    listaccessPro=[]
    for userPro in usersPro:
        accesbool= userPro.has_perm("tablecom.CSNB{0}_access".format(id_carnet))

        roleProNum=Profil.objects.get(user_id=userPro.pk).rolePro_id #get for each user the number of rolepro
        nameRole = CategoriePro.objects.get(id=roleProNum).name
        listaccessPro.append((userPro, accesbool, nameRole))

    usersRL=User.objects.filter(groups="3") #group 3 is "Legal Responsibles"
    listaccessRL = []
    for userRL in usersRL:
        accesboolRL = userRL.has_perm("tablecom.CSNB{0}_access".format(id_carnet))
        roleRL = Profil.objects.get(user_id=userRL.pk).statusRL
        listaccessRL.append((userRL, accesboolRL, roleRL))

    return render(request, 'tablecom/PermissionsManagement_Detail.html', locals())

@permission_required('auth.change_permission')
def PermissionsManagement_Action (request, id_carnet, id_user, action):
    print("appel d'une fonction visant à {0} l'acces de l'user {1} au carnet {2}".format(action,id_user,id_carnet))
    carnet = get_object_or_404(ChildSNotebook, id=id_carnet)
    if action=="Allow":
        PermAllower(id_carnet,id_user)

    if action=="Remove":
        PermRemover(id_carnet,id_user)
    return redirect('PermissionsManagement_Detail', id_carnet=id_carnet)

