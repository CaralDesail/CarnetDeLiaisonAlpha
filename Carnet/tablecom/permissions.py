from .models import *
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import Permission, User



def PermUniqueCreation():
    content_type = ContentType.objects.get_for_model(ChildSNotebook)
    permission = Permission.objects.create(
        codename='can_publish',
        name='Can Publish Posts',
        content_type=content_type,
    )

def PermAllower(id_carnet,id_user_to_allow):
    SelectedPerm=Permission.objects.get(codename='CSNB{}_access'.format(id_carnet))
    SelectedUser=User.objects.get(pk=id_user_to_allow)
    SelectedUser.user_permissions.add(SelectedPerm)
    PermStateCoherenceToCSNB(id_carnet)


def PermRemover(id_carnet,id_user_to_remove):
    SelectedPerm=Permission.objects.get(codename='CSNB{}_access'.format(id_carnet))
    SelectedUser=User.objects.get(pk=id_user_to_remove)
    SelectedUser.user_permissions.remove(SelectedPerm)
    PermStateCoherenceToCSNB(id_carnet)

def PermStateCoherenceToCSNB(id_carnet): #for few users, will do the job , for more, can be loud so must be replaced by carnet editing function (add, and remove)
    carnet = get_object_or_404(ChildSNotebook, id=id_carnet)

    #about pro :
    carnet.id_prof_auth=""
    carnet.save()
    userProList=User.objects.filter(groups="2")
    for userSel in userProList:
        print (userSel, userSel.pk)
        print("check if : user",userSel," access to ", 'CSNB{}_access'.format(id_carnet), ": ",userSel.has_perm('tablecom.CSNB{}_access'.format(id_carnet)))
        if userSel.has_perm('tablecom.CSNB{}_access'.format(id_carnet)):

            carnet.id_prof_auth+=str(userSel.pk)+";"
            carnet.save()

    #about RL :
    carnet.id_RespLeg=""
    carnet.save()
    userRLList=User.objects.filter(groups="3")
    for userSel in userRLList:
        print(userSel, userSel.pk)
        print("check if : user", userSel, " access to ", 'CSNB{}_access'.format(id_carnet), ": ",
              userSel.has_perm('tablecom.CSNB{}_access'.format(id_carnet)))
        if userSel.has_perm('tablecom.CSNB{}_access'.format(id_carnet)):
            carnet.id_RespLeg += str(userSel.pk) + ";"
            carnet.save()