from .forms import *
from django.http import request

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
            print("Impossible de récupérer la liste des professionnels: Vérifier que chaque ID existe")
            return None
    return NewListProfs

def list_of_articles(string_of_articles):
    listIDarticles=string_of_articles.split(";")
    #print(listIDarticles)

    NewListArticles=[]

    for article in listIDarticles:
        try :
            articleSel=Article.objects.get(id=article)
            print(articleSel.title)
            NewListArticles.append(articleSel)
        except:
            print("Impossible de récupérer la liste des articles : Vérifier que chaque ID existe")
            return None

    return NewListArticles

