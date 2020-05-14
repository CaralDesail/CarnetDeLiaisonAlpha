from django.contrib import admin
from django.urls import path, include
from . import views
from . import ModulesComplementaires
from .views import TemplateNewMessageFormView
from .forms import Message_SW

urlpatterns = [
    path('', views.home,name="accueilMessager"),
    path('accueilMessager', views.home, name="accueilMessager"),

    path('CorrespondanceTableCheck', ModulesComplementaires.correspondanceTableMessages_check,name="CorrespondanceTableCheck" ),
    path('Message_sw', TemplateNewMessageFormView.as_view(form_class=Message_SW), name='Message_sw')

]