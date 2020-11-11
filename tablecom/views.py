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


def home(request):
    date=datetime.now()
    #CurrentUserP=request.user  // not used because "user" can be called directly in template : no need to call it
    #print(CurrentUserP.username)
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
        #print(form.data)
    return render(request, 'tablecom/ContactUs.html',locals())

def MyProfile(request):
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

def ChildSNotebookListVisu(request):
    datetrans = datetime.now()
    ChildSNBsInput=list(ChildSNotebook.objects.all())
    ChildSNBs=[]
    for CSNB in ChildSNBsInput:
        pkAct=CSNB.pk
        print("ID du carnet actuel= ",pkAct)
        if request.user.has_perm("tablecom.CSNB{0}_access".format(pkAct)):
            print("acces")
            ChildSNBs.append(CSNB)
        else:
            print("No acces")


    print(ChildSNBs)
    return render(request, 'tablecom/ChildSNotebookListVisu.html', {'liste_carnets': ChildSNBs,'date':datetrans})

def ChildSNotebookVisu(request,id_carnet):

    if request.user.has_perm("tablecom.CSNB{0}_access".format(id_carnet)):
        carnet = get_object_or_404(ChildSNotebook, id=id_carnet)
        print("Ouverture d'un carnet",id_carnet, carnet)

        listProfString = carnet.id_prof_auth #catch list of id of profs
        newListOfProf=list_of_prof(listProfString) #call external function that returns list of professionnals

        listArticlesString= carnet.articles_id #catch list of articles ID

        newListOfArticles=list_of_articles(listArticlesString)
        newListOfArticles.reverse() #reverse list of articles to makes the last wroten the first printend
        print(newListOfProf)



        return render(request, 'tablecom/ChildSNotebook.html', locals())

def NewArticle(request,id_carnet):
    if request.user.has_perm("tablecom.CSNB{0}_access".format(id_carnet)):
        carnet=get_object_or_404(ChildSNotebook, id=id_carnet)
        id_of_current_user=request.user.pk
        premodel=Article(id_Professionnal=id_of_current_user)
        form = NewArticleForm(request.POST or None, instance=premodel)
        if form.is_valid():
            print("Formulaire validé")
            envoi = True
            form.save()
            dernier_article=Article.objects.latest('date')
            print(dernier_article.pk)

            carnet.articles_id+=(";"+str(dernier_article.pk)) #will add article reference to carnet
            carnet.save()

        return render(request, 'tablecom/NewArticle.html', locals())


def AdminTools(request):
    return render(request,'tablecom/AdminTools.html',locals())

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

