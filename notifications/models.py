from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Notifications(models.Model): #extend User proprieties
    user = models.OneToOneField(User,on_delete=models.CASCADE,default=1)
    NotifMessages = models.TextField(verbose_name="Notifications Des Nouveaux Messages") #contain list of waiting notif
    # for this user with model : (CarnetID:Contact)(CarnetID:Contact)(Ca ...
    NotifFil = models.TextField( verbose_name="Notifications du fil",) # contain list of wainting notif
    # like (carnetId:Count)(carnetId:Count)(car...

