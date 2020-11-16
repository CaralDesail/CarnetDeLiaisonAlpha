from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class ChildSNotebook(models.Model): #name of table that contain differents "carnets" for each child
    active=models.BooleanField(default=True)
    name = models.CharField(max_length=80, verbose_name="Nom")
    forename = models.CharField(max_length=80, verbose_name="Prénom")
    date_of_birth = models.DateField(verbose_name="Date de naissance")
    id_RespLeg = models.CharField(max_length=20,verbose_name="Id responsables legaux", default="")  # id of childs attached to LR
    num_ident=models.CharField( verbose_name="Identifiant sécurité sociale",max_length=20)
    id_prof_auth=models.TextField(max_length=1200, verbose_name="Id Professionnels Rattachés")
    articles_id=models.TextField(max_length=2500, verbose_name="Id des articles rattachés", default="")

    class Meta:
        verbose_name = "Carnet Enfant"
        ordering = ['date_of_birth']

    def __str__(self):
        return self.name


class Profil(models.Model): #extend User proprieties
    user = models.OneToOneField(User,on_delete=models.CASCADE,default=1)
    rolePro = models.ForeignKey('CategoriePro', on_delete=models.CASCADE, default=0, verbose_name='Catégorie si professionnel')
    statusRL = models.CharField(max_length=20,default="NA", verbose_name="Catégorie si reponsable légal") #who it is ? parent ? tutor ? curator ?
    num_ident = models.CharField(verbose_name="Identifiant sécurité sociale", max_length=20)
    phone =  models.CharField(max_length=60, null=True)


class CategoriePro(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name



class Article(models.Model): #table of differents "notes", or "articles" that will be created by Pro or LR
    active = models.BooleanField(default=True) #is active or not (suppressed ?)
    id_Professionnal=models.IntegerField(verbose_name='Id Professionnel')
    title = models.CharField(max_length=255, verbose_name="Titre")
    content = models.TextField(null=False, verbose_name="Contenu")
    date = models.DateTimeField(default=timezone.now,
                                verbose_name="Date de parution")
    valid_art=models.BooleanField(default=True) #validation or not of the article by legal Responsible
    list_to_notify = models.TextField(null=True, verbose_name="Id des personnes notifiée") #list of differents "pro"
                                                # that will be notified when article agreed by legal Responsible

    class Meta:
        verbose_name = "article"
        ordering = ['date']

    def __str__(self):
        return self.title

class ContactUs(models.Model):
    title=models.CharField(max_length=255, verbose_name="Titre",blank=True, default="")
    content = models.TextField(verbose_name="Votre message*")
    email= models.EmailField(verbose_name="email*")
    # fields if ask for user access creation
    username = models.CharField(max_length=255, verbose_name="Nom d'utilisateur",blank=True)
    first_name = models.CharField(max_length=255, verbose_name="Prénom",blank=True)
    last_name= models.CharField(max_length=255, verbose_name="Nom",blank=True)
    #num_ident = models.CharField(max_length=255, verbose_name="Numéro d'identité",blank=True)
    phone = models.CharField(max_length=60, blank=True,verbose_name="Téléphone",default="")
    TYPE_SELECT = (
        ('0', 'Je ne sais pas'),
        ('1', 'Responsable_Legal'),
        ('2', 'Professionnel')
    )
    RLorPro = models.CharField(max_length=11,choices=TYPE_SELECT, default='0',verbose_name="Quel est votre statut ? (Professionnel = Enseignant, Professionnel de santé, Responsable légal = Parent, tuteur)")
    statusRL=models.CharField(blank=True, max_length=25, verbose_name="Statut si résponsable légal (Mère, Père, Tuteur, ...)", default=" ")
    rolePro = models.ForeignKey('CategoriePro', on_delete=models.CASCADE, default=0,
                                verbose_name='Catégorie si professionnel',blank=True)
    child_access_asked = models.CharField(max_length=255, verbose_name="Nom des enfants rattachés",blank=True, default=" ")