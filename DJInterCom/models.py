from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from tablecom.models import *

# Create your models here.


class MessagePerso(models.Model):
    titre = models.CharField(max_length=100)
    auteurID = models.CharField(max_length=6)
    contenu = models.TextField(null=True)
    date = models.DateTimeField(default=timezone.now,
                                verbose_name="Date d'envoi'")
    accessUserID=models.CharField(max_length=80,default="0")

    class Meta:
        verbose_name = "Message Privé"
        ordering = ['date']

    def __str__(self):
        """
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que
        nous traiterons plus tard dans l'administration
        """
        return self.titre

class CorrespondanceTableMessagesByUser(models.Model):
    idUser = models.CharField(max_length=6)
    messagesAccess = models.TextField(blank=True,default="0")