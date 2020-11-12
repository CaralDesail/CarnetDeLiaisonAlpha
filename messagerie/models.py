from django.db import models
from django.utils import timezone


# Create your models here.
class MessagePersoAT(models.Model):
    titre = models.CharField(max_length=100, default="")
    auteurID = models.CharField(max_length=6)
    AttachedChildNotebookID = models.CharField(max_length=7)
    receiverID = models.CharField(max_length=6, default="0")
    contenu = models.TextField(null=True, verbose_name="")
    date = models.DateTimeField(default=timezone.now,
                                verbose_name="Date d'envoi'")
    validated=models.BooleanField(default=True) #is the message validated to appear?
    read=models.BooleanField(default=False) #is the message read by receiver ?


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