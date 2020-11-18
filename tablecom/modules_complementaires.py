from .forms import *
from django.http import request
from .models import *
from notifications.modules_complementaires import notif_message_by_CNB_and_Correspondant
from django.core.mail import send_mail

def list_of_prof(request,listStringId,id_carnet):
    print("Liste en string : ",listStringId)
    listIdprofs=listStringId.split(";")
    print (listIdprofs)

    NewListProfs=[]

    for prof in listIdprofs:
        try:
            ProfSel=User.objects.get(id=prof)
            print(ProfSel.first_name,' ', ProfSel.last_name, ' ',ProfSel.email)
            ProfSel.RoleProText=CategoriePro.objects.get(id=ProfSel.profil.rolePro_id).name
            print(ProfSel.RoleProText)

            ProfSel.NotifMessage = notif_message_by_CNB_and_Correspondant(request, id_carnet, ProfSel.pk)
            NewListProfs.append(ProfSel)
        except:
            print("Impossible de récupérer certains professionnels, ou erreur de notifications: Vérifier que chaque ID existe")



    return NewListProfs

def list_of_articles(string_of_articles):
    listIDarticles=string_of_articles.split(";")
    #print(listIDarticles)

    NewListArticles=[]

    for article in listIDarticles:
        try :
            articleSel=Article.objects.get(id=article)

            if articleSel.valid_art != True:
                continue
            #print(articleSel.title)
            #print("les numero de l'auteur :",articleSel.id_Professionnal, "ce qui correspond à :",User.objects.get(pk=articleSel.id_Professionnal).first_name,User.objects.get(pk=articleSel.id_Professionnal).last_name)

            articleSel.auteur_first_name=User.objects.get(pk=articleSel.id_Professionnal).first_name
            articleSel.auteur_last_name=User.objects.get(pk=articleSel.id_Professionnal).last_name
            articleSel.auteur_id=User.objects.get(pk=articleSel.id_Professionnal).id
            if articleSel.active != True:  # if article is no longer active, it means that it has been deleted
                articleSel.title = ""
                articleSel.content = "Commentaire supprimé par son auteur"


            NewListArticles.append(articleSel)



        except:
            print("Impossible de récupérer l'item {0} : Vérifier que chaque ID existe".format(article))



    return NewListArticles

def PermCreationAccessLastEntry(model_transmis):
    #ok quite complicated : this function will be called at each new CSNB creation, will catch last entry and create
    #a permition to last item of "model_transmis".
    lastId=model_transmis.objects.all().order_by('-id')[0].id
    content_type = ContentType.objects.get_for_model(model_transmis)
    permission = Permission.objects.create(
        codename='CSNB{0}_access'.format(lastId),
        name='Acces to CSNB number {0}'.format(lastId),
        content_type=content_type,
    )

def send_a_mail(subject,content):
    send_mail(subject,content,'devtemp@alaincarrot.com',['devtemp@alaincarrot.com'],fail_silently=False,)
    print("Message bien envoyé en mail")