from django.urls import path
from . import views
from django.conf.urls import include, url
from django.views.generic import *
from .models import ChildSNotebook
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='accueil'),
    path('accueil', views.home, name='accueil'),

    path('Connexion', auth_views.LoginView.as_view(),name="connexion"),
    path('Deconnexion', views.deconnexion, name="deconnexion"),
    path('Changepassword',auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name="password_change"),
    path('password_change_done',auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_form_done.html'), name="password_change_done"),
    path('password_reset',auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_form_done.html'),name='password_reset_complete'),


    path('Carnets',views.ChildSNotebookListVisu, name="ChildSNotebookListVisu"),
    path('CarnetVisu/<id_carnet>',views.ChildSNotebookVisu, name="ChildSNotebookVisu"),
    path('NewCSNB', views.ChildSNotebookCreatView, name="ChildSNotebookCreatView"),
    path('NewArticle/<id_carnet>',views.NewArticle, name="NewArticle"),
    path('ProCreat', views.ProCreatView, name='ProCreat'),
    path('RLCreat', views.RLCreatView, name="RLCreat"),
    path('MyProfile',views.MyProfile, name="MyProfile"),
    path('EditUserForm/<editzone>',views.EditUserForm, name="EditUserForm"),


    path('AdminTools',views.AdminTools, name="AdminTools"),
    path('AdminTools_PermissionCarnetRecreation',views.AdminTools_PermissionCarnetRecreation,name="AdminTools_PermissionCarnetRecreation"),
    path('AdminTools_PermCoherenceAll', views.AdminTools_PermCoherenceAll,
         name="AdminTools_PermCoherenceAll"),

    path('PermissionsManagement_Main', views.PermissionsManagement_Main, name="PermissionsManagement_Main"),
    path('PermissionsManagement_Detail/<id_carnet>', views.PermissionsManagement_Detail, name="PermissionsManagement_Detail"),
    path('PermissionsManagement_Action/<id_carnet>/<id_user>/<action>', views.PermissionsManagement_Action, name="PermissionsManagement_Action"),

    path('ContactUs', views.ContactUs, name="ContactUs"),

    path('baseHTML', TemplateView.as_view(template_name="tablecom/base.html"))
]