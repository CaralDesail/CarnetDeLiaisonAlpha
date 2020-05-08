from .forms import *
from django.http import request
from .models import *
from django.db.models import Max


def PermCreationOneEntry(model_transmis, IdToCreate):
    # this function will be called to create the permissions needed for one id entry of a table/class "model transmis"

    content_type = ContentType.objects.get_for_model(model_transmis)
    permission = Permission.objects.create(
        codename='CSNB{0}_access'.format(IdToCreate),
        name='Acces to CSNB number {0}'.format(IdToCreate),
        content_type=content_type,
    )

def PermCreationAllEntry(model_transmis):
    # this function will be called to create all the permissions needed for id entry of a table/class "model transmis"
    idMax=model_transmis.objects.all().aggregate(Max('id'))
    idMaxValue=idMax['id__max']

    print(model_transmis.objects.all()[0])
    for idTest in range(0,idMaxValue):
        try :
            PermCreationOneEntry(model_transmis,idTest)
            print("Entrée {0} créée".format(idTest))
        except :
            print("Entrée {0} non créée".format(idTest))



