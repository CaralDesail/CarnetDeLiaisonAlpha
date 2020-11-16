from django.db import models
from django.utils import timezone


# Create your models here.
class MessagePersoAT(models.Model):

    """ this model is the "private" or "direct" message system model :
    a message will be defined by different common fields (titre, auteur, receiver, contenu, date) and specific ones :
    - AttachedChildNotebook ID (because the messages here are always attached to one NoteBook (yes, may be a more elegant
    method is possible with foreign keys ;)   )
    - validated : is parents has told "ok to validation" (can be set manually message after message or in global CGU)
    - activeMessage : Has this message been deleted ?
    - read (a unused field that could be used for notifications)
    """

    titre = models.CharField(max_length=100, default="")
    auteurID = models.CharField(max_length=6)
    AttachedChildNotebookID = models.CharField(max_length=7)
    receiverID = models.CharField(max_length=6, default="0")
    contenu = models.TextField(null=True, verbose_name="")
    date = models.DateTimeField(default=timezone.now,
                                verbose_name="Date d'envoi'")
    validated=models.BooleanField(default=True) #is the message validated to appear?
    activeMessage=models.BooleanField(default=True) #is the message is active or inactive (deleted, problem, ...)
    read=models.BooleanField(default=False) #is the message read by receiver ?


    class Meta:
        verbose_name = "Message Privé"
        ordering = ['date']

    def __str__(self):

        return self.titre