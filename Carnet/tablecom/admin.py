from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class ChildSNotebookAdmin(admin.ModelAdmin):
    list_display   = ('id', 'name', 'forename','date_of_birth')
    #list_filter    = ('id', 'date_of_birth',)
    #date_hierarchy = 'date'
    #ordering       = ('id','name', 'date_of_birth',)
    search_fields  = ('name', 'forename','date_of_birth')


class CategorieProAdmin(admin.ModelAdmin):
    list_display = ('id','name')

class ProfilAdmin(admin.StackedInline):
    model = Profil
    can_delete = False
    verbose_name_plural = 'Profil'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfilAdmin,)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

admin.site.register(ChildSNotebook,ChildSNotebookAdmin)
admin.site.register(CategoriePro,CategorieProAdmin)
#admin.site.register(Profil)
admin.site.register(Article,ArticleAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Permission)

# Register your models here.
