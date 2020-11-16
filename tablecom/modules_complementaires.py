from .forms import *
from django.http import request
from .models import *

def list_of_prof(listStringId):
    print("Liste en string : ",listStringId)
    listIdprofs=listStringId.split(";")
    print (listIdprofs)

    NewListProfs=[]

    for prof in listIdprofs:
        try:
            ProfSel=User.objects.get(id=prof)
            print(type(ProfSel))
            print(ProfSel.first_name,' ', ProfSel.last_name, ' ',ProfSel.email)
            NewListProfs.append(ProfSel)
        except:
            print("Impossible de récupérer certains professionnels: Vérifier que chaque ID existe")

    return NewListProfs

def list_of_articles(string_of_articles):
    listIDarticles=string_of_articles.split(";")
    #print(listIDarticles)

    NewListArticles=[]

    for article in listIDarticles:
        try :
            articleSel=Article.objects.get(id=article)
            if articleSel.active != True :
                continue
            if articleSel.valid_art != True:
                continue
            #print(articleSel.title)
            #print("les numero de l'auteur :",articleSel.id_Professionnal, "ce qui correspond à :",User.objects.get(pk=articleSel.id_Professionnal).first_name,User.objects.get(pk=articleSel.id_Professionnal).last_name)
            articleSel.auteur_first_name=User.objects.get(pk=articleSel.id_Professionnal).first_name
            articleSel.auteur_last_name=User.objects.get(pk=articleSel.id_Professionnal).last_name
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
