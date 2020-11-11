from django.contrib import admin
from .models import *


class CorrespondanceTableAdmin(admin.ModelAdmin):
    list_display   = ('id', 'idUser', 'messagesAccess')
    #list_filter    = ('id', 'date_of_birth',)
    #date_hierarchy = 'date'
    #ordering       = ('id','name', 'date_of_birth',)
    search_fields  = ('idUser', 'messagesAccess')

class MessagesPersoAdmin(admin.ModelAdmin):
    list_display   = ('id', 'titre', 'auteurID','date')
    #list_filter    = ('id', 'date_of_birth',)
    #date_hierarchy = 'date'
    #ordering       = ('id','name', 'date_of_birth',)
    search_fields  = ('auteurID', 'date')

# Register your models here.
admin.site.register(MessagePerso,MessagesPersoAdmin)
admin.site.register(CorrespondanceTableMessagesByUser,CorrespondanceTableAdmin)