from .models import *
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

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

def PermRemover(id_carnet,id_user_to_allow):
    SelectedPerm=Permission.objects.get(codename='CSNB{}_access'.format(id_carnet))
    SelectedUser=User.objects.get(pk=id_user_to_allow)
    SelectedUser.user_permissions.remove(SelectedPerm)