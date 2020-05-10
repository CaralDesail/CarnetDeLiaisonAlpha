from django.contrib import admin
from django.urls import path, include
from . import views
from . import ModulesComplementaires

urlpatterns = [
    path('', views.home,name="accueilMessager"),
    path('accueilMessager', views.home, name="accueilMessager"),

    path('new_MessagePerso', views.new_MessagePerso, name="new_MessagePerso"),
    path('CorrespondanceTableCheck', ModulesComplementaires.correspondanceTableMessages_check,name="CorrespondanceTableCheck" ),

]