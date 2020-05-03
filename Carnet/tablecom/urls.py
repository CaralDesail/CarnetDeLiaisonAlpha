from django.urls import path
from . import views

urlpatterns = [
    path('accueil', views.home),
    path('ProCreat', views.ProCreatView, name='ProCreat'),
    path('RLCreat',views.RLCreatView,name="RLCreat"),
    path('Connexion', views.connexion,name="connexion"),
    path('Deconnexion', views.deconnexion, name="deconnexion"),
    path('Carnets',views.ChildSNotebookListVisu, name="ChildSNotebookListVisu"),
    path('CarnetVisu/<id_carnet>',views.ChildSNotebookVisu, name="ChildSNotebookVisu"),
    path('NewArticle/<id_carnet>',views.NewArticle, name="NewArticle"),

]