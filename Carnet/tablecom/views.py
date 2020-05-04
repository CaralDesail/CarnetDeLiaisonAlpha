from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from datetime import datetime
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import permission_required
from tablecom.models import ChildSNotebook
from .modules_complementaires import *

# Create your views here.

def home(request):
    date=datetime.now()
    #CurrentUserP=request.user  // not used because "user" can be called directly in template : no need to call it
    #print(CurrentUserP.username)
    groupQS=request.user.groups.all()
    userGroupName=groupQS[0].name
    return render(request,'tablecom/accueil_tablecom.html',locals())

def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'tablecom/ConnectUser.html', locals())

def deconnexion(request):
    logout(request)
    return render(request, 'tablecom/ConnectUser.html', locals())

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
    ChildSNBs=ChildSNotebook.objects.all()
    print(ChildSNBs)
    return render(request, 'tablecom/ChildSNotebookListVisu.html', {'liste_carnets': ChildSNBs})

def ChildSNotebookVisu(request,id_carnet):

    carnet = get_object_or_404(ChildSNotebook, id=id_carnet)
    print("Ouverture d'un carnet",id_carnet, carnet)

    listProfString = carnet.id_prof_auth #catch list of id of profs
    newListOfProf=list_of_prof(listProfString) #call external function that returns list of professionnals

    listArticlesString= carnet.articles_id #catch list of articles ID
    newListOfArticles=list_of_articles(listArticlesString)

    return render(request, 'tablecom/ChildSNotebook.html', locals())

def NewArticle(request,id_carnet):
    form = NewArticleForm(request.POST or None)
    # print(form.Categorie_Professionnelle)
    if form.is_valid():
        print("Formulaire validé")
        envoi = True
        form.save()

    return render(request, 'tablecom/NewArticle.html', locals())
