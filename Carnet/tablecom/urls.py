from django.urls import path
from . import views
from django.conf.urls import include, url
from django.views.generic import *
from .models import ChildSNotebook

urlpatterns = [
    path('', views.home, name='accueil'),
    path('accueil', views.home, name='accueil'),
    path('ProCreat', views.ProCreatView, name='ProCreat'),
    path('RLCreat',views.RLCreatView,name="RLCreat"),
    path('Connexion', views.connexion,name="connexion"),
    path('Deconnexion', views.deconnexion, name="deconnexion"),
    path('Carnets',views.ChildSNotebookListVisu, name="ChildSNotebookListVisu"),
    path('CarnetVisu/<id_carnet>',views.ChildSNotebookVisu, name="ChildSNotebookVisu"),
    path('NewCSNB', views.ChildSNotebookCreatView, name="ChildSNotebookCreatView"),
    path('NewArticle/<id_carnet>',views.NewArticle, name="NewArticle"),
    path('AdminTools',views.AdminTools, name="AdminTools"),
    path('AdminTools_PermissionCarnetRecreation',views.AdminTools_PermissionCarnetRecreation,name="AdminTools_PermissionCarnetRecreation"),
    path('PermissionsManagement_Main', views.PermissionsManagement_Main, name="PermissionsManagement_Main"),
    path('PermissionsManagement_Detail/<id_carnet>', views.PermissionsManagement_Detail, name="PermissionsManagement_Detail"),
    path('PermissionsManagement_Action/<id_carnet>/<id_user>/<action>', views.PermissionsManagement_Action, name="PermissionsManagement_Action"),

    path('baseHTML', TemplateView.as_view(template_name="tablecom/base.html"))
]