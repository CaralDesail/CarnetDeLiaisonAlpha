from django.shortcuts import render
from . import models
from django.views.generic import ListView

# Create your views here.
class NotifList(ListView):
    model = models.Notifications
    #gives object_list to template linked with url that will use this class