from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('MessageAboutTo/<id_carnet>/<id_correspondant>/', views.messageAboutTo, name="MessageAboutTo")


]